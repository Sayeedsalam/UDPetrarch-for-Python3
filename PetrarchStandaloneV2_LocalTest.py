from UniversalPetrarch.EventCoder import EventCoder
import json

from PhoenixConverter import PhoenixConverter

from PetrarchFormatter import PetrarchFormatter
from UDParser import UDParser
from pprint import pprint


MONGO_PORT="3154"
MONGO_USER="event_reader"
MONGO_PSWD="dml2016"
MONGO_SERVER_IP="172.29.100.16"
MONGO_PORT="3154"

# MONGO_COLLECTION = "processed_stories_ud"
# password = urllib.quote_plus(MONGO_PSWD)
# client = MongoClient('mongodb://'+MONGO_USER+':' + password + '@'+MONGO_SERVER_IP+":"+MONGO_PORT)
#
# db = client.event_scrape
#
#consumer = KafkaConsumer('petrarch_ud',bootstrap_servers='172.29.100.6:9092')

formatter = PhoenixConverter(geo_ip="149.165.168.205", geo_port="8080")

coder = EventCoder()

petr_converter = PetrarchFormatter()

# def get_info_from_mongo(id_str):
#     object_id = ObjectId(id_str)
#     article = db.stories.find_one({"_id": object_id})
#
#     if article is not None:
#         return article['source'], article['url']
#     else:
#         return None, None

parser = UDParser()

def parse_ud(corenlp_data):

    entries = corenlp_data["sentences"]
    ud_parser_data = {}

    for entry in entries:
        entry["parse_sentence"] = parser.parse(entry['sentence'])

    return corenlp_data

# for msg in consumer:
    #print msg
article_str = open("UniversalPetrarch/test_article_173_2.json").read()
try:
    corenlp_data = json.loads(article_str)
    corenlp_data = parse_ud(corenlp_data)

    #print corenlp_data



    event_dict = coder.encode_dict(corenlp_data)
    pprint(event_dict)
    #event_dict = coder.encode(msg.value)

    # formatted_dict = PETRwriter.pipe_output(event_dict)

    db_value = {}
    db_value['udpipe'] = corenlp_data
    #str_id = db_value['udpipe']['mongo_id']
    #source, url = get_info_from_mongo(str_id)

    additional_info = {"source": "TEST", "url": "ALPHA", "mongo_id": "TEST123"}

    events = formatter.format(event_dict, additional_info)

    print(("Number of events ", str(len(events))))

    #mongo_id = ObjectId(str_id)
    db_value['petrarch_ud'] = petr_converter.encode(event_dict)
    db_value['processed'] = "True"
    #db_value['ref_id'] = mongo_id


    #db.stories.update({"_id":mongo_id}, {"$set": db_value}, check_keys = False)

    #db.processed_stories_ud.insert(db_value, check_keys=False)

    for event in events:
        print("========")
        print(event)
        #db.phoenix_events_ud.insert(event, check_keys=False)

except Exception as e:
    print(("EXCEPTION ", str(e)))
    issue_article = {}
    issue_article['article'] = ""
    issue_article['issue'] = str(e)

    #db.issue_for_stories.insert(issue_article, check_keys=False)

