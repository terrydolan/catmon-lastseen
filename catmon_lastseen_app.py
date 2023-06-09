# -*- coding: utf-8 -*-
"""
Catmon Last Seen App

The web app shows when Boo or Simba were last seen.

The app parses the @boosimba catmon tweets, which include the cat images from
catmon, and the replies from the catmon image classifier that categorises
the cat image as Boo, Simba or Unknown.

The associated images are enhanced and displayed.

To run:
    $streamlit run catmon_lastseen_app.py

History
v0.1.0 - Aug 2022, First version
v0.2.0 - June 2023, Update to handle situation where catmonic not running;
         Update to use latest version of streamlit
"""

import streamlit as st
import tweepy
import utils

__author__ = "Terry Dolan"
__copyright__ = "Terry Dolan"
__license__ = "MIT"
__email__ = "terry8dolan@gmail.com"
__status__ = "Beta"
__version__ = "0.2.0"
__updated__ = "June 2023"


# configure streamlit page
st.set_page_config(
    page_title="catmon_lastseen_app", page_icon=":cat:", layout="centered",
    initial_sidebar_state="auto", menu_items={
    'About': "Catmon Last Seen App"
    }
)

st.title("Catmon Last Seen App")

# instantiate the twitter api
auth = tweepy.OAuth1UserHandler(**st.secrets.twitter_auth_info)
api = tweepy.API(auth)

# create the two tweet dictionaries containing the catmon auto-tweets (with
# the cat images) and and the replies from the catmon image classifier (with
# the cat label)
tweet_d, tweet_reply_d = utils.parse_catmon_tweets(api)

# check the dictionaries
if not tweet_d:
    st.error("Unexpected error: no @boosimba catmon tweets found")
    st.stop()
if not tweet_reply_d:
    st.info("""
        No catmon image classifications found on @boosimba catmon tweets, 
        check catmonic is running.  
        Therefore only the latest catmon image will be shown, classified 
        as 'unknown'.
        """)
    # st.stop()

# assert len(tweet_d) != 0, "unexpected error, tweet_d is empty"
# assert len(tweet_reply_d) != 0, "unexpected error, tweet_reply_d is empty"


# process the tweet dictionaries obtain the 'last seen' data
last_seen_d = utils.get_last_seen(tweet_d, tweet_reply_d)

# show the last seen info
found_boo = True if 'boo' in last_seen_d else False
found_simba = True if 'simba' in last_seen_d else False
images = []
captions = []

# test different UI scenarios with a variable number of images
# st.write(last_seen_d) # normally 2 images; can be 0 to 3 images
# del(last_seen_d['boo']); found_boo = False # reduce to 1 image
# del(last_seen_d['simba']); found_simba= False # reduce to 1 image
# last_seen_d["unknown"] = ("2022-08-03_045303.jpg",
#                           "http://pbs.twimg.com/media/FZNSPVEXgAIvWni.jpg");\
#                             # add extra image
# last_seen_d = [] # remove all images

if last_seen_d:
    for label, (image_fname, image_url) in last_seen_d.items():
        img_date_str = image_fname.split('.')[0]
        friendly_lastseen_date = utils.get_friendly_lastseen_date(img_date_str)
        if label == "boo":
            label_enh = "Boo (aka Fluffbag)"
        elif label == "simba":
            label_enh = "Simba (aka Mr. Handsome)"
        elif label == "unknown":
            label_enh = "Unknown (aka the cat of mystery)"
        else:
            raise ValueError("label is not 'boo', 'simba' or 'unknown")
        st.write((
            f"{label_enh} was last seen {friendly_lastseen_date}"
            ))

        # download the associated image and enhance (given that some are dark)
        img = utils.image_download(image_url)
        img_enh = utils.resize(utils.enhance_image(img))
        images.append(img_enh)
        captions.append(f"{label} ({image_fname})")
    st.markdown("***")

# report if Boo and/or Simba not found
if not found_simba and not found_boo:
    st.write(
        f"Could not find Boo or Simba in last {len(tweet_d)} "
        f"tweets from @boosimba"
        )
else:
    if not found_boo:
        st.write(
            f"Could not find Boo in last {len(tweet_d)} "
            f"tweets from @boosimba"
        )
    if not found_simba:
        st.write(
            f"Could not find Simba in last {len(tweet_d)} "
            f"tweets from @boosimba"
            )

# show the associated images
if images:
    st.markdown("**Latest cat images**")
    cols = st.columns(len(images), gap='small')
    for idx, col in enumerate(cols):
        with col:
            st.image(images[idx], captions[idx])

st.write("[@boosimba twitter account](https://twitter.com/boosimba)")
st.write("  ")

# Show info about the app
with st.expander("Show the app's readme (from github)"):
    ABOUT_MD_STR = utils.read_file_str('README.md')
    st.markdown(ABOUT_MD_STR, unsafe_allow_html=True)
    
