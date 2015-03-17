#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import utils_yaml
import math

import matplotlib.pyplot as pyplot

result_dir = "output/en/"

def precision(tp,tn,fp,fn):
	return tp/float(tp + fp)

def recall(tp,tn,fp,fn):
	return tp/float(tp + fn)	

def f1_score(precision, recall):
	return 2.0 * precision * recall / float(precision + recall)

def mean(l):
	return sum(l) / float(len(l))

# Sample standard deviation
def sstddev(l):
	n = len(data)
	if n < 2:
		raise ValueError('Sample standard deviation requires at least two data points')

	xbar = mean(l)
	svariance = 1.0/(n-1) * sum((x-xbar)**2 for x in l)
	return math.sqrt(svariance)

def plot_results():
	data = yaml.load(open("results.yml"))

	plot_data = []

	for category in ["PERSON","GEO","ORG","KEYWORD"]:

		for engine, results in data.items():
			if category in results:
				plot_data.append((engine, category, results[category]["f1_score"], results[category]["precision"], results[category]["recall"]))

	pyplot.style.use('ggplot')
	for number, category in enumerate(["PERSON", "GEO", "ORG", "KEYWORD"]):
		index = 0
		labels = []
		data_x1 = []
		data_y1 = []
		data_y2 = []
		data_y3 = []

		for label, title, y1, y2, y3 in sorted(plot_data, key=lambda item: item[2], reverse=True):
			if title == category:
				index += 1
				labels.append(label)
				data_x1.append(index)
				data_y1.append(y1)
				data_y2.append(y2)
				data_y3.append(y3)

		data_x2 = [x + 0.25 for x in data_x1]
		data_xlabel = [x + 0.375 for x in data_x1]
		data_x3 = [x + 0.50 for x in data_x1]
		pyplot.subplot(4,1,number + 1)
		pyplot.title(category)
		pyplot.xticks(data_xlabel, labels)
		# for color style, see here https://tonysyu.github.io/mpltools/auto_examples/style/plot_ggplot.html
		y1 = pyplot.bar(data_x1, data_y1, width=0.25, color=pyplot.rcParams['axes.color_cycle'][1])
		y2 = pyplot.bar(data_x2, data_y2, width=0.25, color=pyplot.rcParams['axes.color_cycle'][2])
		y3 = pyplot.bar(data_x3, data_y3, width=0.25, color=pyplot.rcParams['axes.color_cycle'][3])
		pyplot.legend((y1[0],y2[0],y3[0]),("F1 score", "precision", "recall"))


	pyplot.tight_layout()
	pyplot.show()


if __name__ == '__main__':

	precisions = {}
	recalls = {}
	f1_scores = {}

	for filename in os.listdir(result_dir):
		if filename.endswith(".yml"):
			with open(result_dir + filename, "r") as f:
				data = utils_yaml.ordered_load(f, yaml.SafeLoader)
				
				engine = filename.split(".")[0].split("_")[1]

				if engine not in precisions:
					precisions[engine] = {}
					recalls[engine] = {}
					f1_scores[engine] = {}

				for category in ["PERSON","GEO","ORG","KEYWORD"]:

					if category not in precisions[engine]:
						precisions[engine][category] = []
						recalls[engine][category] = []
						f1_scores[engine][category] = []
					
					tp = 0
					tn = 0
					fp = 0
					fn = 0

					for entities in (data[category]["detected"] + data[category]["undetected"]):
						for key,value in entities.items():
							if key == "TP": tp += 1
							if key == "TN": tn += 1
							if key == "FP": fp += 1
							if key == "FN": fn += 1
					try: 		
						prec = precision(tp,tn,fp,fn)
						rec = recall(tp,tn,fp,fn)
						f1 = f1_score(prec, rec)

						precisions[engine][category].append(prec)
						recalls[engine][category].append(rec)
						f1_scores[engine][category].append(f1)
					except ZeroDivisionError:
						pass	

	results = {}
	for engine,categories in precisions.items():
		if engine not in results:
			results[engine] = {}
		for category, values in categories.items():
			if values:
				prec_avg = mean(values)
				if category not in results[engine]:
					results[engine][category] = {"precision" : prec_avg}
				else:
					results[engine][category]["precision"] = prec_avg
	for engine,categories in recalls.items():
		if engine not in results:
			results[engine] = {}
		for category, values in categories.items():
			if values:
				recall_avg = mean(values)
				if category not in results[engine]:
					results[engine][category] = {"recall" : recall_avg}
				else:
					results[engine][category]["recall"] = recall_avg
	for engine,categories in f1_scores.items():
		if engine not in results:
			results[engine] = {}
		for category, values in categories.items():
			if values:
				f1_avg = mean(values)
				if category not in results[engine]:
					results[engine][category] = {"f1_score" : f1_avg}
				else:
					results[engine][category]["f1_score"] = f1_avg
	path = "results.yml"
	print "Storing file: ", path
	with open(path, "w") as out:
		# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
		utils_yaml.ordered_dump(results, out, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)		

	plot_results()

		




					



				


