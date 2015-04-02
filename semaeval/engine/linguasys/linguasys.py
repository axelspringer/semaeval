# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree

# see https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
import yaml
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = yaml.load(open(os.path.join(__location__, "config.yml"), "r"))

key = config["key"]
labels = config["labels"]
langs = config["langs"]


def convert_label(label):
	prefix="/".join(label.split("/")[:3])
	if prefix in labels:
		return labels[prefix]
	else:
		print "linguasys:",label
		return label


def convert_lang(lang):
	if lang in langs:
		return langs[lang]
	else:
		return lang


def extract_entities(text, lang):
	# Linguasys has a limit (officially of 16kB, I found 12000 chars) when using a GET request (TODO: switch to POST)
	text = text[:12000]
	entities = {}
	language = convert_lang(lang).upper()
	payload = {'subscription-key': key, 'languageModelCode': language, 'bodyText': text}
	rp = requests.get('https://api.linguasys.com/storymapper/analyze', params=payload)

	try:
		xml = ElementTree.fromstring(rp.content)
		for tag in xml.findall(".//entity"):
			k = unicode(tag.attrib["fullName"])
			v = convert_label(tag.attrib["type"])
			entities[k] = v
	except ElementTree.ParseError as pe:
		print "Linguasys API Error:", pe
		print "Linguasys Response:", rp.content
	return entities