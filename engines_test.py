#!/usr/bin/env python
# -*- coding: utf-8 -*-
import engines.simple as simple
import engines.temis as temis
import engines.retresco as retresco

def dedup_list(input_list):
	output=[]
	for elem in input_list:
		if elem not in output:
			output.append(elem)	
	return output		


test_text = "Let's try to talk with Angela Merkel at the Brandenburger Tor in Berlin: 'äh, öh, üh, ßß'."

print test_text

entities_retresco = retresco.extract_entities(test_text)
entities_nltk = simple.extract_entities(test_text.decode("utf-8"))
entities_temis = temis.extract_entities(test_text)

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






