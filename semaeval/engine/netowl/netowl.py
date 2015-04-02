# -*- coding: utf-8 -*-
import requests
import json

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import yaml
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

key = config["key"]
labels = config["labels"]
langs = config["langs"]


def convert_label(label):
	prefix = ":".join(label.split(":")[:2])
	if prefix in labels:
		return labels[prefix]
	else:
		print "netowl:", label
		return label


def convert_lang(lang):
	if lang in langs:
		return langs[lang]
	else:
		return lang


def extract_entities(text, lang):
	entities = {}

	data = text.encode("utf-8")
	endpoint = convert_lang(lang)
	rp = requests.post("https://dev.netowl.com/extractor/simple/presets/" + endpoint + "?apiKey=" + key, data=data)
	try:
		result = rp.json()

		for entity in result["entity"]:
			k = entity["value"]
			entities[k] = convert_label(entity["ontology"])
	except Exception as e:
		print "NetOwl API Error:", e
		print "NetOwl Response:", rp.content
	return entities