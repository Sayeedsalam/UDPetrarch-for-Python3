#encoding=utf-8

# from EventCoder import EventCoder
# import json
#
# coder = EventCoder()
#
# article = json.load(open("test_article_173_2.json"))
#
# events = coder.encode(open("test_article_173_2.json").read())
#
# print events

from UDParser import UDParser
import pickle



parser = UDParser(lang="es")

print parser.parse("Ucrania ratificó un acuerdo radical con la Unión Europea el martes.")

print pickle.dumps(parser)