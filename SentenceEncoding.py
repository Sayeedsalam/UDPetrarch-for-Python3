import json
from UDParser import UDParser
from UniversalPetrarch.EventCoder import EventCoder

parser = UDParser()
event_coder = EventCoder()

def parse_ud(corenlp_data):

    entries = corenlp_data["sentences"]


    for entry in entries:
        entry["parse_sentence"] = parser.parse(entry['sentence'])

    return corenlp_data

def create_dummy_article(sentence):
    article = {}
    article["type"] = "story"
    article["doc_id"] = "dummy_001"
    article["head_line"] = "dummy headline"
    article["date_line"] = "Tue, 21 Jun 2017 03:52:15 GMT" #helpful to identify the role based on timeline
    article["sentences"] = []
    sentence_node = {}
    sentence_node["sentence_id"] = 1
    sentence_node["sentence"] = sentence
    article["sentences"].append(sentence_node)

    return article

def encode_sentence(sentence):
    article = create_dummy_article(sentence)
    article = parse_ud(article)
    print article
    return event_coder.encode_dict(article)



print encode_sentence("Ukraine ratified a sweeping agreement with the European Union on Tuesday.")

