#!/usr/bin/env python
# -*- coding: utf-8 -*-
from engine import simple
import engine.temis as temis
import engine.retresco as retresco
import engine.alchemy as alchemy
import engine.repust as repustate
import engine.linguasys as linguasys
import engine.semant as semantria
import engine.txtrazor as textrazor
import engine.bitext as bitext
import engine.meaningcloud as meaningcloud


test_text = u"Let's try to talk with Angela Merkel at the Brandenburger Tor in Berlin: 'äh, öh, üh, ßß'."
engines = [meaningcloud, bitext, textrazor, temis, semantria, repustate, linguasys, alchemy, retresco, simple]

def run(text, lang):
    for engine in engines:
        entities = engine.extract_entities(text, lang)
        print ""
        print engine.__name__
        for key, value in entities.items(): print value,key

if __name__ == '__main__':
    print test_text
    run(test_text, "en")
