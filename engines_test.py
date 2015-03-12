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


test_text = u"Let's try to talk with Angela Merkel at the Brandenburger Tor in Berlin: 'äh, öh, üh, ßß'."
engines = [meaningcloud, bitext, textrazor, temis, semantria, repustate, linguasys, alchemy, retresco, simple]

def run(text, lang):
    for engine in engines:
        entities = engine.extract_entities(text,lang)
        print ""
        print engine.__name__
        for key,value in entities.items(): print value,key

if __name__ == '__main__':
    print test_text
    run(test_text,"en")







