#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
dir = "/Users/amaier1/Documents/semeval/german/NLP-Vergleich/NLP_Evaluation/data/judgements/"
test_set = "AS_NLP_testset.txt"

ids = set()
for filename in os.listdir(dir):
	ids.add(filename.split("_")[0])

with open(test_set,"r") as input, open("urls_welt_de.txt","w") as output:
	for line in input:
		# print line.strip()
		tokens = line.split()
		id = tokens[0]
		url = tokens[1].replace(".xmli",".html")
		if id in ids:
			print url
			output.write(url.replace(".xmli",".html") + "\n")
