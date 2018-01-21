"""
tweet stuff in intervals
"""

import time

import twitter

from markov_chains.generate_text import setup_model
from config import config_no, config_yes

MAX_TWEET_LENGTH = 280
greeting = ' Sehr geehrte/r Anstragssteller/in.'
ending = ' MfG'
num_tweets = 3

class FoiaBot:
    def __init__(self, config):
        self.api = twitter.Api(consumer_key=config["consumer_key"],
                               consumer_secret=config["consumer_secret"],
                               access_token_key=config["access_token"],
                               access_token_secret=config["access_token_secret"], sleep_on_rate_limit=True)
        self.screen_name = config["screen_name"]
        self.model = setup_model(config["model_path"])

    def get_favorites(self):
        favorites = self.api.GetFavorites(
            screen_name=self.screen_name, count=200)
        print(favorites)
        fav_set = set([f.id for f in favorites])
        return fav_set

    def get_status_to_work_on(self):
        favorites = self.get_favorites()

        status_list = self.api.GetMentions(count=200, trim_user=True,
                                           contributor_details=False, include_entities=False)
        for status in status_list:
            print(status)
            if status.id in favorites:
                continue
            if status.in_reply_to_status_id is not None:
                continue
            if not status.text.startswith('@' + self.screen_name):
                continue
            self.post_replies(status)

    def post_replies(self, status):
        tweets = self.create_tweets()
        status_id = status.id
        print(tweets)
        success = True
        for tweet in tweets:
            response = self.api.PostUpdate(tweet, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True,
                exclude_reply_user_ids=False, trim_user=True, verify_status_length=False)
            if response is None:
                success = False
                break

        if success:
            self.api.CreateFavorite(status=status)


    def generate_sentence(self, max_length=150):
        return self.model.make_short_sentence(max_length, tries=100)

    def create_tweets(self):
        tweets = []

        for i in range(num_tweets):
            tweet_text = f'{i + 1}/{num_tweets}'
            if i == 0:
                tweet_text += greeting

            while True:
                chars_left = MAX_TWEET_LENGTH - len(tweet_text) - 1 #because of space

                # ensure space for the ending
                if i + 1 == num_tweets:
                    chars_left -= len(ending)

                if chars_left < 20:
                    # at ending
                    if i + 1 == num_tweets:
                        tweet_text += ending
                    break
                if chars_left < 70:
                    new_sent = self.generate_sentence(chars_left)
                    if new_sent is not None and len(new_sent) < chars_left:
                        tweet_text += ' ' + new_sent
                else:
                    new_sent = self.generate_sentence()
                    if new_sent is not None and len(new_sent) < chars_left:
                        tweet_text += ' ' + new_sent

            tweets.append(tweet_text)

        return tweets


    def run(self):
        self.get_status_to_work_on()


def main():
    no_bot = FoiaBot(config_no)
    yes_bot = FoiaBot(config_yes)

    while True:
        no_bot.run()
        yes_bot.run()
        time.sleep(30)

if __name__ == '__main__':
    main()
