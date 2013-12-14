import json
from operator import itemgetter
#import robotsettings
#backup = robotsettings.backup_name
backup = 'robot.backup.log'

count = 0
selected = []

for line in open(backup, 'r'):
    js = json.loads(line)
    #print js.keys()
    if int(js['note_count']) != 0:
        if 'body' in js.keys():
            count += 1
            selected.append(js)
selected = sorted(selected, key=itemgetter('note_count'))
fout = open('popular.json', 'w')
json.dump(selected, fout, sort_keys=False, indent=4)
print 'Count: ' + str(count)
