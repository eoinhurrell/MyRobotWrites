from tumblr import Api
import robotsettings
import random
import sys
import os

cwpath=robotsettings.cwpath
BLOG=robotsettings.blog
USER=robotsettings.user
PASSWORD=robotsettings.password
TAGS=robotsettings.tags
STATE=robotsettings.state
stopword = "\n" # Since we split on whitespace, this can never be a word
stopsentence = (".", "!", "?",) # Cause a "new sentence" if found at the end of a word
sentencesep	 = "\n" #String used to seperate sentences

def makePost(title,body):
	global posttimes
	global BLOG
	global USER
	global PASSWORD
	global TAGS
	global STATE
	api = Api(BLOG,USER,PASSWORD)
	try:
		post = api.write_regular(title,body,tags=TAGS,state=STATE)
		print "Published: ", post['url']
	except:
		print "Published okay, tumblr complained though!"	#tumblr for some reason complains


def genPost(book):
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
	maxsentences	= 5

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

def post():
	global TAGS
	global cwpath
	txt_files = filter(lambda x: x.endswith('.txt'), os.listdir(cwpath+'/books'))
	book = random.choice(txt_files)
	TAGS = TAGS + ",inspired by " + book.replace('-','by')[:book.find(".")+1]
	if(book.find("-") != -1):
		TAGS = TAGS + "," + book[:book.find("-")-1]
		TAGS = TAGS + "," + book[book.find("-")+2:book.find(".")]
	print TAGS	
	makePost("",genPost(cwpath + "/books/"+ book))
	
#each week, generate 15 posts
for x in xrange(15):
	post()
	TAGS=robotsettings.tags
