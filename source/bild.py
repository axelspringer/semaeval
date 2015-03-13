#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.etree import ElementTree

import feedparser
import requests
import dateutil.parser
import yaml
import utils_yaml


german_dir = "input/de/"

rss_bild = "http://rss.bild.de/bild.xml"

# Helper method to convert from
# http://da.feedsportal.com/c/32310/f/645629/s/445b0d9d/l/0L0Sbild0Bde0Clifestyle0C20A150Ckrimi0Cneue0Ekrimis0Eleipziger0Ebuchmesse0E39960A1460Bbild0Bhtml/ia1.htm
# to this
# http://www.bild.de/lifestyle/2015/krimi/neue-krimis-leipziger-buchmesse-39960146.bild.html
def convert_url(url):

	temp1 = url.split("/")[-2]
	temp2 = (temp1
				 .replace("0A","0")
				 .replace("0B",".")
				 .replace("0C","/")
				 .replace("0E","-")
				 .replace("0H",",")
				 .replace("0I","_")
				 .replace("0L","")
				 .replace("0S",""))
	return "http://" + temp2


def articles_from_feed():
	articles = []
	feed = feedparser.parse(rss_bild)
	for item in feed["items"]:
		url = convert_url(item["link"])
		print item["published"]
		print url
		if "bild-plus" not in url:
			data = article_from_url(url)
			articles.append(data)
	return articles


def article_from_url(url):
	download_url = url.replace("html","xmli")

	r = requests.get(download_url)

	xml = ElementTree.fromstring(r.content)
	date_tag = xml.find(".//Property[@FormalName='PublicationDateLong']")
	iso = dateutil.parser.parse(date_tag.attrib["Value"]).isoformat()

	text_tag = xml.find(".//body.content/p")
	text = ""
	for child in text_tag.iter():
		if child.text and child.text.strip():
			text = text + child.text.strip() +"\n"

	return {"text": text, "date": iso, "url": url}


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download article text from bild.de url.')
	parser.add_argument("url", metavar="URL", type=str, nargs="?", help="The url to download text from.")

	args = parser.parse_args()

	url = args.url
	if url:
		article = article_from_url(url)
		filename = url.split(".")[-3]
		with open(german_dir + filename + ".yml", "w") as f:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			utils_yaml.ordered_dump(article, f, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)
