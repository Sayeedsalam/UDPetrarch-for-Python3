import json

import requests


def prepare_dataset():

    tranlsated_file = open("translated.txt", "r")

    articles_map = {}

    for line in tranlsated_file:
        key, article_json = line.split("\t")

        articles_map[key] = json.loads(article_json)

    spanish_file  = open("Spanish_articles.tsv", "r")

    relevant_articles = []

    for line in spanish_file:
        article_url, type = line.split("\t")[:2]

        article_id = article_url.split("id=")[1]

        print article_id

        if type is "Irrelevant":
            continue

        if article_id in articles_map:
            response = requests.get(article_url)

            article_es = json.loads(response.content)["data"]

            articles_map[article_id]["content_es"] = article_es["content"]

            relevant_articles.append(articles_map[article_id])

    json.dump(relevant_articles, open("parallel_corpus.json", "w+"))

    print("Saved Articles: "+ len(relevant_articles))