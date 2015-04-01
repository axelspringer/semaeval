#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import argparse
from xml.etree import ElementTree
import re
import os

import feedparser
import requests
import dateutil.parser
import yaml

from semaeval import utils as storage


store_dir = "input/"
rss_welt = "http://www.welt.de/?service=Rss"
regex = re.compile("article\d+")

default_urls = [
"http://www.welt.de/english-news/article3181485/Germany-is-the-most-beloved-country-worldwide.html",
"http://www.welt.de/english-news/article4174441/United-States-to-begin-swine-flu-vaccine-trials.html",
"http://www.welt.de/english-news/article4201214/Are-Rihanna-and-Chris-Brown-back-together.html",
"http://www.welt.de/english-news/article4209330/Dr-Murray-gave-Michael-Jackson-lethal-injection.html",
"http://www.welt.de/english-news/article4216441/Soldiers-on-the-hunt-for-members-of-Islamic-sect.html"
]


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
	id = regex.findall(url)[0]
	download_url = "http://www.welt.de/" + id + ".xmli"
	r = requests.get(download_url)
	xml = ElementTree.fromstring(r.content)
	date_tag = xml.find(".//Property[@FormalName='PublicationDateLong']")
	iso = dateutil.parser.parse(date_tag.attrib["Value"]).isoformat()

	text_tag = xml.find(".//body.content")
	text = ""
	for child in text_tag:
		if child.text and child.text.strip():
			text = text + child.text.strip() + "\n"

	filename = id + ".yml"

	data = {"text": text, "date": iso, "url": url, "filename": filename }
	return data

def store_articles(articles, prefix):
	dir = store_dir + prefix + "/"
	# create the directory if it does not yet exist
	# see http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
	try:
		os.makedirs(dir)
	except OSError:
		if not os.path.isdir(dir):
			raise

	# see http://stackoverflow.com/questions/998938/handle-either-a-list-or-single-integer-as-an-argument
	if type(articles) is not list: articles = [articles]

	for article in articles:
		path = dir + article["filename"]
		print "Storing file: ", path
		with open(path, "w") as f:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			storage.ordered_dump(article, f, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)

def load_articles(prefix):
	articles = []
	dir = store_dir + prefix + "/"

	for filename in os.listdir(dir):
		if filename.endswith(".yml"):
			with open(dir + filename,"r") as f:
				data = storage.ordered_load(f, yaml.SafeLoader)
				articles.append(data)
	return articles

# start with "python -m semaeval.source.welt semaeval/source/welt.py"
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download article text from welt.de url.')
	parser.add_argument("url", metavar="URL", type=str, nargs="?", help="The url to download text from.")
	parser.add_argument("-l","--lang", type=str, help="Language of the text (two-letter code: en, de, fr, ...)", required=True)

	args=parser.parse_args()

	url = args.url
	if url:
		article = article_from_url(url)
		store_articles(article, args.lang)
	else:
		# download some default articles
		for url in default_urls:
			article = article_from_url(url)
			store_articles(article, args.lang)
