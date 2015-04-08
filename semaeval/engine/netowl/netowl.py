# -*- coding: utf-8 -*-
import requests

from ... import config

if "netowl" in config.engines:
	key = config.engines["netowl"]["key"]
	labels = config.engines["netowl"]["labels"]
	langs = config.engines["netowl"]["langs"]


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