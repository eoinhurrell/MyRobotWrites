#!/usr/bin/python

import oauth2 as oauth
import random,sys,os,urllib,urllib2,json,urlparse,getopt

config_file = "../robotsettings.json"
settings = {}

fout = None

info_address = "http://api.tumblr.com/v2/blog/"
posts_address = "http://api.tumblr.com/v2/blog/"
blog_name = "Unknown"
blog_total_posts = 0
backup_offset = 0 

def loadSettings():
	"""Loads script settings from a json file into memory. Exits on invalid JSON in file

	    Raises:
	        IOError: if the file does not exist
	"""	
	global settings
	global fout
	json_data=open(config_file)
	try:
		settings = json.load(json_data)
	except ValueError as e:
		print "The configuration file " + config_file + " exists but is not valid JSON. Either correct the error or revert to a working veersion"
		print "Error details: " + str(e)
		sys.exit(1)
	fout = open(settings['backup_name'],'w')

def getBlogInfo():
	global blog_total_posts
	global blog_title
	global info_address
	data = {"oauth_token":settings['oauth_token']}
	consumer = oauth.Consumer(settings['consumer_key'], settings['consumer_secret'])
	token = oauth.Token(settings['oauth_token'], settings['oauth_token_secret'])
	client = oauth.Client(consumer,token)
	resp, content = client.request(info_address, "POST", urllib.urlencode(data))
	js = json.loads(content)
	blog_total_posts = int(js['response']['blog']['posts'])
	blog_title = js['response']['blog']['title']
	
def getTwentyPosts():
	global settings
	global backup_offset
	global posts_address
	data = {"offset":backup_offset,"oauth_token":settings['oauth_token']}
	consumer = oauth.Consumer(settings['consumer_key'], settings['consumer_secret'])
	token = oauth.Token(settings['oauth_token'], settings['oauth_token_secret'])
	client = oauth.Client(consumer,token)
	resp, content = client.request(posts_address, "POST", urllib.urlencode(data))
	js = json.loads(content)
 	if js['meta']['status'] != 201 and js['meta']['status'] != 200: #something wrong
		print js['meta']['msg']
		print js
	for i in js['response']['posts']:
		out = json.dumps(i)
		fout.write(out+'\n')
	backup_offset += 20

if __name__ == '__main__':
	loadSettings()
	info_address  = info_address  + settings['blog'] + "/info?api_key="+settings['consumer_key']
	posts_address = posts_address + settings['blog'] + "/posts?api_key="+settings['consumer_key']
	if "oauth_token" not in settings.keys():
		authorize()
	getBlogInfo()
	print "Backing up " + blog_title + ", " + str(blog_total_posts) + " posts."
	while backup_offset < blog_total_posts:
		getTwentyPosts()
	print "Backup complete."
	fout.close()

