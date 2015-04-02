# -*- coding: utf-8 -*-

import semantria
import uuid
import time

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import yaml
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

key = config["key"]
secret = config["secret"]
labels = config["labels"]
langs = config["langs"]

serializer = semantria.JsonSerializer()
session = semantria.Session(key, secret, serializer, use_compression=True)


def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "semantria:",label
		return label


def convert_lang(lang):
	if lang in langs:
		return langs[lang]
	else:
		return lang


def extract_entities(text, lang):
	# Semantria seems to have a limit of 8192 chars per document (at least with the demo key)
	text = text[:8191]
	entities = {}
	doc = {"id": str(uuid.uuid4()).replace("-", ""), "text": text}
	config_id = convert_lang(lang)
	status = session.queueDocument(doc, config_id=config_id)
	if status == 202:
		results = []

		while len(results) < 1:
			time.sleep(2)
			# get processed documents (you have use the same config_id as for queuing!)
			status = session.getProcessedDocuments(config_id=config_id)
			results.extend(status)

		for data in results:
			if "entities" in data:
				for entity in data["entities"]:
					key = entity['title']
					value = convert_label(entity['entity_type'])
					entities[key] = value

	return entities
