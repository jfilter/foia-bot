"""
tweet stuff in intervals
"""

import time
import datetime

import twitter

from markov_chains import german_text
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
        self.model = german_text.setup_model(config["model_path"])
        self.hour_to_tweet = config["hour_to_tweet"]

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
        print(tweets)
        success = True
        reply_to_status_id = status.id
        for tweet in tweets:
            response = self.api.PostUpdate(tweet, in_reply_to_status_id=reply_to_status_id, auto_populate_reply_metadata=True,
                                           exclude_reply_user_ids=False, trim_user=True, verify_status_length=False)
            if response is None:
                success = False
                break
            else:
                reply_to_status_id = response.id

        if success:
            self.api.CreateFavorite(status=status)

    def generate_sentence(self, tweet_text, chars_left, set_limit=False):
        max_length = 150
        if set_limit:
            max_length = chars_left

        new_sent = self.model.make_short_sentence(max_length, tries=100)
        if new_sent is not None and len(new_sent) < chars_left:
            tweet_text += ' ' + new_sent
        return tweet_text

    # https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
    def get_date_from_twitter_string(self, created_at):
        x = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        return datetime.datetime.fromtimestamp(time.mktime(x))


    def tweet_once_a_day(self):
        now = datetime.datetime.now()
        print(now.hour)
        if now.hour == self.hour_to_tweet:
            last_status_list = self.api.GetUserTimeline(screen_name=self.screen_name, count=1,
                                     include_rts=False, trim_user=True, exclude_replies=True)
            print(last_status_list)
            if last_status_list is None:
                return
            if len(last_status_list) == 0:
                self.post_single_tweet()
            if len(last_status_list) == 1:
                last_status = last_status_list[0]
                created_at_date = self.get_date_from_twitter_string(last_status.created_at)

                time_diff = now - created_at_date
                print('time_diff', time_diff)
                time_diff_hours = time_diff.seconds / 3600 + time_diff.days * 24
                print(time_diff_hours)
                if time_diff_hours > 20: # something is broken with the date but whatever
                    self.post_single_tweet()

    def post_single_tweet(self):
        tweet_text = self.generate_single_tweet_text()
        response = self.api.PostUpdate(tweet_text, verify_status_length=False)

    def generate_single_tweet_text(self):
        tweet_text = ""
        while True:
            chars_left = MAX_TWEET_LENGTH - len(tweet_text)
            chars_left -= 1 # for the space
            if chars_left < 20:
                break
            if chars_left < 70:
                tweet_text = self.generate_sentence(
                    tweet_text, chars_left, True)
            else:
                tweet_text = self.generate_sentence(
                    tweet_text, chars_left)
        return tweet_text

    def create_tweets(self):
        tweets = []

        for i in range(num_tweets):
            tweet_text = f'{i + 1}/{num_tweets}'
            if i == 0:
                tweet_text += greeting

            while True:
                chars_left = MAX_TWEET_LENGTH - \
                    len(tweet_text) - 1  # because of space

                # ensure space for the ending
                if i + 1 == num_tweets:
                    chars_left -= len(ending)

                if chars_left < 20:
                    # at ending
                    if i + 1 == num_tweets:
                        tweet_text += ending
                    break
                if chars_left < 70:
                    tweet_text = self.generate_sentence(tweet_text, chars_left, True)
                else:
                    tweet_text = self.generate_sentence(
                        tweet_text, chars_left)


            tweets.append(tweet_text)

        return tweets

    def run(self):
        self.get_status_to_work_on()


def main():
    print('main called')
    no_bot = FoiaBot(config_no)
    print('after setting up no bot')
    yes_bot = FoiaBot(config_yes)
    print('after setting up yes bot')

    no_bot.run()
    print('after running no bot')
    yes_bot.run()
    print('after running yes bot')
    no_bot.tweet_once_a_day()
    yes_bot.tweet_once_a_day()
    print('after tweet once a day')


def lambda_handler(event, context):
    print('handler called')
    main()
    print('handler about to finish')


# if __name__ == '__main__':
#     main()
