# -*- coding: utf-8 -*-

from alchemyapi import AlchemyAPI

label_alchemy = {
"City":"GEO", 
"Facility":"GEO",
"StateOrCounty":"GEO",
"Country":"GEO",
"Region":"GEO",
"Continent":"GEO", 
"Person":"PERSON",
"Company":"ORG",
"Organization":"ORG",
"PrintMedia":"ORG",
"JobTitle":"FUNCTION",
"Quantity":"NUMBER",
"SportingEvent":"EVENT",
"Drug":"KEYWORD",
"HealthCondition":"KEYWORD",
"FieldTerminology":"KEYWORD",
"Sport":"KEYWORD",
"Technology":"KEYWORD",
"EntertainmentAward":"KEYWORD",
"Holiday":"EVENT"
}

def convert_label(label):
	if label in label_alchemy:
		return label_alchemy[label]
	else:
		print "alchemy:",label
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
