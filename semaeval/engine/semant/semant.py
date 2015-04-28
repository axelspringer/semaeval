# -*- coding: utf-8 -*-

import semantria
import uuid
import time

from ... import config

if "semantria" in config.engines:
	key = config.engines["semantria"]["key"]
	secret = config.engines["semantria"]["secret"]
	labels = config.engines["semantria"]["labels"]
	langs = config.engines["semantria"]["langs"]

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
			# get processed documents (you have to use the same config_id as for queuing!)
			status = session.getProcessedDocuments(config_id=config_id)
			results.extend(status)

		for data in results:
			if "entities" in data:
				for entity in data["entities"]:
					k = entity['title']
					v = convert_label(entity['entity_type'])
					entities[k] = v

	return entities
