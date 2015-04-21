# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree

from ... import config

if "temis" in config.engines:
	host = config.engines["temis"]["host"]
	labels = config.engines["temis"]["labels"]
	plan = config.engines["temis"]["endpoint"]


def convert_label(label):
	prefix = "/".join(label.split("/")[:3])
	if prefix in labels:
		return labels[prefix]
	else:
		print "temis",label
		return label


def extract_entities(text, lang):
	entities = {}
	headers = {"content-type": "text/plain; charset=UTF-8", "accept-language": lang}
	rp = requests.post(host + '/temis/v1/annotation/annotate/' + plan + '?container=none', headers=headers, data=text.encode("utf-8"))
	xml = ElementTree.fromstring(rp.content)
	for tag in xml.findall(".//knowledge[@name='Knowledge']//annotation"):
		if "name" in tag.attrib:
			key = unicode(tag.attrib["name"])
			value = convert_label(tag.attrib["type"]) 
			entities[key] = value
	return entities			