# -*- coding: utf-8 -*-
import requests
import json

# see http://www.bitext.com/btxt_docs/Bitext_API-Reference-Manual_EN.pdf, page 33
label_bitext = {19: "NUMBER", 15: "CURRENCY", 10: "DATE", 8: "URL", 7: "ORG", 6: "ORG", 3: "GEO", 1: "PERSON", 0: "KEYWORD"}
# conversion from ISO_639-1 to bitext language codes (see page 50 of http://www.bitext.com/btxt_docs/Bitext_API-Reference-Manual_EN.pdf)
lang_bitext = {"en": "ENG", "de": "DEU", "es": "ESP", "pt": "POR", "it": "ITA", "fr": "FRA", "nl": "NLD","ca": "CAT"}


def convert_label(label):
	if label in label_bitext:
		return label_bitext[label]
	else:
		print "bitext:",label
		return label


def convert_lang(lang):
	if lang in lang_bitext:
		return lang_bitext[lang]
	else:
		return lang


def extract_entities(text, lang):
	entities={}
	language = convert_lang(lang)
	# see also http://www.bitext.com/btxt_docs/API_Code/Bitext_API_Client_Python.txt
	headers = {"Content-type": "application/x-www-form-urlencoded"}
	# ID must be a number not a string. Otherwise the returned JSON is invalid. Bug in the example above or in the API?
	data = {'User': 'amaier1', 'Pass': 'Qp76dY1DQ', 'Lang': language, 'ID': 0001, 'Text': text, 'Detail': 'Detailed', 'OutFormat':'JSON', 'Normalized': 'No', 'Theme': 'Gen'}
	rp = requests.post("http://svc8.bitext.com/WS_Nops_Ent/Service.aspx", data=data, headers=headers)
	try:
		result = rp.json()
		for entity in result["entities"]:
			key = entity["ent_text"]
			value = convert_label(entity["type"])
			entities[key] = value
	except ValueError, e:
		print "Bitext API Error:", e
		print "Bitext Response:", rp.content
	return entities