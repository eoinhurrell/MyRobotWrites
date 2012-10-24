import robotsettings
import urllib, json

for line in open(robotsettings.backup_name,'r'):
	js = json.loads(line)
	#print js.keys()
	if int(js['note_count']) != 0:
		if 'body' in js.keys():
			print unicode(js['body'])

