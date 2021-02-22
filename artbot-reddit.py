import os
import tempfile
import requests
import io
import argparse

import random
import datetime
random.seed(datetime.datetime.now())

from dotenv import load_dotenv
load_dotenv()

from PIL import Image

import praw
from imgurpython import ImgurClient

import divide

PROCESS_N = 1

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--drawN', type=int, default=1)
parser.add_argument('-s', '--subreddit', type=str, default='Redditgetsdrawnbybot')
parser.add_argument('-c', '--comment', type=str, default='yes')
parser.add_argument('-m', '--maxComment', type=int, default=1)
args = parser.parse_args()




reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="my user agent",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

imgur = ImgurClient(
    os.getenv("IMGUR_CLIENT_ID"),
    os.getenv("IMGUR_CLIENT_SECRET"),
    os.getenv("IMGUR_ACCESS_TOKEN"),
    os.getenv("IMGUR_REFRESH_TOKEN")
)

tmpfile = tempfile.NamedTemporaryFile(suffix='.jpg')


sub = reddit.subreddit(args.subreddit)

for submission in sub.new(limit=args.drawN):
    #--------Get the submission photo:
    print(submission.title)
    print(submission.created_utc)

    m = 0
    for top_level_comment in submission.comments:
        #print(top_level_comment.author)
        if top_level_comment.author == os.getenv("REDDIT_USERNAME"):
            m += 1
    if m >= args.maxComment:
        continue

    img_url = submission.preview['images'][0]['source']['url']
    print('Drawing: {}'.format(img_url))

    r = requests.get(img_url)
    im = Image.open(io.BytesIO(r.content))
    #im.show()
    #im.save(tmpfile.name)



    #----------Resize the image for faster processing
    S = 1920
    w, h = im.size
    if w > h:
        new_w = S
        new_h = int(S*h/w)
    else:
        new_h = S
        new_w = int(S*w/h)
    im = im.resize((new_w, new_h), resample=Image.BICUBIC)

    #---------In case the image is png and it has an alpha channel
    if im.mode == 'RGBA':
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask = im.split()[3])
        im = background



    #--------Draw something from the photo:
    line_color = random.choice(['#FFFFFF', '#000000'])
    iterations = random.randint(50, 600)

    original = divide.Original(im, line_color=line_color)

    for x in range (iterations):
        original.split()

    im2 = original.drawSections()
    #im2.show()


    #--------Submit the drawing:
    if args.comment=='yes':
        im2.save(tmpfile.name)
        r = imgur.upload_from_path(tmpfile.name, config={'title': 'Redditgetsdrawnbybot'}, anon=False)
        #pprint(r)

        #Reply to the original submission with the imgur link
        reply_text = "[Here]({}), I hope you like it.".format(r['link'])
        submission.reply(reply_text)
        print('Replied with {}'.format(reply_text))
    else:
        im2.save('result.jpg')
