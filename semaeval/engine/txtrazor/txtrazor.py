# -*- coding: utf-8 -*-
from textrazor import TextRazor
from textrazor import TextRazorAnalysisException

from ... import config

if "textrazor" in config.engines:
	key = config.engines["textrazor"]["key"]
	labels = config.engines["textrazor"]["labels"]

	client = TextRazor(api_key=key, extractors=["entities", "topics"])


def convert_labels(label_list):
	for label in label_list:
		if label in labels:
			return labels[label]
	if not label_list:
		return "KEYWORD"
	else:
		print "textrazor:", label_list
		return label_list[0]


def extract_entities(text, lang):
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