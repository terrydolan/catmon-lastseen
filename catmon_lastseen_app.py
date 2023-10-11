# -*- coding: utf-8 -*-
"""
Catmon Last Seen App

The web app shows when Boo or Simba were last seen.

The app reads the latest cat image files from Google Drive, parses the filename to determine when the cat
was last seen, and displays the last seen information and the latest image.

To run:
    $streamlit run catmon_lastseen_app.py

History
v0.1.0 - Aug 2022, First version; parses the @boosimba catmon tweets
v0.2.0 - June 2023, Update to handle situation where catmonic image classifier not running;
         Update to use latest version of streamlit
v0.3.0 - Oct 2023, Update to handle situation where app is forbidden from reading catmon tweets
v0.4.0 - Oct 2023, Read catmon images from private Google Drive account instead of public Twitter account,
         as Twitter free access no longer includes read access to tweets
"""

import streamlit as st
import utils

__author__ = "Terry Dolan"
__copyright__ = "Terry Dolan"
__license__ = "MIT"
__email__ = "terry8dolan@gmail.com"
__status__ = "Beta"
__version__ = "0.4.0"
__updated__ = "October 2023"

# configure streamlit page and set title
st.set_page_config(
    page_title="catmon_lastseen_app", page_icon=":cat:", layout="centered",
    initial_sidebar_state="auto", menu_items={'About': "Catmon Last Seen App"})
st.title("Catmon Last Seen App")

# connect to Google Drive
drive_service = utils.gdrive_connect()

# get latest Boo image and filename from Boo folder
boo_img_obj, boo_img_name = utils.gdrive_get_most_recent_image(
    drive_service=drive_service,
    folder_id=st.secrets["BOO_IMAGES_FOLDER_ID"])

# report when Boo was last seen
boo_img_date_str = boo_img_name.split('.')[0]
boo_lastseen = utils.get_friendly_lastseen_date(image_date_str=boo_img_date_str)
st.write(f"Boo, aka Fluff Bag!, was last seen {boo_lastseen}")

# prepare the Boo image and caption, ready to display
boo_img_obj_enh = utils.resize(utils.enhance_image(boo_img_obj))
boo_img_caption = f"Boo ({boo_img_name})"

# get latest Simba image and filename from Simba folder
simba_img_obj, simba_img_name = utils.gdrive_get_most_recent_image(
    drive_service=drive_service,
    folder_id=st.secrets["SIMBA_IMAGES_FOLDER_ID"])

# report when Simba was last seen
simba_img_date_str = simba_img_name.split('.')[0]
simba_lastseen = utils.get_friendly_lastseen_date(image_date_str=simba_img_date_str)
st.write(f"Simba, aka Mr Handsome!, was last seen {simba_lastseen}")

# prepare the Simba image and caption, ready to display
simba_img_obj_enh = utils.resize(utils.enhance_image(simba_img_obj))
simba_img_caption = f"Simba ({simba_img_name})"

# show the enhanced images and captions
st.markdown("***")
st.markdown("**Latest cat images**")
col1, col2 = st.columns(2, gap='small')

with col1:
    st.image(boo_img_obj_enh, boo_img_caption)

with col2:
    st.image(simba_img_obj_enh, simba_img_caption)

# show additional information
st.write("  ")
addl_info = st.checkbox("Additional Information")

if addl_info:
    # show link to boosimba Twitter account
    st.write("[@boosimba Twitter account](https://twitter.com/boosimba)")

    # show link to GitHub repo and option to show readme file
    st.write("[Catmon Last Seen GitHub repo](https://github.com/terrydolan/catmon-lastseen)")
    with st.expander("Show the app's readme (from GitHub)"):
        ABOUT_MD_STR = utils.read_file_str('README.md')
        st.markdown(ABOUT_MD_STR, unsafe_allow_html=True)
