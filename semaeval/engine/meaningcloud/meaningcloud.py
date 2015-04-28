# -*- coding: utf-8 -*-
import requests

from ... import config

if "meaningcloud" in config.engines:
	key = config.engines["meaningcloud"]["key"]
	labels = config.engines["meaningcloud"]["labels"]


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