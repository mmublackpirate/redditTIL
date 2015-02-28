#!/usr/bin/env python
import urllib2 , json,webbrowser,sys,os,textwrap,urlparse
import oauth2 as oauth
from twitter import *

url="http://www.reddit.com/r/todayilearned/new/.json"
consumer_key = "hS9IbNdSl09PkXDFGWgM1vd9T"
consumer_secret = "hFRSUpHkhOp9hKnqGICYE94z80NVx8kMhlhNfNIoFoDW2sH66A"

def tweet_status(tweet):
    MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("redditTIL",consumer_key,consumer_secret,
                MY_TWITTER_CREDS)

    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    twitter = Twitter(auth=OAuth(
        oauth_token, oauth_secret,consumer_key,consumer_secret))
    twitter.statuses.update(status = tweet)



try:
    result = urllib2.urlopen(url)
    data = json.loads(result.read())
    children = data['data']['children']
    print  "n = next TIL,  o = open link in browser,t = tweet TIL,  q = quit"
    print "."*100+"\n"

    for js in children:
        title = js['data']['title'].replace("TIL that",'',1).replace("TIL:",'',1) \
                                                            .replace("TIL of",'',1).replace("TIL",'',1).lstrip().capitalize()
        url = js['data']['url']
        for ti in textwrap.wrap(title,100):
            print ti

        print "\n"

        while True:
            choice=raw_input('n = next TIL,o = open link,t = tweet TIL,q = quit?')

            if choice == 'n':
                print "."*100+"\n"
                break;
            elif choice == 'o':
                 try:
                    savout = os.dup(1)
                    os.close(1)
                    os.open(os.devnull, os.O_RDWR)
                    webbrowser.open_new_tab(url)
                 finally:
                    os.dup2(savout, 1)
                
            elif choice == 'q':
                sys.exit(0)
               
            elif choice == 't':
                tweet_status(title+"\n"+url)
            
except  urllib2.URLError, e:
    print "An error occured! It's not your fault"

