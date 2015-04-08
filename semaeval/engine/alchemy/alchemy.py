# -*- coding: utf-8 -*-

import yaml
from alchemyapi import AlchemyAPI

from ... import config

if "alchemy" in config.engines:
	labels = config.engines["alchemy"]["labels"]


def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "alchemy:", label
		return label


def extract_entities(text, lang):
	entities = {}
	alchemyapi = AlchemyAPI()
	response = alchemyapi.entities('text', text, {'sentiment': 1})
	if response['status'] == 'OK':
		for entity in response['entities']:
			key = entity['text'].encode('utf-8')
			value = entity['type']
			entities[key] = convert_label(value)
	return entities
