from twython import TwythonStreamer
import pymongo
from flask import Flask

app = Flask(__name__)

try:
    conn = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    print("Connected To mongo")

except pymongo.errors.ConnectionFailure as e:
    print(e)
db = conn["twitter"]

with open('consumer_key.txt', 'r') as f:
    consumer_key = f.read()
f.closed

with open('consumer_secret.txt', 'r') as f:
    consumer_secret = f.read()
f.closed

with open('access_key.txt', 'r') as f:
    access_key = f.read()
f.closed

with open('access_secret.txt', 'r') as f:
    access_secret = f.read()
f.closed


def process_tweet(tweet):
    d = dict(hashtags=[hashtag['text'] for hashtag in tweet['entities']['hashtags']], user=tweet['user'],
             created_at=tweet['created_at'], geo=tweet['geo'], reply_count=tweet['reply_count'],
             retweet_count=tweet['retweet_count'], favorite_count=tweet['favorite_count'], id=tweet['id_str'],
             in_reply_to_status_id=tweet['in_reply_to_status_id_str'],
             in_reply_to_user_id_str=tweet['in_reply_to_user_id_str'])
    return d


class StreamTwitter(TwythonStreamer):
    count = 0

    def on_success(self, data):
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            db.tweets.insert_one(data)
            self.count += 1
            if self.count % 100 == 0:
                print("tweet received: " + str(self.count))

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()


@app.route('/')
def main():
    credentials = {'CONSUMER_KEY': consumer_key, 'CONSUMER_SECRET': consumer_secret, 'ACCESS_TOKEN': access_key,
                   'ACCESS_SECRET': access_secret}

    collect = StreamTwitter(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                            credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    str = input('Enter The Hastag: ')
    collect.statuses.filter(track=str)


if __name__ == "__main__":
    main()
