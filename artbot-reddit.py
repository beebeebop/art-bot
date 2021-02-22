import os
import tempfile
import requests
import io

from dotenv import load_dotenv
load_dotenv()

from PIL import Image

import praw
from imgurpython import ImgurClient


PROCESS_N = 1

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="my user agent",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

client = ImgurClient(
    os.getenv("IMGUR_CLIENT_ID"),
    os.getenv("IMGUR_CLIENT_SECRET"),
    os.getenv("IMGUR_ACCESS_TOKEN"),
    os.getenv("IMGUR_REFRESH_TOKEN")
)

tmpfile = tempfile.NamedTemporaryFile(suffix='.jpg')


sub = reddit.subreddit("Redditgetsdrawnbybot")

for submission in sub.new(limit=PROCESS_N):
    #--------Get the submission photo:

    #print(submission._fetch_data())
    print(submission.title)
    print(submission.created_utc)
    print(submission.selftext)
    print(len(submission.comments))
    img_url = submission.preview['images'][0]['source']['url']
    print(img_url)

    r = requests.get(img_url)
    im = Image.open(io.BytesIO(r.content))
    im.show()
    #im.save(tmpfile.name)


    #--------Draw something from the photo:




    #--------Submit the drawing:
    
