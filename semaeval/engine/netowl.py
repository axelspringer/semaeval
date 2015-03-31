# -*- coding: utf-8 -*-
import requests
import json

label_netowl = {
	"entity:person": "PERSON",
	"entity:place": "GEO",
	"entity:organization": "ORG",
	"entity:time": "DATE",
	"entity:other": "KEYWORD",
	"entity:numeric": "NUMBER",
	"entity:address": "URL",
	"entity:artifact": "PRODUCT"
}

lang_netowl = {
	"en": "nametag-english-sentiment-analysis-ignoresgml-json",
	"fr": "nametag-french-ignoresgml-json",
	}

def convert_label(label):
	prefix = ":".join(label.split(":")[:2])
	if prefix in label_netowl:
		return label_netowl[prefix]
	else:
		print "netowl:", label
		return label


def convert_lang(lang):
	if lang in lang_netowl:
		return lang_netowl[lang]
	else:
		return lang


def extract_entities(text, lang):
	entities = {}

	data = text.encode("utf-8")
	endpoint = convert_lang(lang)
	rp = requests.post("https://dev.netowl.com/extractor/simple/presets/"+ endpoint + "?apiKey=a09820f5-4f82-4c26-a5a9-1724e985a776", data=data)
	try:
		result = rp.json()

		for entity in result["entity"]:
			key = entity["value"]
			entities[key] = convert_label(entity["ontology"])
	except Exception as e:
		print "NetOwl API Error:", e
		print "NetOwl Response:", rp.content
	return entities