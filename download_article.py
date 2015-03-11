#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
from xml.etree import ElementTree
import dateutil.parser
import yaml
import re

english_dir = "input/english/"

regex = re.compile("article\d+")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download article text from welt.de url.')
	parser.add_argument("url", metavar="URL", type=str, nargs="?", help="The url to download text from.")

	args=parser.parse_args()

	url = args.url
	if url:

		download_url = url.replace("html","xmli")
		r = requests.get(download_url)
		xml = ElementTree.fromstring(r.content)
		date_tag = xml.find(".//Property[@FormalName='PublicationDateLong']")
		iso = dateutil.parser.parse(date_tag.attrib["Value"]).isoformat()

		text_tag = xml.find(".//body.content")
		text=""
		for child in text_tag:
			if child.text and child.text.strip():
				text = text + child.text.strip() +"\n"

		data = {"text": text , "date": iso , "url":url }

		filename = regex.findall(url)[0]
		with open(english_dir + filename + ".yml", "w") as f:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			yaml.safe_dump(data, f, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)
