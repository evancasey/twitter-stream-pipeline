from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Boolean,
                        DateTime,
                        MetaData,
                        )

# set up our local DB to store the tweets
db = create_engine('sqlite:///tweets.db')
Base = declarative_base(bind=db)
Session = scoped_session(sessionmaker(db))
db.echo = False

class Tweet(Base):
  ''' Class to store individual tweet traits '''
  
  __tablename__ = 'tweet'

  id = Column(Integer, primary_key=True)
  status_text = Column(String)
  user_id = Column(Integer)
  user_follow_request_sent = Column(Boolean)
  status_is_retweeted = Column(Boolean)
  status_retweet_count = Column(Integer)
  status_original_tweet_id = Column(Integer)
  status_created_at = Column(String)
  status_source = Column(String)
  status_urls = Column(String)
  status_hashtags = Column(String)
  status_mentions = Column(String)
  status_is_retweet = Column(Boolean)


class User(Base):
  ''' Class to store individual user traits '''
  
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  user_name = Column(String)
  user_followers_count = Column(Integer)
  user_friends_count = Column(Integer)
  user_statuses_count = Column(Integer)
  user_favourites_count = Column(Integer)
  user_listed_count = Column(Integer)
  user_mention_count = Column(Integer)
  user_retweet_count = Column(Integer)

# create our db
Base.metadata.create_all(db)
