# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import yaml
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

host = config["host"]
labels = config["labels"]


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
	rp = requests.post(host + '/temis/v1/annotation/annotate/AS-test.xml?container=none', headers=headers, data=text.encode("utf-8"))
	xml = ElementTree.fromstring(rp.content)
	for tag in xml.findall(".//knowledge[@name='Knowledge']//annotation"):
		if "name" in tag.attrib:
			key = unicode(tag.attrib["name"])
			value = convert_label(tag.attrib["type"]) 
			entities[key] = value
	return entities			