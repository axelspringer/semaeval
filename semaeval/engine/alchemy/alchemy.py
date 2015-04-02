# -*- coding: utf-8 -*-

import yaml
from alchemyapi import AlchemyAPI

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

labels = config["labels"]


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
