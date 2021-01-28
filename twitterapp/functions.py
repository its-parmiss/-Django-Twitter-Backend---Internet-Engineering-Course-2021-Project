
import os
import sys
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/{instance.dir}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"
    
# function to print all the hashtags in a text 
def extract_hashtags(text): 
      
    # initializing hashtag_list variable 
    hashtag_list = [] 
      
    # splitting the text into words 
    for word in text.split(): 
          
        # checking the first charcter of every word 
        if word[0] == '#': 
              
            # adding the word to the hashtag_list 
            hashtag_list.append(word[1:]) 
    return hashtag_list