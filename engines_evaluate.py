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
from collections import OrderedDict

document = "article3181485.yml"

example_dir = "input/english/"
result_dir = "output/english/"

engines = [meaningcloud, bitext, textrazor, temis, semantria, repustate, linguasys, alchemy, retresco, simple]

engines = [retresco, simple]

# see http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

def collect_results(text, engines):
	results = {}
	pool = {}

	for engine in engines:

		results[engine]={}

		entities = engine.extract_entities(text)
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

	with open(example_dir + document,"r") as f:
		data = ordered_load(f, yaml.SafeLoader)

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
							
			document_name=document.split(".")[0] # remove suffix from document name
			engine_name = engine.__name__.split(".")[1]
			with open(result_dir + document_name + "_"+ engine_name + ".yml", "w") as out: 
				# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
				ordered_dump(data_engine, out, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)			 		 






