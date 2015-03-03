# -*- coding: utf-8 -*-
import requests
import json

label_retresco = {"geos":"GEO", "persons":"PERSON"}

def convert_label(label):
	if label in label_retresco:
		return label_retresco[label]
	else:
		return label

def extract_entities(text):
	entities={}
	data={}
	data["body"]=text
	rp = requests.post('http://pideas-dh04/enrich?userkey=1A5319EA-4AA0-48D8-8010-7952863851D0', data=json.dumps(data))
	result = rp.json()
	categories = result["result"]["keywords"].items()
	for category in categories:
		value = category[0]
		for element in category[1]:
			key = element["lemma"]
			entities[key] = convert_label(value)
	return entities			