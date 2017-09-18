import praw
import pypd
import time

from datetime import datetime
from os import environ

pypd.api_key = environ.get('pd_api_key')
reddit = praw.Reddit(client_id=environ.get('reddit_cid'),
                     client_secret=environ.get('reddit_secret'),
                     user_agent='testscript')

subreddit = reddit.subreddit('hiphopheads')

viewed = []


def clean(item):
    diff = datetime.now() - item['timestamp']
    if diff.days == 0:
        return True


def fetch():
    for s in subreddit.hot(limit=25):
        if s.title.startswith('[FRESH') and s.id not in viewed:
            viewed.append({'title': s.title,
                           'url': s.url,
                           'timestamp': datetime.fromtimestamp(s.created)})

            pypd.Event.create(data={
                'service_key': environ.get('pd_service_key'),
                'event_type': 'trigger',
                'description': s.title,
                'contexts': [
                    {
                        'type': 'link',
                        'href': s.url,
                        'text': 'FRESH HEAT ALERT',
                    },
                ],
            })

            print(s.title)


while True:
    fetch()
    viewed = filter(clean, viewed)
    time.sleep(3600)
