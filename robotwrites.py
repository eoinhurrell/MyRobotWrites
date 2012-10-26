#!/usr/bin/python

import oauth2 as oauth
import random,sys,os,urllib,urllib2,json,urlparse,getopt

config_file = "robotsettings.json"
bookpath = os.path.join(os.getcwd(),'books')
settings = {}

stopword = "\n"
stopsentence = (".", "!", "?",) #for counting sentences
sentencesep	 = "\n"

def loadSettings():
	"""Loads script settings from a json file into memory. Exits on invalid JSON in file

	    Raises:
	        IOError: if the file does not exist
	"""	
	global settings
	global bookpath
	json_data=open(config_file)
	try:
		settings = json.load(json_data)
	except ValueError as e:
		print "The configuration file " + config_file + " exists but is not valid JSON. Either correct the error or revert to a working veersion"
		print "Error details: " + str(e)
		sys.exit(1)
	bookpath = os.path.join(os.getcwd(),settings['source'])
	
def saveSettings():
	"""Saves script settigns from memory to a json file

	"""	
	global settings
	fout = open(config_file,'w')
	fout.write(json.dumps(settings, sort_keys=True, indent=4))
	fout.close()

def authorize():
	"""Authorizes your app with Tumblr for an access token using Oauth(consumer key, consumer secret)
		Adapted directly from https://github.com/simplegeo/python-oauth2 3 stage auth example
		Raises:
			Exception on invalid response from server 
	"""	
	global settings
	consumer_key = settings['consumer_key']
	consumer_secret = settings['consumer_secret']
	
	request_token_url = 'http://www.tumblr.com/oauth/request_token'
	access_token_url = 'http://www.tumblr.com/oauth/access_token'
	authorize_url = 'http://www.tumblr.com/oauth/authorize'
	
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)
	
	# Step 1: Get a request token. This is a temporary token that is used for 
	# having the user authorize an access token and to sign the request to obtain 
	# said access token.
	
	resp, content = client.request(request_token_url, "GET")
	if resp['status'] != '200':
	    raise Exception("Invalid response %s." % resp['status'])
	
	request_token = dict(urlparse.parse_qsl(content))
	# Step 2: Redirect to the provider. Since this is a CLI script we do not 
	# redirect. In a web application you would redirect the user to the URL
	# below.
	
	print "Go to the following link in your browser:"
	print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
	print 
	# After the user has granted access to you, the consumer, the provider will
	# redirect you to whatever URL you have told them to redirect to. You can 
	# usually define this in the oauth_callback argument as well.
	accepted = 'n'
	while accepted.lower() == 'n':
	    accepted = raw_input('Have you authorized me? (y/n) ')
	oauth_verifier = raw_input('What is the Oauth_Verifer parameter? ')
	
	# Step 3: Once the consumer has redirected the user back to the oauth_callback
	# URL you can request the access token the user has approved. You use the 
	# request token to sign this request. After this is done you throw away the
	# request token and use the access token returned. You should store this 
	# access token somewhere safe, like a database, for future use.
	token = oauth.Token(request_token['oauth_token'],
	    request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)
	
	resp, content = client.request(access_token_url, "POST")
	access_token = dict(urlparse.parse_qsl(content))
	
	settings['oauth_token'] = access_token['oauth_token']
	print access_token['oauth_token']
	settings['oauth_token_secret'] = access_token['oauth_token_secret']
	print access_token['oauth_token_secret']

def tumblrPost(body,tags=None,title=None):
	"""Generates a short nonsense text based on the input book.

	    Args:
	       book (str): the location of the corpus to use to generate the post.
	    Returns:
	        (str) A string, five sentences long, of nonsense generated from the corpus 
	    Raises:
	        Error: if the file does not exist
	"""	
	global settings
	post_address = "http://api.tumblr.com/v2/blog/"+settings['blog']+"/post"
	data = {"type":"text","state":settings['state'],"body" : body, "oauth_token":settings['oauth_token']}
	if tags != None:
		data['tags'] = str(tags)
	if title != None:
		data['title'] = str(title)
	consumer = oauth.Consumer(settings['consumer_key'], settings['consumer_secret'])
	token = oauth.Token(settings['oauth_token'], settings['oauth_token_secret'])
	client = oauth.Client(consumer,token)
	resp, content = client.request(post_address, "POST", urllib.urlencode(data))
	js = json.loads(content)
 	if js['meta']['status'] != 201: #something wrong
		print js['meta']['msg']
		print js

def generatePost(book):
	"""Generates a short nonsense text based on the input book.

	    Args:
	       book (str): the location of the corpus to use to generate the post.
	    Returns:
	        (str) A string of nonsense generated from the corpus. Number of sentences is defined by settings['max_sentences'] 
	    Raises:
	        Error: if the file does not exist
	"""
	global stopword
	global stopsentence
	global sentencesep
	# GENERATE TABLE
	w1 = stopword
	w2 = stopword
	table = {}

	for line in open(book):
		for word in line.split():
			if word[-1] in stopsentence:
				table.setdefault( (w1, w2), [] ).append(word[0:-1])
				w1, w2 = w2, word[0:-1]
				word = word[-1]
			table.setdefault( (w1, w2), [] ).append(word)
			w1, w2 = w2, word
	# Mark the end of the file
	table.setdefault( (w1, w2), [] ).append(stopword)

	# GENERATE SENTENCE OUTPUT		
	maxsentences = 5
	if 'max_sentences' in settings:
		maxsentences = settings['max_sentences']

	w1 = stopword
	w2 = stopword
	sentencecount = 0
	sentence = []
	post = []

	#note replace lessthan with the symbol
	# I was having trouble with aspn commets
	while sentencecount < maxsentences:
		newword = random.choice(table[(w1, w2)])
		if newword == stopword: sys.exit()
		if newword in stopsentence:
			if sentencecount != 0:
				post.append(" ".join(sentence) + newword)
			#print "%s%s" % (" ".join(sentence), newword)
			sentence = []
			sentencecount += 1
		else:
			sentence.append(newword)
		w1, w2 = w2, newword
	return " ".join(post)

def randomPostToTumblr():
	"""Chooses a random corpus, generates tumblr tags and a tumblr post, posts to tumblr
	
	"""	
	txt_files = filter(lambda x: x.endswith('.txt'), os.listdir(bookpath))
	book = random.choice(txt_files)
	TAGS = settings['tags'] + ",inspired by " + book.replace('-','by')[:book.find(".")+1]
	if(book.find("-") != -1):
		TAGS = TAGS + "," + book[:book.find("-")-1]
		TAGS = TAGS + "," + book[book.find("-")+2:book.find(".")]
	tumblrPost(generatePost(os.path.join(bookpath,book)), tags=TAGS)
	
def randomPostToScreen():
	"""Prints a post generated from a randomly chosen corpus to the screen

	"""
	txt_files = filter(lambda x: x.endswith('.txt'), os.listdir(bookpath))
	book = random.choice(txt_files)
	print generatePost(os.path.join(bookpath,book))
	print '----------------------------'

if __name__ == '__main__':
	print_posts = False
	silent = False
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hpsc:",["print","silent","config="])
	except getopt.GetoptError:
		print 'Usage: robotwriter.py [-p] [--config <configfile.json>]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: robotwriter.py [-p] [--config <configfile.json>]'
			sys.exit()
		elif opt in ("-c", "--config"):
			try:
			   with open(arg) as f: pass
			except IOError as e:
				print "Configuration file " + arg + " does not exist, exiting"
				sys.exit(1)
			config_file = arg
		elif opt in ("-p", "--print"):
			print_posts = True
		elif opt in ("-s", "--silent"):
			silent = True
	loadSettings()
	if "oauth_token" not in settings.keys():
		authorize()
	for x in xrange(settings['posts_per_run']):
		if not print_posts:
			randomPostToTumblr()
		else:
			randomPostToScreen()
	if not silent:
		print str(settings['posts_per_run']) + " post(s) successfully generated."
	saveSettings()
