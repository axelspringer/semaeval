# -*- coding: utf-8 -*-
import nltk

label_nltk = {
	"GPE": "GEO",
	"LOCATION": "GEO",
	"ORGANIZATION": "ORG",
	"PERSON": "PERSON",
	"FACILITY": "KEYWORD",
	"GSP": "ORG"}


def convert_label(label):
	if label in label_nltk:
		return label_nltk[label]
	else:
		print "simple:",label
		return label


# see http://timmcnamara.co.nz/post/2650550090/extracting-names-with-6-lines-of-python-code
def extract_entities(text, lang):
	entities={}
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			# see http://stackoverflow.com/questions/26352041/nltk-entity-extraction-difference-from-nltk-2-0-4-to-nltk-3-0
			if hasattr(chunk, "label"):
				key=' '.join(c[0] for c in chunk.leaves())
				value=convert_label(chunk.label())
				entities[key]=value 
	return entities 		