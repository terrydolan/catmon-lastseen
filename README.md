# Catmon Last Seen App

## Introduction
The web app shows when Boo or Simba were last seen.
Boo and Simba are two cool cats with a twitter account!

The app parses the @boosimba tweets, which show the cat images from *catmon*,
and the tweet replies from the catmon image classifier that categorises the
cat as Boo, Simba or Unknown.

The associated images are enhanced and displayed.

To run:

```
    $streamlit run catmon_lastseen_app.py
```

## Related Catmon Projects

1. *Catmon*: a cat flap monitor application that takes a picture when a cat
enters through the cat flap, uploads the picture to google drive and tweets it
on @boosimba. The application is deployed on a raspberry pi.
1. *Catmon image tagger*: a web app that provides a UI to help classify the
catmon images as either 'Boo' or 'Simba' or 'Unknown'.
The results are saved to google drive.
1. *Catmon image classifier*: an application that processes the catmon images
and classifies the image as 'Boo', 'Simba' or 'Unknown' using a MobileNetV2
convolutional neural network.
The MobileNetV2 model uses transfer learning and was trained on the tagged
catmon images.
The application is deployed on a raspberry pi.

I created Catmon as a fun 'maker' project in ~2015.
The application is deployed on a raspberrypi and has been running continuously,
 tweeting cat images on @boosimba.

In 2022 I applied machine learning in order to automatically classify those
cat images.
The solution uses a convolutional neural network with a small footprint so
that it can be deployed on a raspberry pi.

Terry Dolan