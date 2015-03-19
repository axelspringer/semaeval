# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree

label_linguasys = {
"person" : "PERSON", 
"location": "GEO",
"organisation": "ORG",
"administrative unit": "ORG",
"date" : "DATE",
"time" : "DATE",
"aspect" : "KEYWORD",
"abbreviation" : "KEYWORD"}

# conversion from ISO_639-1 to linguasys language codes (see https://nlp.linguasys.com/Languages)
lang_linguasys = {"en": "ENG"}

def convert_label(label):
	prefix="/".join(label.split("/")[:3])
	if prefix in label_linguasys:
		return label_linguasys[prefix]
	else:
		print "linguasys:",label
		return label

def convert_lang(lang):
	if lang in lang_linguasys:
		return lang_linguasys[lang]
	else:
		return lang

def extract_entities(text,lang):
	entities={}
	language = convert_lang(lang).upper()
	payload = {'subscription-key': 'a0fa546f85ca4bbfb55bab69aa2c5a4f', 'languageModelCode': language, 'bodyText': text}
	rp = requests.get('https://api.linguasys.com/storymapper/analyze', params=payload)
	xml = ElementTree.fromstring(rp.content)
	for tag in xml.findall(".//entity"):
		key = unicode(tag.attrib["fullName"])
		value = convert_label(tag.attrib["type"])
		entities[key] = value
	return entities