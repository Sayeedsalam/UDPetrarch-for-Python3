import networkx as nx
from pprint import pprint

from UDParser import UDParser

parser = UDParser(lang="en")


results = parser.parse("Nine injured in accident.").split("\n")

print (len(results))

pprint(results)







