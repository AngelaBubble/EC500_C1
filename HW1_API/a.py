


import tweepy #https://github.com/tweepy/tweepy
from tweepy import OAuthHandler
import json
import wget
import os
import io
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import bigquery
import google.cloud.vision


#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""


def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status
 
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profil
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse
    # You need to do it for all the models you need
 
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
 
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print ("...%s tweets downloaded so far" % (len(alltweets)))
       
    #write tweet objects to JSON
    #file = open('tweet.json', 'w')
    #print "Writing tweet objects to JSON please wait..."
    #for status in alltweets:
#    json.dump(status._json,file,sort_keys = True,indent = 4)
    media_files = set()
    for status in alltweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])
    
    #close the file
    print (media_files)

    #download image
    media_names = set()
    for media_file in media_files:
        filename = media_file.split("/")[-1]
        media_names.add(filename)
        wget.download(media_file)
    #file.close()
    print (media_names)

    #convert image to video
    for filename in media_names:
        output = filename.replace(".jpg",".mp4")
        cmd = "ffmpeg -loop 1 -i " + filename + " -c:a libfdk_aac -ar 44100 -ac 2 -vf \"scale='if(gt(a,16/9),1280,-1)\':\'if(gt(a,16/9),-1,720)\', pad=1280:720:(ow-iw)/2:(oh-ih)/2\" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 " + output
        os.system(cmd)

    #describe the content of the images
    # Create a Vision client.
    vision_client = google.cloud.vision.ImageAnnotatorClient()
    file = open('resul.txt', 'w')   #vision_client = vision.Client()

    # TODO (Developer): Replace this with the name of the local image
    # file to analyze.
    for image_file_name in media_names:
        with io.open(image_file_name, 'rb') as image_file:
            content = image_file.read()

         # Use Vision to label the image based on content.
        image = google.cloud.vision.types.Image(content=content)
        response = vision_client.label_detection(image=image)
        file.write("Labels for " + image_file_name + " :\n")
        #print('Labels:')
        for label in response.label_annotations:
            #print(label.description)
            file.write(label.description + "\n")







if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@CuteAnimaIPic")
