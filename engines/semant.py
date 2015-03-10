# -*- coding: utf-8 -*-

import semantria
import uuid
import time

serializer = semantria.JsonSerializer()
session = semantria.Session("1e9489fd-9870-45c3-9cd2-0890aafad3fa", "02f32cbb-0e0a-4150-a93a-b36d28b99cfd", serializer, use_compression=True)

label_semantria = {
"Place":"GEO", 
"Person":"PERSON", 
"Company":"ORG",
"Job Title":"FUNCTION"}

def convert_label(label):
	if label in label_semantria:
		return label_semantria[label]
	else:
		return label

def extract_entities(text):
	entities = {}
	doc = {"id": str(uuid.uuid4()).replace("-", ""), "text": text}

	status = session.queueDocument(doc)
   	if status == 202:
   		results = []

		while len(results) < 1:
   			time.sleep(2)
   			# get processed documents
   			status = session.getProcessedDocuments()
   			results.extend(status)
   			
   		for data in results:
   			for entity in data["entities"]:
   				key = entity['title']
   				value = convert_label(entity['entity_type'])
   				entities[key] = value	

   	return entities			
