#!/usr/bin/env python
import urllib2,json,webbrowser,sys,os,textwrap,urlparse
from twitter import *

url="http://www.reddit.com/r/todayilearned/new/.json"

# I don't care about the key!

consumer_key = "hS9IbNdSl09PkXDFGWgM1vd9T"
consumer_secret = "hFRSUpHkhOp9hKnqGICYE94z80NVx8kMhlhNfNIoFoDW2sH66A"

def tweet_status(tweet):
    MY_TWITTER_CREDS = os.path.expanduser('~/.redditTIL_credentials')
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("redditTIL",consumer_key,consumer_secret,
                MY_TWITTER_CREDS)

    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    twitter = Twitter(auth=OAuth(
        oauth_token, oauth_secret,consumer_key,consumer_secret))
    twitter.statuses.update(status = tweet)


""" getTerminalSize()
 - get width and height of console
 - works on linux,os x,windows,cygwin(windows)
"""

__all__=['getTerminalSize']


def getTerminalSize():
   import platform
   current_os = platform.system()
   tuple_xy=None
   if current_os == 'Windows':
       tuple_xy = _getTerminalSize_windows()
       if tuple_xy is None:
          tuple_xy = _getTerminalSize_tput()
          # needed for window's python in cygwin's xterm!
   if current_os == 'Linux' or current_os == 'Darwin' or  current_os.startswith('CYGWIN'):
       tuple_xy = _getTerminalSize_linux()
   if tuple_xy is None:
       print "default"
       tuple_xy = (80, 25)      # default value
   return tuple_xy

def _getTerminalSize_windows():
    res=None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _getTerminalSize_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
       import subprocess
       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       cols=int(output[0])
       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       rows=int(output[0])
       return (cols,rows)
    except:
       return None


def _getTerminalSize_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])



if __name__ == "__main__":
    try:
        sizex,sizey=getTerminalSize()
        result = urllib2.urlopen(url)
        data = json.loads(result.read())
        children = data['data']['children']
        print  "n = next TIL,  o = open link in browser,t = tweet TIL,  q = quit"
        print "."*sizex+"\n"
        
        for js in children:
            title = js['data']['title'].replace("TIL that",'',1).replace("TIL:",'',1) \
                                                            .replace("TIL of",'',1).replace("TIL",'',1).lstrip().capitalize()
            url = js['data']['url']

            print title + "\n"

            while True:
                choice=raw_input('n = next TIL,o = open link,t = tweet TIL,q = quit? ')

                if choice == 'n':
                    print "."*sizex+"\n"
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
                    tweet = title + "\n" +url
                    if len(tweet) > 140:
                        if len(title) > 140:
                           print "Your tweet is exceeding 140 characters. Try another one!"
                        else:
                           tweet = title
                           tweet_status(tweet)
                           print ""
                    else:
                        tweet_status(tweet)
                        print ""

    except  urllib2.URLError, e:
        print "An error occured! It's not your fault"

