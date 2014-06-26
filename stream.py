''' Twitter streaming utility for BTC-related keywords '''

import sys
import tweepy
import json
from dateutil import parser

import tokens
from models import *

class TwitterStreamListener(tweepy.StreamListener):

    def on_status(self,status):
        ''' Method to store incoming tweets into stream.db '''

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
                               user_mention_count = 0, #fill in later
                               user_retweet_count = 0 #fill in later
                               )

        Session.add(status_data)
        Session.add(user_data)

        try:
            # print status.text.encode('utf-8') if status.text else ""
            # print "Committing.."

            Session.commit()

        except Exception, e:
            # handle sqlalchemy errors
            print >> sys.stderr, 'Encountered Exception: ', e
            pass

    def on_error(self, status_code):
        ''' Handle errors originating from the stream'''

        print >> sys.stderr, 'Error...'
        return True # don't kill the stream

    def on_timeout(self):
        ''' Handle timeouts from the Twitter API '''

        print >> sys.stderr, 'Timeout...'
        return True # don't kill the stream


if __name__ == "__main__":

    # initialize auth using tweepy's built in oauth handling
    auth = tweepy.OAuthHandler(tokens.CONSUMER_KEY,tokens.CONSUMER_SECRET)
    auth.set_access_token(tokens.ACCESS_TOKEN,tokens.ACCESS_TOKEN_SECRET)

    # create our listener and stream
    listener = BTCStreamListener()
    stream = tweepy.streaming.Stream(auth,listener)

    # define terms we want to filter on
    # TODO: Use arg parsing
    query_terms = ['btc','bitcoin']

    # filter the stream on query_terms
    stream.filter(track=query_terms)
