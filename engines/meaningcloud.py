# -*- coding: utf-8 -*-
import requests
import json

label_meaningcloud = {"Top>Location":"GEO", "Top>Person":"PERSON", "Top":"UNKNOWN"}

def convert_label(label):
	prefix=">".join(label.split(">")[:2])
	if prefix in label_meaningcloud:
		return label_meaningcloud[prefix]
	else:
		return label

def extract_entities(text):
	entities={}
	
  	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
  	# see https://www.meaningcloud.com/developer/topics-extraction/doc/1.2/request
  	data = {'key': 'dbc8c605163c8e789c2faaa9ce05fbde', 'lang': 'en', 'txt': text, 'tt': 'e'}

	rp = requests.post('http://api.meaningcloud.com/topics-1.2.php', headers=headers, data=data)
	result = rp.json()
	for entity in result["entity_list"]:
		key = entity["form"]
		value = convert_label(entity["sementity"]["type"])
		entities[key]=value
	return entities			