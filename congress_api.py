"""
URL Parameters

Parameter	Description
congress	105-115
chamber	house or senate
type	introduced, updated, passed or major
"""
from collections import Counter
import json
import requests
from textblob import TextBlob
from ApiKey import params

def get_house_bills(key='api_key'):
	"""
	Given API key, sends get request to propublica's Congress API
	Returns results as json
	"""
	key = params[key]
	#url = "https://api.propublica.org/congress/v1/115/senate/members.json"
	# get recent bills
	url = "https://api.propublica.org/congress/v1/115/house/bills/introduced.json"
	r = requests.get(url,headers={"X-API-KEY":key})
	return json.loads(r.content)

'''

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

def get_bill_title(json):
	"""
	Given json return object
	Returns list of bill titles
	"""
	bills = json['results'][0]['bills']
	return [bills[i]['title'] for i in range(len(bills))]

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

#--- MAIN GET_WORDS ---------------------------#

def get_house_words():
	json = get_house_bills()
	title_list = get_bill_title(json)
	for i in title_list:
		blob = get_blob(i)
		a = get_adj(blob)
		n = get_noun(blob)
		v = get_verb(blob)
		print(a, n, v)

def get_words_from_house_bill(bill):
	title_list = [bills[i]['title'] for i in range(len(bills))]
	for i in title_list:
		blob = get_blob(i)
		a = get_adj(blob)
		n = get_noun(blob)
		v = get_verb(blob)
		print(a, n, v)




#--- PARTY STATS ------------------------------#

# make sure we're pulling in party sponsor
# counter for each party
# 
def get_party_sponsor(json):
	"""
	Given json return object
	Return list of bill sponsors ('D' or 'R')
	"""	
	bills = json['results'][0]['bills']
	return [bills[i]['sponsor_party'] for i in range(len(bills))]

def get_party_words(json):
	"""
	Given json object w/ bill titles
	Return word counters for each party
	"""
	# initialize counters
	d = Counter()
	r = Counter()
	i = Counter()
	# get bills
	bills = json['results'][0]['bills']
	for i in bills:
		if bills[i]['sponsor_party'] == 'D':
			# get words
			# count
			# update counter
		elif bills[i]['sponsor_party'] == 'R':
			# get words
			# count
			# update counter
		else: # party == I
			# get words
			# count
			# update counter
	return d, r, i





'''
construct tables (df) for the top pos:
	topAdj:
	ID, adj1, adj2, adj3

	topNoun:
	ID, noun1, noun2, noun3

	topVerb:
	ID, verb1, verb2, verb3


'''

if __name__ == '__main__':
	
	get_house_words()