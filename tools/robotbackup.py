import robotsettings
import urllib2, json

fout = open(robotsettings.backup_name,'w')

info_address = "http://api.tumblr.com/v2/blog/"+robotsettings.hostname+"/info?api_key=" + robotsettings.authkey
posts_address = "http://api.tumblr.com/v2/blog/"+robotsettings.hostname+"/posts?api_key=" + robotsettings.authkey
total_posts = 9999
offset = 0 

#First get total posts
url = info_address
req = urllib2.Request(url)
f = urllib2.urlopen(req)
response = f.read()
f.close()
js = json.loads(response)
total_posts = int(js['response']['blog']['posts'])
print "Backing up " + js['response']['blog']['title'] + ", " + str(total_posts) + " posts."

while offset < total_posts:
	print str(offset) + "/" + str(total_posts)
	url = posts_address + "&offset=" + str(offset)
	req = urllib2.Request(url)
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	#write to file
	js = json.loads(response)
	for i in js['response']['posts']:
		out = json.dumps(i)
		fout.write(out+'\n')
	offset += 20
fout.close()