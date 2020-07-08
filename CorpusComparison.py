import json
import os
import sys
import time

from googletrans import Translator
from SentenceEncoding import encode_sentence

import requests
from nltk import sent_tokenize
from mtranslate import translate



def download_and_translate():

    translator = Translator(service_urls=[

      'translate.google.com',
    ])
    spanish_data_file = open("Spanish_articles.tsv", "r")

    relevant_articles = []
    skip_count = 0

    if os.path.exists("counter.txt"):
        skip_count = int(open("counter.txt", "r").read())
        print (skip_count)
        relevant_articles = json.load(open("translated_articles.json", "r"))

    i = 0

    print ("Skip Count is "+str(skip_count))
    lines = spanish_data_file.readlines()[skip_count:]
    for line in lines:

        link = line.split("\t")[0]
        type = line.split("\t")[1] #can be Irrelevant, Political or Non-Political
        sub_type = None
        try:
            sub_type = line.split("\t")[2] #represents Root Code in CAMEO ontology
        except IndexError:
            sub_type = "Irrelevant"
        if not link.startswith("http"):
            continue
        print (link)
        response = requests.get(link)

        article = json.loads(response.content)["data"]

        #print article
        article["sub_type"] = sub_type
        #not processing any irrelevant article
        if type in ["Political", "Non-Political"]:
            print("Relevent article, processing for next steps")
            # sentences = sent_tokenize(article["content"]) #spliting up into sentences
            # article["sentences"] = sentences
            # trans_sents = []
            # trans_sents.append(translator.translate(sentences, dest="en"))
            #adding english translation to the corresponding object
            try:
               print ("========")
               print(article["content"])
               article["translation"] = translate(article["content"].encode("utf-8"), to_language="en")

            except (TypeError, ValueError) as e:

               print("Inside Exception handling")
               json.dump(relevant_articles, open("translated_articles.json", "w+"))
               counter_file = open("counter.txt", "w+")
               counter_file.write(str(skip_count))
               counter_file.close()
               sys.exit(1)


            # article["translated_sents"] = trans_sents
            # article.pop("content")
            relevant_articles.append(article)
            print (len(relevant_articles))
            time.sleep(10)

        else:
            print "Skipping an irrelevant article"

        skip_count += 1



    #saving the articles in file for future processing
    json.dump(relevant_articles, open("translated_articles.json", "w+"))


download_and_translate()


articles = json.load(open("translated_articles.json", "r"))
from UDParser import UDParser
from UniversalPetrarch.EventCoder import EventCoder
from pprint import pprint

from nltk import sent_tokenize

parser_en = UDParser()
parser_es = UDParser(lang="es")
event_coder_es = EventCoder(config_file="PETR_config_es.ini")
event_coder_en = EventCoder()

coders = {"en": event_coder_en, "es": event_coder_es}
parsers = {"en": parser_en, "es": parser_es}

def parse_ud(corenlp_data, language = "en"):

    entries = corenlp_data["sentences"]


    for entry in entries:
        entry["parse_sentence"] = parsers[language].parse(entry['sentence'])

    return corenlp_data

def create_article(art, lang="english", content_key="translation"):
    article = {}
    article["type"] = "story"
    article["doc_id"] = art["_id"]
    article["head_line"] = art["title"]
    article["date_line"] = "Tue, 21 Jun 2017 03:52:15 GMT" #helpful to identify the role based on timeline
    article["sentences"] = []
    i = 1
    sentences = sent_tokenize(art[content_key], lang)
    for sentence in sentences:
        sentence_node = {}
        sentence_node["sentence_id"] = i
        i += 1
        sentence_node["sentence"] = sentence
        article["sentences"].append(sentence_node)

    return article

def encode_sentence(article, language="en"):

    events = coders[language].encode_dict(article)
    event_set = []

    for i in range(1, len(events['dummy_001']['sents'])+1):

        if events is not None and 'events' in events['dummy_001']['sents'][i]:
            event_set.append(events['dummy_001']['sents'][i])
            i += 1
        else:
            event_set.append({})

    return event_set

def process(article):
    art_es = create_article(article, content_key="content")
    art_en = create_article(article, content_key="translation")

    art_es = parse_ud(art_es, language="es")
    art_en = parse_ud(art_en, language="en")
    try:
        events_es = encode_sentence(art_es,language="es")
        events_en = encode_sentence(art_en,language="en")
        return events_en, events_es

    except (KeyError, TypeError):
        return



from multiprocessing import Pool

workers = Pool(4)

# dup_articles = []
#
# for i in range(10):
#     for article in articles:
#         dup_articles.append(article)
#
# print ("Number of articles: ", str(len(dup_articles)))




#
# for article in dup_articles:
#     if article["sub_type"] is not "Irrelevant":

start = time.time()
events_tuples = workers.map(process, articles)

print(len(events_tuples))
workers.close()
end = time.time()

for event_en, event_es in  events_tuples:
    print event_en, event_es


json.dump(events_tuples, open("events_es_en.json", "w+"))

print (end-start)

