from SentenceEncoding import encode_sentence
import json

en_file = open("articles_500/europarl-v7.es-en.en", "r")
es_file = open("articles_500/europarl-v7.es-en.es", "r")

out_file = open("articles_500/event_with_pairs_v1.txt", "a+")
pairs_with_events = []

limit = -1

count = 0
for line in en_file:
    if limit == 0:
        break
    limit -= 1

    es_line = es_file.readline()
    #print line
    #print es_line
    count += 1
    if count % 1000 == 0:
        print count
        open("counter.txt","w+").write(str(count))
    try:
        events = encode_sentence(line)

    except Exception, e:
        continue



    if len(events) != 0:
        pair = {"en": line, "es": es_line.encode("utf-8"), "events": events}
        pairs_with_events.append(pair)
        #print "Pair Added"
        pair_str = json.dumps(pair)
        out_file.write(pair_str+"\n")
        out_file.flush()


print len(pairs_with_events)
  
json.dump(pairs_with_events, open("event_pairs.json", "w+"), encoding="utf-8")




