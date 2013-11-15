import oauth2 as oauth
import json

class SentifiTwitterClient:
    def __init__(self, url):
        OAUTH_TOKEN = "18113338-60RyLRMrW4vFxqBibn5LJPx4EAJgByRjLctM86w"
        OAUTH_SECRET = "W9GSPl8dItl4Bk3J6dKNImcL99PSbZinkn4FREWVhUg"
        CONSUMER_KEY = "egYRKgKOkJ2Utf06tYUFw"
        CONSUMER_SECRET = "ezfzK9ddmwCCgBVJKCKHROYfEwX86wWYqLoVMZhicU"

        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_SECRET)
        #connection = oauth.Client(consumer, access_token)
        client = oauth.Client(consumer, access_token)
        response, data = client.request(url)
        json_data = json.loads(data)
        self.data = json_data

    @property
    def client(self):
        OAUTH_TOKEN = "18113338-60RyLRMrW4vFxqBibn5LJPx4EAJgByRjLctM86w"
        OAUTH_SECRET = "W9GSPl8dItl4Bk3J6dKNImcL99PSbZinkn4FREWVhUg"
        CONSUMER_KEY = "egYRKgKOkJ2Utf06tYUFw"
        CONSUMER_SECRET = "ezfzK9ddmwCCgBVJKCKHROYfEwX86wWYqLoVMZhicU"

        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_SECRET)
        return oauth.Client(consumer, access_token)
print SentifiTwitterClient("https://api.twitter.com/1.1/users/lookup.json?screen_name=glorevenhite").data