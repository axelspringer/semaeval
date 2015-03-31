# -*- coding: utf-8 -*-
from textrazor import TextRazor
from textrazor import TextRazorAnalysisException

client = TextRazor(api_key="18f6730269b89e61a2d9c89853960328aa5511226830cf32025ce43e", extractors=["entities", "topics"])

# see also https://www.textrazor.com/types
label_textrazor = {
"Place": "GEO",
"Person": "PERSON",
"Organisation" : "ORG",
"Company": "ORG",
"Disease": "KEYWORD",
"Species": "KEYWORD",
"AnatomicalStructure": "KEYWORD",
"Drug": "KEYWORD",
"ChemicalSubstance": "KEYWORD",
"Work": "PRODUCT",
"EthnicGroup": "KEYWORD",
"Currency": "CURRENCY",
"URL": "URL",
"Automobile": "PRODUCT",
"Ship": "PRODUCT",
"Aircraft": "PRODUCT",
"Event": "EVENT",
"Sport": "KEYWORD",
"Holiday": "EVENT",
"CelestialBody": "KEYWORD", # could also be GEO?
"Language": "KEYWORD",
"Activity": "EVENT",
"Food": "PRODUCT",
"TopicalConcept": "KEYWORD",
"TimePeriod": "DATE",
"Biomolecule": "KEYWORD",
"Date": "DATE",
"Flag": "KEYWORD"
}

def convert_labels(labels):
	for label in labels:
		if label in label_textrazor:
			return label_textrazor[label]
	if not labels:
		return "KEYWORD"
	else:
		print "textrazor:", labels
		return labels[0]

def extract_entities(text, lang):
	entities = {}
	try:
		rp = client.analyze(text)
		for entity in rp.entities():
			key = entity.id
			value = convert_labels(entity.dbpedia_types)
			entities[key] = value
	except TextRazorAnalysisException as e:
		print "TextRazor API:", e

	return entities