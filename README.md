# Catmon Last Seen App

## Introduction
The *Catmon Last Seen* web app shows when Boo or Simba were last seen.
Boo and Simba are two cool cats with a twitter account!

The app parses [@boosimba tweets](https://twitter.com/boosimba), which show 
the cat images from *Catmon*, and the tweet replies from the *Catmon Image 
Classifier*.

The associated cat images are enhanced and displayed.

The app is built using python, streamlit, tweepy, requests and PIL.

## Key Project Files
The 'catmon\_lastseen\_app.py' is the main python application, with helper 
functions in 'utils.py'.

## Run the app
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/terrydolan/catmon-lastseen/main/catmon_lastseen_app.py)

## Catmon Last Seen Output
Here is an example of the app's output:  
<img src="https://raw.githubusercontent.com/terrydolan/catmon-img-classifier/main/images/catmon_lastseen_example_2022-08-10_111800.jpg" 
width="300">

## Related Catmon Projects
1. *Catmon*: a cat flap monitor application that takes a picture when a cat
enters through the cat flap, tweets it on @boosimba and uploads the image
to google drive. 
The application has been running since 2015 on a raspberry pi model B rev 2.  
[Catmon repo](https://github.com/terrydolan/catmon)
1. *Catmon Image Tagger*: a web app that provides a UI to help tag a set of 
catmon images as either 'Boo' or 'Simba' or 'Unknown'.
The results are saved to google drive.  
[Catmon Image Tagger repo](https://github.com/terrydolan/catmon-img-tag)
1. *Catmon image classifier*: an application that processes the new catmon 
tweets and classifies the associated image as 'Boo', 'Simba' or 'Unknown' 
using a trained MobileNetV2 convolutional neural network (CNN).
The image classification is tweeted as a reply to the catmon tweet.
The MobileNetV2 model applies transfer learning and was trained, validated and 
tested  using the tagged catmon images.
MobileNetV2 was selected because it has a small 'footprint', allowing the
application to be deployed on a raspberry pi.  
[Catmon Image Classifier repo](https://github.com/terrydolan/catmon-img-classifier)

Terry Dolan  
August 2022
