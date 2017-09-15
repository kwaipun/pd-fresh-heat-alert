import praw
import pypd
from datetime import datetime
from os import environ

pypd.api_key = environ.get('pd_api_key')
reddit = praw.Reddit(client_id=environ.get('reddit_cid'), client_secret=environ.get('reddit_secret'),
                     user_agent='testscript')

subreddit = reddit.subreddit('hiphopheads')

viewed = []

while True:
    for submission in subreddit.hot(limit=25):
        if submission.title.startswith('[FRESH') and submission.id not in viewed:
            viewed.append({'title': submission.title,
                            'url': submission.url,
                            'timestamp': datetime.fromtimestamp(submission.created)})

            pypd.Event.create(data={
                'service_key': environ.get('pd_service_key'),
                'event_type': 'trigger',
                'description': submission.title,
                'contexts': [
                    {
                        'type': 'link',
                        'href': submission.url,
                        'text': 'FRESH HEAT ALERT %d'.format(submission.title),
                    },
                            ],
            })



            print submission.title
    time.sleep(3600) # 1hr

    #TODO: clean viewed entries
