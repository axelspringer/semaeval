#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

import yaml

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
import utils_yaml

input_dir = "input/en/"
store_dir = "output/"

engines = [meaningcloud, bitext, textrazor, temis, semantria, repustate, linguasys, alchemy, retresco, simple]

def collect_results(text, engines, lang):
	results = {}
	pool = {}

	for engine in engines:
		results[engine] = {}

		entities = engine.extract_entities(text, lang)
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

def detect_entities(articles, lang):
	# see http://stackoverflow.com/questions/998938/handle-either-a-list-or-single-integer-as-an-argument
	if type(articles) is not list: articles = [articles]

	outputs = []

	for article in articles:
		text = article["text"]

		pool,results = collect_results(text, engines, lang)

		for engine, categories in results.items():
			engine_name = engine.__name__.split(".")[1]
			print engine_name

			output = OrderedDict(article)

			output["engine"] = engine_name
			output["info"]="TP: True Positive, TN: True Negative, FP: False Positive, FN: False Negative, X: Ignored"

			for category in ["PERSON","GEO","ORG","KEYWORD"]:
				output[category] = {}

				if category in categories:
					entities = categories[category]
				else:
					entities = []

				output[category]["detected"] = []
				output[category]["undetected"] = []

				for entity in entities:
					output[category]["detected"].append({"FP":entity})
				if category in pool:
					for entity in pool[category].difference(entities):
						output[category]["undetected"].append({"FN":entity})
			outputs.append(output)

	return outputs

def store_articles(articles, prefix):
	dir = store_dir + prefix + "/"
	# create the directory if it does not yet exist
	# see http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
	try:
		os.makedirs(dir)
	except OSError:
		if not os.path.isdir(dir):
			raise

	# see http://stackoverflow.com/questions/998938/handle-either-a-list-or-single-integer-as-an-argument
	if type(articles) is not list: articles = [articles]

	for article in articles:
		filename_prefix = article["filename"].split(".")[0]  # remove suffix from filename name
		engine_name = article["engine"]
		path = dir + filename_prefix + "_"+ engine_name + ".yml"
		print "Storing file: ", path

		with open(path, "w") as out:
			# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
			utils_yaml.ordered_dump(article, out, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)

if __name__ == '__main__':
	articles = []

	for filename in os.listdir(input_dir):
		if filename.endswith(".yml"):
			with open(input_dir + filename,"r") as f:
				articles.append(utils_yaml.ordered_load(f, yaml.SafeLoader))

	articles_enriched = detect_entities(articles, "en")

	store_articles(articles_enriched, "en")






