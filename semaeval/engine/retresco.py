# -*- coding: utf-8 -*-
import requests
import json

label_retresco = {
"geos": "GEO",
"persons": "PERSON",
"orgs": "ORG",
"products": "PRODUCT",
"keywords": "KEYWORD",
"events":" EVENT"}

def convert_label(label):
	if label in label_retresco:
		return label_retresco[label]
	else:
		print "retresco:",label
		return label

def extract_entities(text, lang):
	entities={}
	data={}
	data["body"]=text
	rp = requests.post('https://rtr.ipool.asideas.de/enrich?userkey=1A5319EA-4AA0-48D8-8010-7952863851D0', data=json.dumps(data), verify=False)
	result = rp.json()
	categories = result["result"]["keywords"].items()
	for category in categories:
		value = category[0]
		for element in category[1]:
			key = element["lemma"]
			entities[key] = convert_label(value)
	return entities			