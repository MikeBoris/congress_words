"""
URL Parameters

Parameter	Description
congress	105-115
chamber	house or senate
type	introduced, updated, passed or major
"""

import json
import requests
from ApiKey import params

def proAPI():
	key = params['api_key']
	#url = "https://api.propublica.org/congress/v1/115/senate/members.json"
	# get recent bills
	url = "https://api.propublica.org/congress/v1/115/house/bills/introduced.json"
	r = requests.get(url,headers={"X-API-KEY":key})
	return r.content
	#return r.content

def print_data(data):
	r = json.loads(data)
	bills = r['results'][0]['bills']
	for i in range(len(bills)):
		print(bills[i]['number'])
		#print(bills[i]['introduced_date'])
		print(bills[i]['title'])
		print(bills[i]['sponsor_party'])
		print("")



'''

construct tables (df) for the top pos:
	topAdj:
	ID, adj1, adj2, adj3

	topNoun:
	ID, noun1, noun2, noun3

	topVerb:
	ID, verb1, verb2, verb3


'''
from textblob import textblob
from collections import Counter

#--- some functions for extracting text metrics ----------------

def get_blob(text):
	"""
	Given text (string)
	Returns textblob object for further text processing
	"""
	return TextBlob(text)

def get_adj(blob):
	"""
	Given textblob obj
	Return counter for pos: adjectives
	"""
	adj = [blob.tags[i][0] for i in range(len(blob.tags)) 
	if blob.tags[i][1] == 'JJ']
	adjs = Counter(adj)
	return adjs.most_common(3)

def get_noun(blob):
	"""
	Given textblob obj
	Return counter for pos: nouns
	"""
	noun = [blob.tags[i][0] for i in range(len(blob.tags))
	if blob.tags[i][1].startswith('NN')]
	nouns = Counter(noun)
	return nouns.most_common(3)

def get_verb(blob):
	"""
	Given textblob obj
	Return counter for pos: verb
	"""
	verb = [blob.tags[i][0] for i in range(len(blob.tags))
	if blob.tags[i][1].startswith('VB')]
	verbs = Counter(verb)
	return verbs
	



	
		adjectives
		nouns
		verbs



if __name__ == '__main__':
	data = proAPI()
	print_data(data)