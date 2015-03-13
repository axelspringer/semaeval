#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import urlparse
import requests
import argparse
from xml.etree import ElementTree
import dateutil.parser
import yaml
import utils_yaml
import re

english_dir = "../input/en/"

rss_welt = "http://www.welt.de/?service=Rss"

regex = re.compile("article\d+")


# Helper method to get the real url of the article
def convert_url(url):

	url_data = urlparse.urlparse(url)
	params = urlparse.parse_qs(url_data.query)

	return "http://www.welt.de/article" + params["artid"][0] + ".html"


def articles_from_feed():
	articles = []
	feed = feedparser.parse(rss_welt)
	for item in feed["items"]:
		url = convert_url(item["link"])
		print item["published"]
		print url
		data = article_from_url(url)
		articles.append(data)
	return articles


def article_from_url(url):
	download_url = url.replace("html","xmli")
	r = requests.get(download_url)
	xml = ElementTree.fromstring(r.content)
	date_tag = xml.find(".//Property[@FormalName='PublicationDateLong']")
	iso = dateutil.parser.parse(date_tag.attrib["Value"]).isoformat()

	text_tag = xml.find(".//body.content")
	text = ""
	for child in text_tag:
		if child.text and child.text.strip():
			text = text + child.text.strip() + "\n"

	data = {"text": text, "date": iso, "url": url}
	return data


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download article text from welt.de url.')
	parser.add_argument("url", metavar="URL", type=str, nargs="?", help="The url to download text from.")

	args=parser.parse_args()

	url = args.url
	if url:
		article = article_from_url(url)
		filename = regex.findall(url)[0]
		with open(english_dir + filename + ".yml", "w") as f:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			utils_yaml.ordered_dump(article, f, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)
