#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import nltk
from xml.etree import ElementTree

label_temis = {"/Entity/Person":"PERSON", "/Entity/Location": "GEO"}
label_nltk = {"GPE":"GEO"}
label_retresco = {"geos":"GEO", "persons":"PERSON"}

def convert_label_temis(label):
	prefix="/".join(label.split("/")[:3])
	if prefix in label_temis:
		return label_temis[prefix]
	else:
		return label

def convert_label_nltk(label):
	if label in label_nltk:
		return label_nltk[label]
	else:
		return label

def convert_label_retresco(label):
	if label in label_retresco:
		return label_retresco[label]
	else:
		return label					

# see http://timmcnamara.co.nz/post/2650550090/extracting-names-with-6-lines-of-python-code
def extract_entities_nltk(text):
	entities={}
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			# see http://stackoverflow.com/questions/26352041/nltk-entity-extraction-difference-from-nltk-2-0-4-to-nltk-3-0
			if hasattr(chunk, "label"):
				key=' '.join(c[0] for c in chunk.leaves())
				value=convert_label_nltk(chunk.label())
				entities[key]=value 
	return entities 

def extract_entities_temis(text):
	entities={}
	headers = {"content-type": "text/plain; charset=UTF-8"}
	rp = requests.post('http://193.28.233.173:8091/temis/v1/annotation/annotate/AS-test.xml?container=none', headers=headers, data=text)
	xml = ElementTree.fromstring(rp.content)
	for tag in xml.findall(".//knowledge[@name='Knowledge']//annotation"):
		key = unicode(tag.attrib["name"])
		value = convert_label_temis(tag.attrib["type"]) 
		entities[key] = value
	return entities	

def extract_entities_retresco(text):
	entities={}
	data={}
	data["body"]=text
	rp = requests.post('http://pideas-dh04/enrich?userkey=1A5319EA-4AA0-48D8-8010-7952863851D0', data=json.dumps(data))
	result = rp.json()
	categories = result["result"]["keywords"].items()
	for category in categories:
		value = category[0]
		for element in category[1]:
			key = element["lemma"]
			entities[key] = convert_label_retresco(value)
	return entities		


def dedup_list(input_list):
	output=[]
	for elem in input_list:
		if elem not in output:
			output.append(elem)	
	return output		


test_text = "Let's try to talk with Angela Merkel at the Brandenburger Tor in Berlin: 'äh, öh, üh, ßß'."

print test_text

entities_retresco = extract_entities_retresco(test_text)
entities_nltk = extract_entities_nltk(test_text.decode("utf-8"))
entities_temis = extract_entities_temis(test_text)

print ""
print "Python NLTK"
for key,value in entities_nltk.items(): print value,key
print ""
print "Temis"
for key,value in entities_temis.items(): print value,key
print ""
print "Retresco"
for key,value in entities_retresco.items(): print value,key


pool = dedup_list(entities_temis.items() + entities_nltk.items() + entities_retresco.items())
# print pool






