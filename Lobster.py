# Author: Kyle Busdieker
# Purpose:
#         A program that lets the user choose which songs he/she wants to download from
#         a Youtube music mix video.

from pytube import YouTube
from pprint import pprint
from bs4 import BeautifulSoup as bs
import urllib
import re

# this pattern is intended to match the timestamps given in a video's description for when each song begins
pattern = re.compile('[0-9]?[0-9]{1}:{1}[0-9]{1}[0-9]{1}:?[0-9]?[0-9]?')

def getPageHTML(url):
    webpage = urllib.request.urlopen(url)
    html = webpage.read()
    return html

def createSoup(html):
    htmlSoup = bs(html, "lxml")
    return htmlSoup

def getVideoDescription(soup):
    description = soup.find(id='watch-description-text')
    return description

def getAnchorTags(description):
    tags = description.find_all('a')
    return tags

def makeTimestampsList(anchorTags):
    timestamps = []
    for link in anchorTags:
        # match text found in a tag with a regular expression that looks for a time
        matchFound = pattern.findall(link.text)
        if matchFound != []:
            timestamps.append(str(matchFound).strip('[\'\']'))
    return timestamps

def getSongTimes(timestamps):
    songTimes = {}
    for x in range(0, len(timestamps)-1, 1):
        songTimes[x+1] = {'start': timestamps[x], 'end' : timestamps[x+1]}
    return songTimes
    

pprint(getSongTimes(makeTimestampsList(getAnchorTags(getVideoDescription(createSoup(getPageHTML("https://www.youtube.com/watch?v=FFFuqCuEfKQ")))))))


yt = YouTube("https://www.youtube.com/watch?v=b-b9Y_h6X7I")
#pprint(yt.get_videos())
print(yt.filename)
video = yt.get('mp4', '720p')
#video.download('C:/Users/Kyle/Downloads/')


"""
The plan is to extract the timestamps of each song in the video by looking at the times provided in the video's description by the uploader. The video will be downloaded and by will be separated based on the song lengths found from the description. The user will be able to select which songs they want 'downloaded' (even though the whole video will be downloaded) and those selected will be converted to MP3's put in a directory.

"""