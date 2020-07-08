# coding=utf-8

import json
from UDParser import UDParser
from UniversalPetrarch.EventCoder import EventCoder
from pprint import pprint

from nltk import sent_tokenize
import nltk
nltk.data.path.append("/Volumes/Untitled 2/Users/sayeed")

parser = UDParser(lang="en")
event_coder = EventCoder(config_file="PETR_config.ini")

def parse_ud(corenlp_data):

    entries = corenlp_data["sentences"]


    for entry in entries:
        entry["parse_sentence"] = parser.parse(entry['sentence'])
    print entry["parse_sentence"]

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


if __name__ == "__main__":

    summary = "The UN Security Council on Tuesday unanimously approved a United States’ resolution on the recent deal between the U.S. and the Afghan Taliban, a rare endorsement of an agreement with a militant group."
    print summary

    summary_sentences = sent_tokenize(summary)
    print(type(summary_sentences))

    events = encode_sentence(summary_sentences)

    for event_dict in events:
        pprint(event_dict)

        for key in event_dict["events"]:

            print event_dict['triplets'][key]["source_text"]
            print event_dict['triplets'][key]["verb_text"]
            print event_dict['triplets'][key]["target_text"]