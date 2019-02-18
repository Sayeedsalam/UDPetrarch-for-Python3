from SentenceEncoding import encode_sentence
import json

en_file = open("articles_500/europarl-v7.es-en.en", "r")
es_file = open("articles_500/europarl-v7.es-en.es", "r")

pairs_with_events = []

limit = -1

translation_map = {}
count = 0
for line in en_file:
    if limit == 0:
        break
    limit -= 1

    es_line = es_file.readline()
    translation_map[line] = es_line
    count += 1
    if len(translation_map) % 10000 == 0:
        print count

print "Translation Map build complete"

event_pairs = json.load(open("event_pairs.json", "r"), encoding="utf-8")

print len(event_pairs)

event_pairs_v2 = []

for pair in event_pairs:
    try:
        es_line = translation_map[pair["en"]]
        if es_line is None or len(es_line) == 0:
            print "Translation Not found"
            continue

        events = encode_sentence(pair["en"])

        sentence_tuple = {"en": pair["en"], "es": es_line, "events": events}

        event_pairs_v2.append(sentence_tuple)
    except KeyError, k:
        print k.message



json.dump(event_pairs_v2, open("pairs_with_events.json", "w+"))


print len(event_pairs_v2)




