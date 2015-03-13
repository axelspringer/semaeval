#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from boilerpipe.extract import Extractor
import yaml
import utils_yaml
import email.utils
import datetime 

french_dir = "../input/fr/"

rss_huffingtonpost = "http://www.huffingtonpost.fr/feeds/index.xml"

def articles_from_feed():
	articles=[]

	feed = feedparser.parse(rss_huffingtonpost)
	for item in feed["items"]:
		url = item["link"]
		print item["published"]
		print url
		try:
			extractor = Extractor(extractor="ArticleExtractor", url=url)

			date = email.utils.parsedate_tz(item["published"])
			timestamp = email.utils.mktime_tz(date)
			iso = datetime.datetime.utcfromtimestamp(timestamp).isoformat()

			data = {"text": extractor.getText(), "date": iso, "url":url }
		except Exception as e:
			print "Error downloading article from " + url
		articles.append(data)
	return articles

if __name__ == '__main__':

	articles = articles_from_feed()

	for article in articles:
		url = article["url"]
		filename = url.split(",")[-1].split(".")[0]

		with open(french_dir + filename + ".yml", "w") as f:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			utils_yaml.ordered_dump(article, f, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)
