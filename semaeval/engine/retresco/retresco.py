# -*- coding: utf-8 -*-
import requests
import json

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import yaml
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

key = config["key"]
host = config["host"]
server_cert = config["server_cert"]
labels = config["labels"]


def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "retresco:",label
		return label


def extract_entities(text, lang):
	entities = {}
	data = {"body": text}
	rp = requests.post(host + '/enrich?userkey=' + key, data=json.dumps(data), verify=os.path.join(__location__, server_cert))
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