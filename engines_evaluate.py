#!/usr/bin/env python
# -*- coding: utf-8 -*-
import engines.simple as simple
import engines.temis as temis
import engines.retresco as retresco
import engines.alchemy as alchemy
import engines.repust as repustate
import engines.linguasys as linguasys
import engines.semant as semantria
import engines.txtrazor as textrazor
import engines.bitext as bitext
import engines.meaningcloud as meaningcloud

import yaml

def dedup_list(input_list):
	output=[]
	for elem in input_list:
		if elem not in output:
			output.append(elem)	
	return output		

english_example = "examples/english/article4216441.yml"

engines = [meaningcloud, bitext, textrazor, temis, semantria, repustate, linguasys, alchemy, retresco, simple]

if __name__ == '__main__':

	with open(english_example,"r") as f:
		data = yaml.load(f)

		text = data["text"]

		for engine in engines:
			entities = engine.extract_entities(text)
			print ""
			print engine.__name__
			for key,value in entities.items(): print value,key

	# pool = dedup_list(entities_temis.items() 
	#	+ entities_nltk.items() 
	#	+ entities_retresco.items()
	#	+ entities_alchemy.items())
	# print pool






