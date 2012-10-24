#Robot Writer
A python script to generate somewhat human posts on Tumblr.

##Requires
[Python Oauth2 module](http://)
##Quickstart
* Fill in all the details in _robotsettings.sample.json_
* Rename _robotsettings.sample.json_ to _robotsettings.json_
* Run robotwriter.py, it will automatically go through Oauth authorization

##The configuration file
The _robotsettings.sample.json_ is the sample configuration file that must be filled out before using the robot to generate Tumblr posts.

* "backup_name": "robot.backup.log", 
* "blog": "YOURSITE.tumblr.com", 
* "consumer_key": "YOUR_CONSUMER_KEY", 
* "consumer_secret": "YOUR_CONSUMER_SECRET_KEY", 
* "hostname": "www.YOURSITE.com",  
* "state": "queue", 
* "tags": "lit,prose,AI,computer-generated",
* "posts_per_run" : 15