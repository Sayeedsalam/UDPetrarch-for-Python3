import json
from UDParser import UDParser
from UniversalPetrarch.EventCoder import EventCoder
from pprint import pprint

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
    pprint(article)
    #print article
    events = event_coder.encode_dict(article)
    if events is not None and 'events' in events['dummy_001']['sents'][1]:
        return events['dummy_001']['sents'][1]
    else:
        return {}



event_dict = encode_sentence("The European Union or individual States must not take over from economic operators, but public authorities must define the rules and objectives which enable the economy to develop in a sustainable fashion.")
pprint(event_dict)
for key in event_dict['triplets']:
    print event_dict['triplets'][key]["triple"][0].text