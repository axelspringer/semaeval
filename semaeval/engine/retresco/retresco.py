# -*- coding: utf-8 -*-
import requests
import json

from ... import config

if "retresco" in config.engines:
	key = config.engines["retresco"]["key"]
	host = config.engines["retresco"]["host"]
	server_cert = config.engines["retresco"]["server_cert"]
	labels = config.engines["retresco"]["labels"]


def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "retresco:",label
		return label


def extract_entities(text, lang):
	entities = {}
	data = {"body": text}
	rp = requests.post(host + '/enrich?userkey=' + key, data=json.dumps(data), verify=server_cert)
	try:
		result = rp.json()
		categories = result["result"]["keywords"].items()
		for category in categories:
			value = category[0]
			for element in category[1]:
				k = element["lemma"]
				entities[k] = convert_label(value)
	except ValueError as e:
		print "Retresco API:", e
		print "Retresco API response:", rp.content
	return entities			