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

	# To activate co-reference resolution one must add "NAMED_ENTITY_CHAIN_ID"
	# to the resultTypes (see chapter 5.10, RLP-AppDev-Guide.pdf)
	data = {'text': text,
			'languageDetection': {"language": "UNKNOWN","strategy": "SINGLE"},
			'resultTypes': ["DEFAULT_NAMED_ENTITY", "NAMED_ENTITY_CHAIN_ID"]}
	rp = requests.post(host + "/rws/services/doc/processText", headers=headers, data=json.dumps(data))
	try:
		result = rp.json()

		types = result["regions"][0]["resultAccess"]["NamedEntityTypeString"]
		lemmas = result["regions"][0]["resultAccess"]["NormalizedNamedEntity"]
		chain_ids = result["regions"][0]["resultAccess"]["NamedEntityChainId"]

		results = zip(lemmas, types, chain_ids)

		for lemma, entity_type, chain_id in results:
			# take the first element of the results triple where chain_id is pointing to.
			key = results[chain_id][0]
			entities[key] = convert_label(entity_type)
	except Exception as e:
		print "BasisTech API Error:", e
		print "BasisTech Response:", rp.content
	return entities