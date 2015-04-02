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


def convert_label(label):
	prefix = ">".join(label.split(">")[:2])
	if prefix in labels:
		return labels[prefix]
	else:
		print "meaningcloud:",label
		return label


def extract_entities(text, lang):
	entities = {}
	
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	# see https://www.meaningcloud.com/developer/topics-extraction/doc/1.2/request
	data = {'key': key, 'lang': lang, 'txt': text, 'tt': 'e'}

	rp = requests.post('http://api.meaningcloud.com/topics-1.2.php', headers=headers, data=data)
	result = rp.json()
	if "entity_list" in result:
		for entity in result["entity_list"]:
			k = entity["form"]
			v = convert_label(entity["sementity"]["type"])
			entities[k] = v
	return entities			