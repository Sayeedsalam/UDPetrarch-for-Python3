import sys

from ufal.udpipe import Model, Pipeline, ProcessingError # pylint: disable=no-name-in-module

# In Python2, wrap sys.stdin and sys.stdout to work with unicode.
if sys.version_info[0] < 3:
    import codecs
    import locale
    encoding = locale.getpreferredencoding()
    sys.stdin = codecs.getreader(encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)

# # if len(sys.argv) < 4:
# #     sys.stderr.write('Usage: %s input_format(tokenize|conllu|horizontal|vertical) output_format(conllu) model_file\n' % sys.argv[0])
# #     sys.exit(1)
#
# sys.stderr.write('Loading model: ')
# model = Model.load("/Users/sxs149331/PycharmProjects/UniversalPetrarch-master/UniversalPetrarch/preprocessing/udpipe-1.0.0/model/english-ud-1.2-160523.udpipe")
# if not model:
#     sys.stderr.write("Cannot load model from file '%s'\n" % sys.argv[3])
#     sys.exit(1)
# sys.stderr.write('done\n')
#
# text = "Ukraine ratified a sweeping agreement with the European Union on Tuesday."
#
# pipeline = Pipeline(model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
# error = ProcessingError()
#
# # Read whole input
# #text = "This is a test."
#
# # Process data
# processed = pipeline.process(text, error)
# if error.occurred():
#     sys.stderr.write("An error occurred when running run_udpipe: ")
#     sys.stderr.write(error.message)
#     sys.stderr.write("\n")
#     sys.exit(1)
# sys.stdout.write(processed)



from UDParser import UDParser
import json
from UniversalPetrarch.EventCoder import EventCoder

parser = UDParser()

def parse_ud(corenlp_data):

    entries = corenlp_data["sentences"]
    ud_parser_data = {}

    for entry in entries:
        entry["parse_sentence"] = parser.parse(entry['sentence'])

    return corenlp_data

corenlp_data = json.load(open("UniversalPetrarch/test_article_173_2.json", "r"))

corenlp_data = parse_ud(corenlp_data)

print corenlp_data

coder = EventCoder()

print coder.encode_dict(corenlp_data)

#print parser.parse("Ukraine ratified a sweeping agreement with the European Union on Tuesday.")