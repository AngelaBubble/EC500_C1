


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
    consumer_key = "*"
    consumer_secret = "*"
    access_token = "*-ZtCaU3ofNCNZg3tDe21MOAPo7A2IeBe"
    access_secret = "*"

def get_all_tweets(screen_name,number_tweets):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status
 
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
 
    api = tweepy.API(auth)
    DIRECTORY = os.getcwd()

    # Checking if there is already an output movie file
    os.system('rm output.mp4')
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    # Gathering twitter data
    try:
        alltweets = api.user_timeline(screen_name=screen_name,          # Gather first set of tweets
                               count=number_tweets, include_rts=False,
                               exclude_replies=True)
    except:
        print('This username does not exist. \n')
        return 'This username does not exist.'

    max_id = alltweets[-1].id
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

    if len(media_files) == 0:
        print('There are no images in these tweets')
        return 'There are no images in these tweets'
    #download image
    media_names = set()
    for media_file in media_files:
        filename = media_file.split("/")[-1]
        media_names.add(filename)
        wget.download(media_file)
    #file.close()
    print (media_names)

    #convert image to video
    os.system('cat *.jpg | ffmpeg -f image2pipe -framerate .5 -i - output.mp4')

    #describe the content of the images
    # Create a Vision client.
    labels_dict = {}
    path = glob.glob('*.jpg')
    client = vision.ImageAnnotatorClient()
    count = 0

    # TODO (Developer): Replace this with the name of the local image
    # file to analyze.
    for image_file_name in media_names:
        with io.open(image_file_name, 'rb') as image_file:
            content = image_file.read()

         # Use Vision to label the image based on content.
        image = google.cloud.vision.types.Image(content=content)
        response = vision_client.label_detection(image=image)
        labels_dict[str(count)] = []
        #print('Labels:')
        for label in response.label_annotations:
            #print(label.description)
            labels_dict[str(count)].append(label.description)
        count += 1
    return labels_dict 







if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@CuteAnimaIPic",number_tweets)
