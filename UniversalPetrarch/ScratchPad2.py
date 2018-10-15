text = "1 Ukraine Ukraine PROPN NNP Number=Sing 2 nsubj _ _\n 2 ratified ratify VERB VBD Mood=Ind|Tense=Past|VerbForm=Fin 0 root _ _\n 3 a a DET DT Definite=Ind|PronType=Art 5 det _ _\n 4 sweeping sweeping ADJ JJ Degree=Pos 5 amod _ _\n 5 agreement agreement NOUN NN Number=Sing 2 dobj _ _\n 6 with with ADP IN _ 9 case _ _\n 7 the the DET DT Definite=Def|PronType=Art 9 det _ _\n 8 European european PROPN NNP Number=Sing 9 compound _ _\n 9 Union Union PROPN NNP Number=Sing 5 nmod _ _\n 10 on on ADP IN _ 11 case _ _\n 11 Tuesday Tuesday PROPN NNP Number=Sing 2 nmod _ SpaceAfter=No\n 12 . . PUNCT . _ 2 punct _ SpacesAfter=\n"

import json
import os
text = open("test_article_173_2.json", "r").read()
article = json.loads(text)
text = article['sentences'][0]['parse_sentence']
print text.split("\n")

#print os.linesep