# -*- coding: utf-8 -*-
__author__ = 'amaier1'

import yaml

config = yaml.load(open("config.yml", "r"))

folder_in = config["folder_input"]
folder_out = config["folder_output"]
engines = config["engines"]
categories = config["categories"]


