import sys
import tweepy
import json
import smtplib
import csv
from argparse import ArgumentParser
from dateutil import parser

import tokens
from models import *

class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, email):
	tweepy.StreamListener.__init__(self)
	self.email = email

    def on_status(self, status):
        ''' Stores incoming tweets into tweets.db '''

        # print "Incoming tweet..."
        # print status.text

        status_data = Tweet(id = status.id,
                            status_text = status.text,
                            user_id = status.author.id,
                            user_follow_request_sent = status.author.follow_request_sent,
                            status_is_retweeted = status.retweeted,
                            status_retweet_count = status.retweet_count,
                            status_original_tweet_id = status.retweeted_status.id if (status.retweet_count > 0) else 0,
                            status_created_at = status.created_at,
                            status_source = status.source,
                            status_urls = json.dumps(status.entities['urls']),
                            status_hashtags = json.dumps(status.entities['hashtags']),
                            status_mentions = json.dumps(status.entities['user_mentions']),
                            status_is_retweet = True if status.text[:2] == "RT" else False
                            )

        user_data = Session.query(User).filter(User.id == status.author.id).first()
        if not user_data:
            user_data =   User(id = status.author.id,
                               user_name = status.author.screen_name,
                               user_followers_count = status.user.followers_count,
                               user_friends_count = status.user.friends_count,
                               user_statuses_count = status.author.statuses_count,
                               user_favourites_count = status.author.favourites_count,
                               user_listed_count = status.author.listed_count,
                               )

        Session.add(status_data)
        Session.add(user_data)

        try:
            print status.text.encode('utf-8') if status.text else ""
            print "Committing.."

            Session.commit()

        except Exception, e:
	    print >> sys.stderr, 'Encountered Exception: ', e
            self.send_error_email()
            pass


    def on_error(self, status_code):
        ''' Handle errors originating from the stream'''

        print >> sys.stderr, 'Error...'
	self.send_error_email()
        return True # don't kill the stream

    def on_timeout(self):
        ''' Handle timeouts from the Twitter API '''

        print >> sys.stderr, 'Timeout...'
	self.send_error_email()
        return True # don't kill the stream


    def send_error_email(self):
        fromaddr = "twitterpipeline@yahoo.com"
	toaddr = self.email
        msg = """
	      Hey! There was an error with your twitter stream pipeline. It's on you to check it out ands see if we need a restart.
	      Traceback:
	      %s
	      """ % (traceback.format_exc())
	server = smtplib.SMTP('smtp.yahoo.com:587')
	server.starttls()
        server.login("twitterpipeline@yahoo.com", "Sk8board")
	server.sendmail(fromaddr, toaddr, msg)
	server.quit()

def read_keywords(filename):
    ''' Reads in keywords from txt to a list '''
    
    file = open(filename)
    reader = csv.reader(file)

    keywords = []
    for row in reader:
	keywords += row

    return keywords

if __name__ == "__main__":

    # keyword and email configuration 
    parser = ArgumentParser()
    parser.add_argument("-k", "--keywords", help="Path to your keywords file", required=True)
    parser.add_argument("-e", "--email", help="Email address for error notification", required=True)
    args = parser.parse_args()

    keywords_file = args.keywords
    email = args.email

    # initialize auth using tweepy's built in oauth handling
    auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET)
    auth.set_access_token(tokens.ACCESS_TOKEN, tokens.ACCESS_TOKEN_SECRET)

    # create our listener and stream
    listener = TwitterStreamListener(email)
    stream = tweepy.streaming.Stream(auth, listener)

    # define terms we want to filter on
    query_terms = read_keywords(keywords_file)

    # filter the stream on query_terms
    stream.filter(track=query_terms)
