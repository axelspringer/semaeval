# -*- coding: utf-8 -*-
import requests
import json
from ... import config

if "basistech" in config.engines:
	host = config.engines["basistech"]["host"]
	labels = config.engines["basistech"]["labels"]


def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "basistech:", label
		return label


def extract_entities(text, lang):
	entities = {}
	headers = {'content-type': 'application/json', 'accept' : 'application/json' }

	# see RLP-AppDev-Guide.pdf
	data = {'text': text,
			'languageDetection': {"language": "UNKNOWN","strategy": "SINGLE"},
			'resultTypes': ["DEFAULT_NAMED_ENTITY"]}
	rp = requests.post(host + "/rws/services/doc/processText", headers=headers, data=json.dumps(data))
	try:
		result = rp.json()

		types = result["regions"][0]["resultAccess"]["NamedEntityTypeString"]
		lemmas = result["regions"][0]["resultAccess"]["NormalizedNamedEntity"]

		for lemma, entity_type in zip(lemmas, types):
			key = lemma
			entities[key] = convert_label(entity_type)
	except Exception as e:
		print "BasisTech API Error:", e
		print "BasisTech Response:", rp.content
	return entities