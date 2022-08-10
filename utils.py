# -*- coding: utf-8 -*-
"""
utils.py: catmon_lastseen_app helper functions
"""

from collections import OrderedDict
from io import BytesIO
from zoneinfo import ZoneInfo
import datetime as dt
import math

from PIL import Image, ImageEnhance, ImageStat
import requests

def image_download(media_url):
    """Download image at given media_url."""
    response = requests.get(media_url)
    img = Image.open(BytesIO(response.content))

    return img

def is_catmon(tweet_full_text):
    """Return True if given tweet text is from catmon auto-tweet."""
    CATMON_START_TEXT = 'auto-tweet from catmon: '
    if tweet_full_text.startswith(CATMON_START_TEXT):
        return True

    return False

def is_catmonic(tweet_full_text):
    """Return True if given tweet text is from catmon image classification."""
    CATMONIC_TEXT = (
        'image automatically identified by the catmon image classifier cnn'
        )
    if CATMONIC_TEXT in tweet_full_text:
        return True

    return False

def get_catmonic_label(tweet_full_text):
    """Return label and reply text from the given tweet reply text.

    The classification label is provided by the catmon image classifier
    and can be 'boo' or 'simba'.
    """
    assert is_catmonic(tweet_full_text), (
        "unexpected error: tweet is not from catmon image classifier"
        )

    # get label from classification text
    if tweet_full_text.startswith('Hello Boo'):
        return 'boo'

    if tweet_full_text.startswith('Hello Simba'):
        return 'simba'

    raise ValueError('Unexpected error parsing catmon image classification, \
                     cannot find label')

def get_catmon_image(catmon_auto_tweet):
    """Return image filename and image url from catmon auto-tweet."""
    image_fname = catmon_auto_tweet.full_text.split(' ')[3]
    image_url = catmon_auto_tweet.entities['media'][0]['media_url']

    return image_fname, image_url

# ref: https://stackoverflow.com/questions/739241/date-ordinal-output
def ordinal(date_int):
    """Return string with date_int followed by ordinal suffix."""
    if 10 <= date_int % 100 < 20:
        return str(date_int) + 'th'

    return  str(date_int) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(
        date_int % 10, "th"
        )

def get_friendly_lastseen_date(image_date_str):
    """Return a friendly date string.

    Input image_date_str format is '%Y-%m-%d_%H%M%S'
    Output is a friendly date string:
        e.g. today at 17:30 - 2.0 hours ago
        yesterday at 04:30 - 24.0 hours ago
        Sunday 17th July at 05:00 - 72.0 hours ago
    """
    CATMON_TIMEZONE = 'Europe/London'
    img_dt = dt.datetime.strptime(image_date_str, "%Y-%m-%d_%H%M%S")
    img_dt = img_dt.replace(tzinfo=ZoneInfo(CATMON_TIMEZONE))
    now_dt = dt.datetime.now(ZoneInfo(CATMON_TIMEZONE))
    hours_ago = (now_dt - img_dt).total_seconds()/(60*60)

    if img_dt.date() == dt.datetime.today().date():
        friendly_date_str = (
            f"today at {img_dt.time().strftime('%H:%M')} "
            f"- {hours_ago:.1f} hours ago"
            )
    elif img_dt.date() == (dt.datetime.today().date() - dt.timedelta(days=1)):
        friendly_date_str = (
            f"yesterday at {img_dt.time().strftime('%H:%M')} "
            f"- {hours_ago:.1f} hours ago"
            )
    else:
        dow = img_dt.date().strftime('%A')
        dom_digits = img_dt.date().strftime('%d')
        month = img_dt.date().strftime('%B')
        friendly_date_str = (
            f"{dow} {ordinal(int(dom_digits))} {month} at "
            f"{img_dt.time().strftime('%H:%M')} - {hours_ago:.1f} hours ago"
            )

    return friendly_date_str

def get_image_brightness(pil_image):
    """Calculate the perceived brightness of a given image object.

    Ref: https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
    Ref: http://alienryderflex.com/hsp.html

    The three constants (.299, .587, and .114) represent the different
    degrees to which each of the primary (RGB) colors affects human
    perception of the overall brightness of a color."""
    R_CONST = 0.299
    G_CONST = 0.587
    B_CONST = 0.114
    stat = ImageStat.Stat(pil_image)
    r, g, b = stat.mean

    return math.sqrt(R_CONST*(r**2) + G_CONST*(g**2) + B_CONST*(b**2))

# https://pythonexamples.org/python-pillow-adjust-image-brightness/
def enhance_image(pil_image, factor=2.0):
    """Return enhanced pil image.

    This is particularly useful for some of the darker, night-time images."""
    # instantiate the image brightness enhancer
    enhancer = ImageEnhance.Brightness(pil_image)

    # brighten the image
    img_output = enhancer.enhance(factor)

    return img_output

def parse_catmon_tweets(api, n=50):
    """Parse last n boosimba tweets (including replies) for catmon tweets.

       Return two dictionaries, one for tweets (containing the image name
       and link) and one for replies (with the full tweet text containing the
       image classification).
    """
    CATMON_USER_NAME = 'boosimba'

    # create ordered dicts
    # these are ordered to maintain date order, with most recent first
    tweet_reply_d = OrderedDict()
    tweet_d = OrderedDict()

    # get the public tweets from the catmon user's timeline
    # with tweet_mode='extended', to ensure full text returned
    public_tweets = api.user_timeline(tweet_mode='extended', count=n)

    # parse the public tweets and populate the two dictionaries
    for tweet in public_tweets:
        if tweet.user.screen_name != CATMON_USER_NAME:
            # ignore any tweets not from catmon user
            continue

        if tweet.in_reply_to_status_id_str:
            # this is a tweet reply
            if is_catmonic(tweet.full_text):
                # this is a catmon image classification
                tweet_reply_d[
                    int(tweet.in_reply_to_status_id_str)
                    ] = tweet.full_text
        elif is_catmon(tweet.full_text):
            # this is a catmon auto-tweet
            image_fname, image_url = get_catmon_image(tweet)
            tweet_d[tweet.id] = [image_fname, image_url]

    return tweet_d, tweet_reply_d

def get_last_seen(tweet_d, tweet_reply_d):
    """Return ordered dict with the 'last seen' most recent data

    Input: tweet and tweet reply ordered dicts
    Output: ordered dict keyed on label, with a value containing a tuple for
    image name and image url.
    """
    last_seen_d = OrderedDict()
    found_boo = found_simba = False

    for tweet_id, (image_fname, image_url) in tweet_d.items():
        if tweet_id in tweet_reply_d:
            label = get_catmonic_label(tweet_reply_d[tweet_id])

            if label == 'boo':
                found_boo = True
            if label == 'simba':
                found_simba = True
        else:
            label = 'unknown'

        if label not in last_seen_d:
            last_seen_d[label] = (image_fname, image_url)

        if found_boo and found_simba:
            break

    return last_seen_d

def resize(img, max_width=300):
    """Resize given PIL image to given max width, maintaining the aspect ratio.

    Note that most catmon images have size 600 x 400 (w x h), so a default
    resize will reduce the image size."""
    width, height = img.size
    ratio = max_width/width
    new_img = img.resize((int(width*ratio), int(height*ratio)))
    return new_img

def read_file_str(filename):
    """Read the file and return as a string."""
    with open(filename, "r", encoding="utf-8") as f:
        file_str = f.read()
    return file_str
