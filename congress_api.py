"""
URL Parameters

Parameter	Description
congress	105-115
chamber	house or senate
type	introduced, updated, passed or major
"""
from collections import Counter
import json
from pandas import DataFrame
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
	return adjs #.most_common(3)

def get_noun(blob):
	"""
	Given textblob obj
	Return counter for pos: nouns
	"""
	noun = [blob.tags[i][0] for i in range(len(blob.tags))
	if blob.tags[i][1].startswith('NN')]
	nouns = Counter(noun)
	return nouns #.most_common(3)

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

def get_words_from_house_bill(bill_title):
	"""
	Given bill (str)
	Returns 3 pos counters
	"""
	blob = get_blob(bill_title)
	a = get_adj(blob)
	n = get_noun(blob)
	v = get_verb(blob)
	return a, n, v


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
	Return lists containing word counters for each party
	"""
	# initialize counters
	d_a = Counter() # dem - adj
	d_n = Counter() # dem - noun
	d_v = Counter() # dem - verb
	r_a = Counter() # rep - adj
	r_n = Counter() # rep - noun
	r_v = Counter() # rep - verb
	i_a = Counter() # ind - adj
	i_n = Counter() # ind - noun
	i_v = Counter() # ind - verb
	d = []
	r = []
	i = []
	# get bills
	bills = json['results'][0]['bills']
	for i in range(len(bills)):
		if bills[i]['sponsor_party'] == 'D':
			# get words
			a, n, v = get_words_from_house_bill(bills[i]['title'])
			# update counters
			d_a, d_n, d_v = d_a + a, d_n + n, d_v + v
		elif bills[i]['sponsor_party'] == 'R':
			# get words
			a, n, v = get_words_from_house_bill(bills[i]['title'])
			# count
			# update counters
			r_a, r_n, r_v = r_a + a, r_n + n, r_v + v
		else: # party == I
			# get words
			a, n, v = get_words_from_house_bill(bills[i]['title'])
			# count
			# update counter
			i_a, i_n, i_v = i_a + a, i_n + n, i_v + v
	# add counters to list
	d.extend((d_a, d_n, d_v))
	r.extend((r_a, r_n, r_v))
	#i.extend((i_a, i_n, i_v))
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

# function to take list of pos counters for each party
# return df of word, freq, pos, party
def party_words_to_df(k, party='Dem'):
	# k is list of counter objects
	cols = ['Word', 'Frequency']
	# ADJ
	df = DataFrame(k[0].most_common(5), columns=cols)
	df['Pos'] = ['Adj']*5
	df.set_index('Pos')
	df['Party'] = [party]*5
	df.set_index('Party')
	# NOUN
	df1 = DataFrame(k[1].most_common(5), columns=cols)
	df1['Pos'] = ['Noun']*5
	df1.set_index('Pos')
	df1['Party'] = [party]*5
	df1.set_index('Party')
	# VERB
	df2 = DataFrame(k[2].most_common(5), columns=cols)
	df2['Pos'] = ['Verb']*5
	df2.set_index('Pos')
	df2['Party'] = [party]*5
	df2.set_index('Party')
	# now we have 3 dfs
	# df, df1, df2
	df = df.append(df1, ignore_index=True)
	df = df.append(df2, ignore_index=True)
	return df

def json_to_df():
	#get_house_words()
	json = get_house_bills()
	d, r, i = get_party_words(json)
	#print('Democrat words: {0}'.format(str(d)))
	print()
	#print('Republican words: {0}'.format(str(r)))
	#print('Adjectives: {}'.format())
	#print('Nouns: {}'.format(d[1]))
	#print('Verbs: {}'.format(d[2]))
	# adj counter
	words_df = party_words_to_df(d)
	words_df = words_df.append(party_words_to_df(r, party='Rep')) 
	return words_df

if __name__ == '__main__':
	
	words = json_to_df()
	print(words.sort_values(['Frequency'], ascending=False))
	
	

	