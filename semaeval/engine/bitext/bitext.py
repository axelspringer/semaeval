# -*- coding: utf-8 -*-
import requests

from ... import config

if "bitext" in config.engines:
	user = config.engines["bitext"]["user"]
	passwd = config.engines["bitext"]["passwd"]
	labels = config.engines["bitext"]["labels"]
	langs = config.engines["bitext"]["langs"]

def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "bitext:",label
		return label


def convert_lang(lang):
	if lang in langs:
		return langs[lang]
	else:
		return lang


def extract_entities(text, lang):
	entities={}
	language = convert_lang(lang)
	# see also http://www.bitext.com/btxt_docs/API_Code/Bitext_API_Client_Python.txt
	headers = {"Content-type": "application/x-www-form-urlencoded"}
	# ID must be a number not a string. Otherwise the returned JSON is invalid. Bug in the example above or in the API?
	data = {'User': user, 'Pass': passwd, 'Lang': language, 'ID': 0001, 'Text': text, 'Detail': 'Detailed', 'OutFormat':'JSON', 'Normalized': 'No', 'Theme': 'Gen'}
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