#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
from itertools import groupby

import yaml
import matplotlib.pyplot as pyplot

import utils_yaml

result_dir = "../output/"

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

	pyplot.style.use('ggplot')
	for number, category in enumerate(["PERSON", "GEO", "ORG", "KEYWORD", "TOTAL"]):
		index = 0
		labels = []
		data_x1 = []
		data_y1 = []
		data_y2 = []
		data_y3 = []
		data_y1_err = []
		data_y2_err = []
		data_y3_err = []

		for label, title, y1, y1_error, y2, y2_error, y3, y3_error in sorted(data, key=lambda item: item[2], reverse=True):
			if title == category:
				index += 1
				labels.append(label)
				data_x1.append(index)
				data_y1.append(y1)
				data_y2.append(y2)
				data_y3.append(y3)
				data_y1_err.append(y1_error)
				data_y2_err.append(y2_error)
				data_y3_err.append(y3_error)

		data_x2 = [x + 0.25 for x in data_x1]
		data_xlabel = [x + 0.375 for x in data_x1]
		data_x3 = [x + 0.50 for x in data_x1]
		pyplot.subplot(5, 1, number + 1)
		pyplot.title(category)
		#pyplot.xticks(data_xlabel, ["" for x in data_x1])
		pyplot.xticks(data_xlabel, labels)
		# for color style, see here https://tonysyu.github.io/mpltools/auto_examples/style/plot_ggplot.html
		# see also https://stackoverflow.com/questions/16776761/color-each-errorbar-with-different-color
		y1 = pyplot.bar(data_x1, data_y1, yerr=data_y1_err, width=0.25, color=pyplot.rcParams['axes.color_cycle'][1], ecolor="grey")
		y2 = pyplot.bar(data_x2, data_y2, yerr=data_y2_err, width=0.25, color=pyplot.rcParams['axes.color_cycle'][2], ecolor="grey")
		y3 = pyplot.bar(data_x3, data_y3, yerr=data_y3_err, width=0.25, color=pyplot.rcParams['axes.color_cycle'][3], ecolor="grey")
		pyplot.legend((y1[0], y2[0], y3[0]), ("F1 score", "precision", "recall"))

		# pyplot.xticks(data_xlabel, ["" for x in data_x1])
		# cell_y1 = ["%0.2f" % i for i in data_y1]
		# cell_y2 = ["%0.2f" % i for i in data_y2]
		# cell_y3 = ["%0.2f" % i for i in data_y3]
		# col_widths = [0.1 for i in data_y1]
		#
		# cell_text = [cell_y1, cell_y2, cell_y3]
		# pyplot.table(loc='bottom',
		# 			 cellText=cell_text,
		# 			 colLabels=labels,
		# 			 rowLabels=("F1 score", "precision", "recall"),
		# 			 colWidths=col_widths)


	pyplot.tight_layout()
	pyplot.show()

def load_articles(prefix):
	articles = []
	dir = result_dir + prefix + "/"

	for filename in os.listdir(dir):
		if filename.endswith(".yml"):
			with open(dir + filename,"r") as f:
				data = utils_yaml.ordered_load(f, yaml.SafeLoader)
				articles.append(data)
	return articles


if __name__ == '__main__':

	articles = load_articles("en")

	statistics = {}
	for article in articles:
		engine = article["engine"]

		if engine not in statistics:
			statistics[engine] = {}

		for category in ["PERSON","GEO","ORG","KEYWORD"]:

			if category not in statistics[engine]:
				statistics[engine][category] = []

			tp = 0
			tn = 0
			fp = 0
			fn = 0

			for entities in (article[category]["detected"] + article[category]["undetected"]):
				for key,value in entities.items():
					if key == "TP": tp += 1
					if key == "TN": tn += 1
					if key == "FP": fp += 1
					if key == "FN": fn += 1
			try:
				prec = precision(tp,tn,fp,fn)
				rec = recall(tp,tn,fp,fn)
				f1 = f1_score(prec, rec)

				statistics[engine][category].append((f1, prec, rec))
			except ZeroDivisionError:
				pass

	results = []
	for engine, categories in statistics.items():
		for category, values in categories.items():
			result = [engine, category]
			if values:
				# see https://stackoverflow.com/questions/19339/a-transpose-unzip-function-in-python-inverse-of-zip
				stats = [(mean(data), sstddev(data)) if len(data) > 1 else (0, 0) for data in zip(*values)]
				for avg, sstd in stats:
					result.append(avg)
					result.append(sstd)
			else:
				result.extend([0, 0, 0, 0, 0, 0])
			results.append(result)

	totals = []
	# see https://stackoverflow.com/questions/773/how-do-i-use-pythons-itertools-groupby
	for key, group in groupby(sorted(results), lambda x: x[0]):

		results_by_key = list(group)

		total = (key, "TOTAL",
				mean([result[2] for result in results_by_key]),
				mean([result[3] for result in results_by_key]),
				mean([result[4] for result in results_by_key]),
				mean([result[5] for result in results_by_key]),
				mean([result[6] for result in results_by_key]),
				mean([result[7] for result in results_by_key]))
		totals.append(total)

	results.extend(totals)

	path = "results.yml"
	print "Storing file: ", path
	with open(path, "w") as out:
		# see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
		utils_yaml.ordered_dump(results, out, Dumper=yaml.SafeDumper, width=200, encoding="utf-8", allow_unicode=True)

	plot_results()
