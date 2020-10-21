import logging
import tweepy
import os

import azure.functions as func


def main(msg: func.QueueMessage) -> func.HttpResponse:
    tweets_enabled = os.environ["EnableTweets"]

    message = msg.get_body().decode("utf-8")

    if tweets_enabled == "true":
        tweet(message)
        logging.info(f'Tweeted!')
    else:
        logging.info(f'Would have tweeted message:\n{message}')


def tweet(message: str) -> None:

    consumer_key = os.environ["TwitterConsumerKey"]
    consumer_secret = os.environ["TwitterConsumerSecret"]
    access_token = os.environ["TwitterAccessToken"]
    access_token_secret = os.environ["TwitterAccessTokenSecret"]

    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
    # authentication of access token and secret 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    
    # update the status 
    api.update_status(status = message) 