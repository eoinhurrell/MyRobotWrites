#Robot Writer
A python script to generate somewhat human posts on Tumblr.

##Requires
[Python Oauth2 module](https://github.com/simplegeo/python-oauth2)

##Quickstart
* Fill in all the details in "robotsettings.sample.json"
* Rename "robotsettings.sample.json" to "robotsettings.json"
* Place the source texts you want your posts to be made from in the "books" directory.
* To print to the screen run: 

    python robotwriter.py -p

* To post to Tumblr run 

    python robotwriter.py 

* Follow the Oauth authorisation instructions if prompted.


##The configuration file
The _robotsettings.sample.json_ is the sample configuration file that must be filled out before using the robot to generate Tumblr posts.

* "backup_name" 
The name of the backup file created by the backup tool
* "blog"
The Tumblr address of your Tumblr blog, e.g. "YOURSITE.tumblr.com" 
* "consumer_key"
The Oauth consumer key given to you by Tumblr for your application. You can generate one [by registering a Tumblr application](http://www.tumblr.com/oauth/register)
* "consumer_secret"
The Oauth consumer secret given to you by Tumblr for your application. You can generate one [by registering a Tumblr application](http://www.tumblr.com/oauth/register)
*"max_sentences"
The maximum number of sentences to generate. Default is 5
* "source" 
The directory containing your corpus files. Default is "books"
* "state"
The state the posts are put on Tumblr in. Tumblr posts can be queued, privately posted or saved as draft rather than just immediately published. Supported states are "published", "draft", "queue", "private". If you are creating more than one post per run "queue" is recommended.
* "tags": 
The tags Tumblr attaches to the posts.
* "posts_per_run"
Number of posts to generate every time the script is run



Additionally two other fields will be needed to post to Tumblr. These are Oauth token details, which you can add manually if you already have them, but the preferred method is to allow the script to generate and save these tokens:

* "oauth_token"
The Oauth token
* "oauth_token_secret"
The Oauth token secret


##The sources
In order to generate posts the system needs at least one plain-text document in its source folder. By default this folder is "books", but it can be changed using the 

##Optional command-line arguments
* -h : Prints the usage information.
* -p or --print : Prints posts.
* -s or --silent : Prints nothing to the screen, making it good for use with cron.
* -c <file> or --config <file> : use the settings details in <file>.

##The backup tool
Provided with the script is a backup tool (located in the "tools" folder). This is a simple tool that downloads all the posts on whatever tumblr blog is defined in the settings (the "blog" setting), into a file defined by the "backup" setting. It is run in the following way:

    python robotbackup.py

These posts are stored in JSON format according to the [Tumblr API details](http://www.tumblr.com/docs/en/api/v2#posts). They can easily be displayed using the backup reader like so:

    python robotbackupreader.py

