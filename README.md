# Catmon Last Seen App

## Introduction
The web app shows when Boo or Simba were last seen.
Boo and Simba are two cool cats with a twitter account!

The app parses the @boosimba tweets, which show the cat images from *catmon*,
and the tweet replies from the *catmon image classifier*.

The associated images are enhanced and displayed.

## Run the app
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/terrydolan/catmon-lastseen/main/catmon_lastseen_app.py)

## Related Catmon Projects
1. *Catmon*: a cat flap monitor application that takes a picture when a cat
enters through the cat flap, tweets it on @boosimba and uploads the picture 
to google drive. 
The application is deployed on a raspberry pi.
1. *Catmon image tagger*: a web app that provides a UI to help classify a 
selection of old catmon images as either 'Boo' or 'Simba' or 'Unknown'.
The results are saved to google drive.
1. *Catmon image classifier*: an application that processes the new catmon 
tweets and classifies the associated image as 'Boo', 'Simba' or 'Unknown' 
using a trained MobileNetV2 convolutional neural network (CNN).
The image classification is tweeted as a reply to the catmon tweet.
The MobileNetV2 model applies transfer learning and was trained, validated and 
tested  using the tagged catmon images.
MobileNetV2 was selected because it has a small 'footprint', allowing the
application to be deployed on a raspberry pi.

Terry Dolan  
August 2022