# -*- coding: utf-8 -*-
import requests
import json

# see http://www.bitext.com/btxt_docs/Bitext_API-Reference-Manual_EN.pdf, page 33
label_bitext = {3:"GEO", 1:"PERSON", 0: "UNKNOWN"}

def convert_label(label):
	if label in label_bitext:
		return label_bitext[label]
	else:
		return label

def extract_entities(text):
	entities={}
	# see also http://www.bitext.com/btxt_docs/API_Code/Bitext_API_Client_Python.txt
	headers = {"Content-type": "application/x-www-form-urlencoded"}
	# ID must be a number not a string. Otherwise the returned JSON is invalid. Bug in the example above or in the API?
	data = {'User': 'amaier1', 'Pass': 'Qp76dY1DQ', 'Lang': 'ENG', 'ID': 0001, 'Text': text, 'Detail': 'Detailed', 'OutFormat':'JSON', 'Normalized': 'Yes', 'Theme': 'Gen'}
	rp = requests.post("http://svc8.bitext.com/WS_Nops_Ent/Service.aspx", data=data, headers=headers)
	result = rp.json()
	for entity in result["entities"]:
		key = entity["ent_norm"]
		value = convert_label(entity["type"])
		entities[key] = value
	return entities