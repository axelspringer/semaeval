# -*- coding: utf-8 -*-

import yaml
import repustate

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

key = config["key"]
labels = config["labels"]


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
