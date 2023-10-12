# Catmon Last Seen App

## Introduction
The *Catmon Last Seen* web app shows when Boo or Simba were last seen.
Boo and Simba are two cool cats with a Twitter account and a Google Drive account!

The app reads the latest cat image files from Google Drive, parses the filename to determine 
when the cat was last seen, and displays the 'last seen' information and the latest image.

The app is built using python, streamlit, PIL and google-api-python-client.

## Key Project Files
The 'catmon\_lastseen\_app.py' is the main python application, with helper
functions in 'utils.py'.

## Run the app
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/terrydolan/catmon-lastseen/main/catmon_lastseen_app.py)

## Catmon Last Seen Output
Here is an example of the app's original output:  
<img src="https://raw.githubusercontent.com/terrydolan/catmon-lastseen/main/images/catmon_lastseen_example_2022-08-10_142300.jpg"
width="300">

## Related Catmon Projects
1. *Catmon*: a cat flap monitor application that takes a picture when a cat
enters through the cat flap, tweets it on @boosimba and uploads the image
to google drive.
The application has been running since 2015. 
It was recently ported to a raspberrypi 3b+ and enhanced to include the 
catmon image classifier (catmonic, see below).  
The app now uses catmonic to try and identify the cat, tweets the identity and automatically 
places the image in a folder for that cat on Google Drive.   
[Catmon repo](https://github.com/terrydolan/catmon)  
2. *Catmon Image Tagger*: a web app that provides a UI to help tag a set of
catmon images as either 'Boo' or 'Simba' or 'Unknown'.
The results are saved to Google Drive.  
[Catmon Image Tagger repo](https://github.com/terrydolan/catmon-img-tag)  
3. *Catmon Image Classifier*: an application that classifies a catmon image 
as 'Boo', 'Simba' or 'Unknown' using a trained MobileNetV2 convolutional neural network (CNN).
The MobileNetV2 model applies transfer learning and was trained, validated and
tested  using the tagged catmon images.
MobileNetV2 was selected because it has a small 'footprint', allowing the
application to be deployed on a raspberry pi.  
[Catmon Image Classifier repo](https://github.com/terrydolan/catmon-img-classifier)  
  
Terry Dolan  
October 2023