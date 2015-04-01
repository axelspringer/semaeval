# -*- coding: utf-8 -*-
import requests
import json
import yaml

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

host = config["host"]
labels = config["labels"]


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