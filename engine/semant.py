# -*- coding: utf-8 -*-

import semantria
import uuid
import time

import json

serializer = semantria.JsonSerializer()
session = semantria.Session("1e9489fd-9870-45c3-9cd2-0890aafad3fa", "02f32cbb-0e0a-4150-a93a-b36d28b99cfd", serializer, use_compression=True)

# see http://support.semantria.com/customer/portal/articles/838464-entity-extraction
label_semantria = {
"Place":"GEO", 
"Person":"PERSON", 
"Company":"ORG",
"Job Title":"FUNCTION",
"Quote":"QUOTE"}

# in semantria the configuration is stored on the server and has an id
# You can get the config id for a language via
# for key in session.getConfigurations(): print key["language"],key["config_id"]
lang_semantria = {
"ko": "bc399d26-9b33-4f00-a7fe-cb343f8a3756",
"it": "72bad261-4240-4cf6-b3e3-5fb27bc9c619",
"jp": "ebda1e20-d666-4533-9614-1e3d02bcb22c",
"fr": "aa2141a3-f990-4296-a82b-daf7f2ee9d9e",
"pt": "5aa3cc21-7c82-463a-8307-de815573e4ed",
"en": "10781931-a7cc-4ff8-aae1-5bda0a7fcec9",
"ms": "d9f02606-f087-45e4-9643-77d0ddd4f4cc",
"de": "04854264-0288-420f-8954-104ab6cc5b1a",
"es": "bd5e9a9b-3772-460c-9fd3-3915ee9c95ec",
"zh": "2fc65284-5743-4ff4-b239-331ac9b03a7a",
}

def convert_label(label):
	if label in label_semantria:
		return label_semantria[label]
	else:
		return label

def convert_lang(lang):
	if lang in lang_semantria:
		return lang_semantria[lang]
	else:
		return lang

def extract_entities(text, lang):
	entities = {}
	doc = {"id": str(uuid.uuid4()).replace("-", ""), "text": text}
	config_id = convert_lang(lang)
	status = session.queueDocument(doc, config_id=config_id)
	if status == 202:
		results = []

		while len(results) < 1:
			time.sleep(2)
			# get processed documents (you have use the same config_id as for queuing!)
			status = session.getProcessedDocuments(config_id=config_id)
			results.extend(status)

		for data in results:
			for entity in data["entities"]:
				key = entity['title']
				value = convert_label(entity['entity_type'])
				entities[key] = value

	return entities
