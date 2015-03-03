# -*- coding: utf-8 -*-

import repustate

# see also here: https://www.repustate.com/media/entities.txt
label_repustate = {"government.politician":"PERSON"}

def convert_label(label):
	if label in label_repustate:
		return label_repustate[label]
	else:
		return label

def extract_entities(text):
	entities = {}
	client = repustate.Client(api_key='317542394cddce0baf6b3ec698d92198e2b6e4a7')
	response = client.entities(text=text, lang="en")

	for k,v in response['entities'].items():
		key = k
		value = v
		entities[key] = convert_label(value)
	return entities
