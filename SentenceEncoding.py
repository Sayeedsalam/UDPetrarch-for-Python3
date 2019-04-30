import json
from UDParser import UDParser
from UniversalPetrarch.EventCoder import EventCoder
from pprint import pprint

from nltk import sent_tokenize

parser = UDParser()
event_coder = EventCoder()

def parse_ud(corenlp_data):

    entries = corenlp_data["sentences"]


    for entry in entries:
        entry["parse_sentence"] = parser.parse(entry['sentence'])

    return corenlp_data

def create_dummy_article(sentences):
    article = {}
    article["type"] = "story"
    article["doc_id"] = "dummy_001"
    article["head_line"] = "dummy headline"
    article["date_line"] = "Tue, 21 Jun 2017 03:52:15 GMT" #helpful to identify the role based on timeline
    article["sentences"] = []
    i = 1
    for sentence in sentences:
        sentence_node = {}
        sentence_node["sentence_id"] = i
        i += 1
        sentence_node["sentence"] = sentence
        article["sentences"].append(sentence_node)

    return article

def encode_sentence(sentence):
    article = create_dummy_article(sentence)
    article = parse_ud(article)
    pprint(article)
    #print article
    events = event_coder.encode_dict(article)
    event_set = []

    for i in range(1, len(sentence)+1):
        if events is not None and 'events' in events['dummy_001']['sents'][i]:
            event_set.append(events['dummy_001']['sents'][i])
            i += 1
        else:
            event_set.append({})

    return event_set



summary = "Assailants detonated an explosive device at an oil holding pool along the Cano Limon - Covenas pipeline in Convencion municipality, North Santander department, Colombia. As a result of the blast, the pool was damaged and local residents evacuated the area. This was one of four holding pools attacked in the area on this day. No group claimed responsibility for the incident; however, sources attributed the attack to National Liberation Army of Colombia (ELN)."


summary_sentences = sent_tokenize(summary)
print(type(summary_sentences))

events = encode_sentence(summary_sentences)

for event_dict in events:
    pprint(event_dict)

    for key in event_dict["events"]:

        print event_dict['triplets'][key]["triple"][0]
        print event_dict['triplets'][key]["triple"][1]
        print event_dict['triplets'][key]["triple"][2]