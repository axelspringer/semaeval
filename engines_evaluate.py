#!/usr/bin/env python
# -*- coding: utf-8 -*-
import engine.simple as simple
import engine.temis as temis
import engine.retresco as retresco
import engine.alchemy as alchemy
import engine.repust as repustate
import engine.linguasys as linguasys
import engine.semant as semantria
import engine.txtrazor as textrazor
import engine.bitext as bitext
import engine.meaningcloud as meaningcloud

import os
import yaml
import utils_yaml

input_dir = "input/en/"
output_dir = "output/en/"

engines = [meaningcloud, bitext, textrazor, temis, semantria, repustate, linguasys, alchemy, retresco, simple]

engines = [retresco, simple]

def collect_results(text, engines):
	results = {}
	pool = {}

	for engine in engines:

		results[engine]={}

		entities = engine.extract_entities(text, "en")
		print ""
		print engine.__name__
		for entity,category in entities.items(): 
			print category,entity

			if category in results[engine]:
				results[engine][category].add(entity)
			else:
				results[engine][category]=set([entity])
					
			if category in pool:
				pool[category].add(entity)
			else:
				pool[category]=set([entity])

	return (pool,results)			

if __name__ == '__main__':

	for filename in os.listdir(input_dir):
		if filename.endswith(".yml"):
			with open(input_dir + filename,"r") as f:
				data = utils_yaml.ordered_load(f, yaml.SafeLoader)

				text = data["text"]

				pool,results = collect_results(text, engines)

				for engine, categories in results.items():
					data_engine = data
					data_engine["info"]="TP: True Positive, TN: True Negative, FP: False Positive, FN: False Negative, X: Ignored"

					for category in ["PERSON","GEO","ORG","KEYWORD"]:
						data_engine[category] = {}
						
						if category in categories:
							entities = categories[category]	
						else:
							entities = []

						data_engine[category]["detected"] = []
						data_engine[category]["undetected"] = []
						
						for entity in entities:
							data_engine[category]["detected"].append({"FP":entity})
						if category in pool:
							for entity in pool[category].difference(entities):
								data_engine[category]["undetected"].append({"FN":entity})
									
					filename_prefix=filename.split(".")[0] # remove suffix from filename name
					engine_name = engine.__name__.split(".")[1]
					with open(output_dir + filename_prefix + "_"+ engine_name + ".yml", "w") as out: 
						# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
						utils_yaml.ordered_dump(data_engine, out, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)			 		 






