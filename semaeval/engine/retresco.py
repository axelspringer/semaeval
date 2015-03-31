# -*- coding: utf-8 -*-
import requests
import json

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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
	entities = {}
	data = {"body": text}
	rp = requests.post('https://rtr.ipool.asideas.de/enrich?userkey=1A5319EA-4AA0-48D8-8010-7952863851D0', data=json.dumps(data), verify=os.path.join(__location__, "rtr_ipool.pem"))
	try:
		result = rp.json()
		categories = result["result"]["keywords"].items()
		for category in categories:
			value = category[0]
			for element in category[1]:
				key = element["lemma"]
				entities[key] = convert_label(value)
	except ValueError as e:
		print "Retresco API:", e
		print "Retresco API response:", rp.content
	return entities			