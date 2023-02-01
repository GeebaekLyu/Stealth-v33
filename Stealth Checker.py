import tweepy
import telegram
import time


def send_telegram_message(message, chat_id="-1001450593946"):
    while True:
        try:
            bot = telegram.Bot(token="5889488279:AAFQCNK6dw3dLiLFB7euCsEHtqzDNlmG0P4")
            try:
                bot.sendMessage(chat_id=chat_id, text=message, parse_mode='HTML')
            except telegram.error.BadRequest as e:
                print(e)
                bot.sendMessage(chat_id=chat_id, text=message[:2000])
            break
        except (telegram.error.RetryAfter, telegram.error.TimedOut, telegram.error.NetworkError):
            time.sleep(60)
            continue

class TwitterScraper(object):

    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token)
        self.s_client = self.IDPrinter(bearer_token)

    def remove_rules(self):
        ids = []
        results = self.s_client.get_rules()
        if results[0]:
            for result in results[0]:
                ids.append(result[2])
            self.s_client.delete_rules(ids=ids)
        print(self.s_client.get_rules())

    def run(self):
        self.remove_rules()
        # 여기서 rule을 바꿀 수 있음
        self.s_client.add_rules(add=tweepy.StreamRule('launched "dexscreener.com" -is:retweet -is:reply'))
        self.s_client.add_rules(add=tweepy.StreamRule('live "dexscreener.com" -is:retweet -is:reply'))
        self.s_client.add_rules(add=tweepy.StreamRule('launched "dextools.com" -is:retweet -is:reply'))
        self.s_client.add_rules(add=tweepy.StreamRule('live "dextools.com" -is:retweet -is:reply'))
        self.s_client.filter(threaded=True, tweet_fields=True, expansions='author_id')

    class IDPrinter(tweepy.StreamingClient):

        def on_tweet(self, tweet):
            self.last_tweet = tweet
            print(tweet)

        def on_includes(self, tweet):
            username = tweet['users'][0].username
            send_telegram_message(f'<b>{username}</b> \n {self.last_tweet}')
            print(tweet)

        def on_errors(self, tweet):
            print(f'on_errors: {tweet}')


if __name__ == '__main__':
    agent = TwitterScraper("AAAAAAAAAAAAAAAAAAAAAJMjlgEAAAAAKEgVY5fD2%2FENjfs4NtbO4TTAc2I%3Dm0k3t33hXouIRNHtZ9ft2UG73OoGq6qCTakL4AY4Dc2lSzkZYP")
    agent.run()
