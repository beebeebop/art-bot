# art-bot

## Setup on Ubuntu

### python, pip, virtualenv and virtualenvwrapper

There are different ways to do this. [Here](https://medium.com/@aaditya.chhabra/virtualenv-with-virtualenvwrapper-on-ubuntu-34850ab9e765) is one way.


### Install dependencies inside the Python virtual environment
```
$ mkvirtualenv art-bot -p python3
$ pip install -r requirements.txt
```

### Get your API access from Reddit and Imgur

1. update file ".env.example" with your Reddit and Imgur access tokens, etc
2. rename ".env.example" to ".env"

Note that load_dotenv() will load environmental variables in the .env file


## Run
```
$ workon art-bot
$ python artbot-reddit.py
```

Argument | Long Name | Meaning | Default
--- | --- | --- | ---
-n | --drawN | get N submissions to draw | 1
-s | --subreddit | from subreddit | Redditgetsdrawnbybot
-c | --comment | make a comment or not | yes
-m | --maxComment | maximum number of comments from current user | 1
### More examples
```
$ python artbot-reddit.py -n 3 -s Redditgetsdrawnbybot -c no
$ python artbot-reddit.py -n 1 -s Redditgetsdrawnbybot -c yes -m 2
```
To exit the current Python virtual environment:
```
$ deactivate
```

## Cron Job
To run this script every 2 hours (for example) automatically,
```
$ crontab -e
```
and copy the following cron job into it,
```
0 */2 * * * cd ~/art-bot && ~/.virtualenvs/art-bot/bin/python artbot-reddit.py -c no >> ~/art-bot.log 2>&1
```


## Acknowledge

The Art transform is similar to
https://github.com/fogleman/Quads
or to see a web demo:
https://www.michaelfogleman.com/static/quads/
