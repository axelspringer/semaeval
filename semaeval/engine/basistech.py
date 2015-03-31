# -*- coding: utf-8 -*-
import requests
import json

label_basistech = {
"PERSON": "PERSON",
"LOCATION": "GEO",
"TITLE": "FUNCTION",
"TEMPORAL:DATE": "DATE"}


def convert_label(label):
	if label in label_basistech:
		return label_basistech[label]
	else:
		print "basistech:",label
		return label


def extract_entities(text, lang):
	entities = {}
	headers = {'content-type': 'application/json', 'accept' : 'application/json' }

	# see RLP-AppDev-Guide.pdf
	data = {'text': text,
			'languageDetection': {"language": "UNKNOWN","strategy": "SINGLE"},
			'resultTypes': ["DEFAULT_NAMED_ENTITY"]}
	rp = requests.post('http://192.168.59.103:9020/rws/services/doc/processText', headers=headers, data=json.dumps(data))
	result = rp.json()

	types = result["regions"][0]["resultAccess"]["NamedEntityTypeString"]
	lemmas = result["regions"][0]["resultAccess"]["NormalizedNamedEntity"]

	for lemma, entity_type in zip(lemmas, types):
		key = lemma
		entities[key] = convert_label(entity_type)
	return entities