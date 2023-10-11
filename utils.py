# -*- coding: utf-8 -*-
"""
utils.py: catmon_lastseen_app helper functions
"""

import io
import datetime as dt
import json

import streamlit as st

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from PIL import Image, ImageEnhance
from zoneinfo import ZoneInfo


# ref: https://stackoverflow.com/questions/739241/date-ordinal-output
def ordinal(date_int):
    """Return string with date_int followed by ordinal suffix."""
    if 10 <= date_int % 100 < 20:
        return str(date_int) + 'th'

    return str(date_int) + {1: 'st', 2: 'nd', 3: 'rd'}.get(
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


# https://pythonexamples.org/python-pillow-adjust-image-brightness/
def enhance_image(pil_image, factor=2.0):
    """Return enhanced pil image.

    This is particularly useful for some of the darker, night-time images."""
    # instantiate the image brightness enhancer
    enhancer = ImageEnhance.Brightness(pil_image)

    # brighten the image
    img_output = enhancer.enhance(factor)

    return img_output


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


@st.cache_resource
def gdrive_connect():
    """Connect to google drive service"""
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # load json authentication string from environment variable
    # it may contain escape chars so strict set to False
    service_account_info = json.loads(
        st.secrets["GDRIVE_AUTH"],
        strict=False)

    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)

    return drive_service


def download_drive_image(drive_service, file_id):
    """Download image with given file_id using given drive_service"""
    request = drive_service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        # print("Download %d%%" % int(status.progress() * 100))

    return Image.open(fh)


def gdrive_get_most_recent_image(drive_service, folder_id):
    """Return most recent image and filename in given Google Drive folder_id."""

    # print(f"gdrive_get_most_recent_image(): {drive_service=}, {folder_id=}")
    FILES_PER_PAGE = 1

    # read next image file in folder
    query = f"'{folder_id}' in parents and mimeType='image/jpeg'"
    response = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=FILES_PER_PAGE).execute()

    # extract the image data
    file = response.get('files', [])[0]
    image_name = file.get('name')
    image_id = file.get('id')
    # print(f"gdrive_get_most_recent_image(): {file=}, {image_name=}, {image_id=}")

    # download the image object
    image_obj = download_drive_image(drive_service, image_id)

    return image_obj, image_name
