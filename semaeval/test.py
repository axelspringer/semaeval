#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Pool
from functools import partial
import time

import engine.simple as simple
import engine.temis as temis
import engine.retresco as retresco
import engine.basistech as basistech
import engine.netowl as netowl
import engine.alchemy as alchemy
import engine.repustate as repustate
import engine.linguasys as linguasys
import engine.semant as semantria
import engine.txtrazor as textrazor
import engine.bitext as bitext
import engine.meaningcloud as meaningcloud
import config


test_text = u"Let's try to talk with Angela Merkel at the Brandenburger Tor in Berlin: 'äh, öh, üh, ßß'."
# see http://stackoverflow.com/questions/14094802/construct-a-callable-object-from-a-string-representing-its-name-in-python
engines = [globals()[engine] for engine in config.engines.keys()]


# extract_function must be the first argument, because we will vary it with pool.map
# see also https://stackoverflow.com/questions/24755463/functools-partial-wants-to-use-a-positional-argument-as-a-keyword-argument
def extract(extract_function, text, lang):
	entities = extract_function(text, lang)
	print ""
	print extract_function.__module__
	for key, value in entities.items():
		print value, key


def run(text=test_text, lang="en", engines=engines):

	if not isinstance(text, unicode):
		print "Text is not a unicode string!"
		return

	print text

	# one process for each engine
	p = Pool(len(engines))

	# We need to use partial, since pool.map doesn't support functions with more than one argument
	# https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments/5443941
	partial_extract = partial(extract, text=text, lang=lang)

	start = time.time()
	# Because of the limitations of pool.map we cannot use a module as parameter to the run method
	# see https://stackoverflow.com/questions/27918547/cant-pickle-type-module-in-multiprocessing-pool
	# and https://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma
	# As a workaround we have to pass a function instead of a module or a class
	# see https://stackoverflow.com/questions/7016567/picklingerror-when-using-multiprocessing
	future = p.map_async(partial_extract, [engine.extract_entities for engine in engines])

	future.get(timeout=60)

	end = time.time()
	print end - start


if __name__ == '__main__':
	run()
