# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree

label_temis = {
"/Entity/Person":"PERSON", 
"/Entity/Location": "GEO", 
"/Entity/Company" : "ORG", 
"/Entity/Organisation":"ORG", 
"/Entity/Media" : "ORG", 
"/Entity/Function": "FUNCTION"}

def convert_label(label):
	prefix="/".join(label.split("/")[:3])
	if prefix in label_temis:
		return label_temis[prefix]
	else:
		return label

def extract_entities(text, lang):
	entities={}
	headers = {"content-type": "text/plain; charset=UTF-8", "accept-language": lang}
	rp = requests.post('http://193.28.233.173:8091/temis/v1/annotation/annotate/AS-test.xml?container=none', headers=headers, data=text.encode("utf-8"))
	xml = ElementTree.fromstring(rp.content)
	for tag in xml.findall(".//knowledge[@name='Knowledge']//annotation"):
		if "name" in tag.attrib:
			key = unicode(tag.attrib["name"])
			value = convert_label(tag.attrib["type"]) 
			entities[key] = value
	return entities			