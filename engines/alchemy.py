# -*- coding: utf-8 -*-

from alchemyapi import AlchemyAPI

label_alchemy = {"City":"GEO", "Facility":"GEO", "Person":"PERSON"}

def convert_label(label):
	if label in label_alchemy:
		return label_alchemy[label]
	else:
		return label

def extract_entities(text):
	entities = {}
	alchemyapi = AlchemyAPI()
	response = alchemyapi.entities('text', text, {'sentiment': 1})
	if response['status'] == 'OK':
		for entity in response['entities']:
			key = entity['text'].encode('utf-8')
			value = entity['type']
			entities[key] = convert_label(value)
	return entities
