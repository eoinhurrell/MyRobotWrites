import json
#import robotsettings
#backup = robotsettings.backup_name
backup = 'robot.backup.log'

count = 0
for line in open(backup, 'r'):
    js = json.loads(line)
    #print js.keys()
    if int(js['note_count']) != 0:
        if 'body' in js.keys():
            count += 1
            print js
            #print js['body'].encode('utf-8')
print 'Count: ' + str(count)
