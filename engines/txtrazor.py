# -*- coding: utf-8 -*-
from textrazor import TextRazor

client = TextRazor(api_key="18f6730269b89e61a2d9c89853960328aa5511226830cf32025ce43e", extractors=["entities", "topics"])

label_textrazor = {
"Place":"GEO", 
"Person":"PERSON", 
"Organisation" : "ORG",
"Company":"ORG",
"Disease":"KEYWORD",
"Species":"KEYWORD",
"AnatomicalStructure":"KEYWORD",
"Drug":"KEYWORD",
"ChemicalSubstance":"KEYWORD",
"Work":"PRODUCT",
"EthnicGroup":"KEYWORD"}

def convert_labels(labels):
	for label in labels:
		if label in label_textrazor:
			return label_textrazor[label]
	if not labels:
		return "KEYWORD"
	else:
		return labels		

def extract_entities(text):
	entities={}
	rp = client.analyze(text)
	for entity in rp.entities():
		key = entity.id
		value = convert_labels(entity.dbpedia_types)
		entities[key] = value
	return entities