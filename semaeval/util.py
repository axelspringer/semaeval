#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaier1'

import os
import shutil
import argparse

folders = ["input/", "output/", "result/"]

# see https://stackoverflow.com/questions/185936/delete-folder-contents-in-python
def clean_storage(lang, dryrun=False):

	for folder in folders:
		folder_path = os.path.join(folder, lang)
		try:
			for the_file in os.listdir(folder_path):
				file_path = os.path.join(folder_path, the_file)
				if not dryrun:
					print "Deleting:", file_path
					if os.path.isfile(file_path):
						os.unlink(file_path)
					elif os.path.isdir(file_path):
						shutil.rmtree(file_path)
					else:
						print "Cannot delete unknown type of file."
		except OSError as ose:
			print ose



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Delete input, output and result documents used for evaluation of semantic engines')
	parser.add_argument("-l","--lang", type=str, help="Language of the text (two-letter code: en, de, fr, ...)", required=True)
	parser.add_argument("--no-dry-run", action="store_true", help="Delete files for real")

	args = parser.parse_args()
	folders = ["../input/","../output/","../result/"]

	if args.no_dry_run:
		print "Deleting files for real."
		clean_storage(args.lang)
	else:
		print "Dryrun mode. "
		clean_storage(args.lang, dryrun=True)