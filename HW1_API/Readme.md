# Assignment 1

Build a library (preferable in python) that downloads images from a twitter feed, convert them to a video and describe the content of the images in the video.

## Twitter API to access the twitter content

This is the guideline: 
https://miguelmalvarez.com/2015/03/03/download-the-pictures-from-a-twitter-feed-using-python/

I used @CuteAnimaIPic twitter account to be an example.

In this part, we use tweepy to get the urls of the images. 
(tweepy: https://miguelmalvarez.com/2015/03/03/download-the-pictures-from-a-twitter-feed-using-python/)
```
pip install tweepy
```

And then, we use wget to download the image to local file. 
(wget: https://pypi.python.org/pypi/wget)
```
 import wget
```

## FFMPEG to convert images to videos

Use the system command:
```
import os

cmd = "command for FFMPEG"
os.system(cmd)
```

## Google Vision analysis to describe the content

Here is the guideline: https://cloud.google.com/python/

Choose "Analyze images with Cloud Vision API"
```
pip install google-cloud-vision
```
Download a private key as JSON. Then:
```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
