# art-bot

## Installation on Ubuntu

### python and virtualenv


### Install dependencies inside the Python virtual environment

$ mkvirtualenv art-bot -p python3
$ pip install -r requirements.txt


## Run

$ workon art-bot
$ python artbot-reddit.py

To exit the current Python virtual environment:
$ deactivate


## Cron Job

$ crontab -e
and copy the following cron job into it,
