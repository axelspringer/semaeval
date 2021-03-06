#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.etree import ElementTree
import re
import os

import dateutil.parser
import yaml

from semaeval import utils as storage


store_dir = "input/"
url_regex = re.compile("(?<=Weblink: )(.*)")


def articles_from_dir(dir):
	articles = []
	for filename in os.listdir(dir):
		path = dir + "/" + filename
		data = article_from_path(path)
		articles.append(data)
	return articles


def article_from_path(path):
	xml = ElementTree.parse(path)
	date_tag = xml.find(".//DAT")
	iso = dateutil.parser.parse(date_tag.text).isoformat()

	text_tag = xml.find(".//BODY")
	text = ""
	for child in text_tag:
		if child.tag == "P":
			if child.text and child.text.strip():
				text = text + child.text.strip() + "\n"
	url = None
	url_tag = xml.find(".//FUS")
	if url_tag is not None:
		result = url_regex.search(url_tag.text)
		if result is not None:
			url = result.group()

	basename = os.path.basename(path)
	filename = basename.split(".")[0] + ".yml"
	if url:
		data = {"text": text, "date": iso, "url": url, "filename": filename }
	else:
		data = {"text": text, "date": iso, "filename": filename }

	return data


def store_articles(articles, prefix):
	folder = store_dir + prefix + "/"
	# create the directory if it does not yet exist
	# see http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
	try:
		os.makedirs(folder)
	except OSError:
		if not os.path.isdir(folder):
			raise

	# see http://stackoverflow.com/questions/998938/handle-either-a-list-or-single-integer-as-an-argument
	if type(articles) is not list: articles = [articles]

	for article in articles:
		path = folder + article["filename"]
		print "Storing file: ", path
		with open(path, "w") as f:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			storage.ordered_dump(article, f, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)


def load_articles(prefix):
	articles = []
	folder = store_dir + prefix + "/"

	for filename in os.listdir(folder):
		if filename.endswith(".yml"):
			with open(folder + filename,"r") as f:
				data = storage.ordered_load(f, yaml.SafeLoader)
				articles.append(data)
	return articles

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parse syndication article from file path.')
	parser.add_argument("path", metavar="PATH", type=str, nargs="?", help="The file path to read text from.")
	parser.add_argument("-l","--lang", type=str, help="Language of the text (two-letter code: en, de, fr, ...)", required=True)

	args = parser.parse_args()

	path = args.path
	if path:
		article = article_from_path(path)
		store_articles(article, args.lang)
