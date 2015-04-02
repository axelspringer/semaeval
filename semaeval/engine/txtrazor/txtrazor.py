# -*- coding: utf-8 -*-
from textrazor import TextRazor
from textrazor import TextRazorAnalysisException

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import yaml
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

key = config["key"]
labels = config["labels"]

client = TextRazor(api_key=key, extractors=["entities", "topics"])


def convert_labels(label_list):
	for label in label_list:
		if label in labels:
			return labels[label]
	if not labels:
		return "KEYWORD"
	else:
		print "textrazor:", labels
		return labels[0]


def extract_entities(text, lang):
	print "txtrazor extract_entities"
	entities = {}
	try:
		rp = client.analyze(text)
		for entity in rp.entities():
			k = entity.id
			v = convert_labels(entity.dbpedia_types)
			entities[k] = v
	except TextRazorAnalysisException as e:
		print "TextRazor API:", e

	return entities