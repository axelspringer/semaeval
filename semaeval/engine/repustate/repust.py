# -*- coding: utf-8 -*-

import repustate

from ... import config

if "repustate" in config.engines:
	key = config.engines["repustate"]["key"]
	labels = config.engines["repustate"]["labels"]


def convert_label(label):
	if label in labels:
		return labels[label]
	else:
		print "repustate:",label
		return label


def extract_entities(text, lang):
	entities = {}
	try:
		client = repustate.Client(api_key=key)
		# see https://www.repustate.com/docs/
		response = client.entities(text=text.encode("utf-8"), lang=lang)

		for k, v in response['entities'].items():
			entities[k] = convert_label(v)
	except repustate.RepustateAPIError, e:
		print "Repustate API Error:", e, "No entities extracted!"

	return entities
