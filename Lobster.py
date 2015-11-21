# Author: Kyle Busdieker
# Purpose:
#         A program that lets the user choose which songs he/she wants to download from
#         a Youtube music mix video.

from pytube import YouTube
from pprint import pprint
from bs4 import BeautifulSoup as bs
from moviepy.editor import *
import urllib, re, sys, os.path, threading, time

# this pattern is intended to match the timestamps given in a video's description for when each song begins
pattern = re.compile('[0-9]?[0-9]{1}:{1}[0-9]{1}[0-9]{1}:?[0-9]?[0-9]?')
fullVidDownloadLocation = 'temp_video_files/'

def getSongTimes(timestamps):
    songTimes = {}
    for x in range(0, len(timestamps)-1, 1):
        songTimes[x+1] = {'start': timestamps[x], 'end' : timestamps[x+1]}
    return songTimes

def makeTimestampsList(anchorTags):
    timestamps = []
    for link in anchorTags:
        # match text found in a tag with a regular expression that looks for a time
        matchFound = pattern.findall(link.text)
        if matchFound != []:
            timestamps.append(str(matchFound).strip('[\'\']'))
    return timestamps

def getAnchorTags(description):
    tags = description.find_all('a')
    return tags

def getVideoDescription(soup):
    description = soup.find(id='watch-description-text')
    return description

def createSoup(html):
    htmlSoup = bs(html, "lxml")
    return htmlSoup

def getPageHTML(url):
    webpage = urllib.request.urlopen(url)
    html = webpage.read()
    return html


if __name__ == '__main__':
    print("Welcome to the Youtube Mix song picker.")
    print("Type 'q', 'Q', 'quit', or 'exit' to close the program.\n")
    
    while(True):
        # print prompt for user get their input
        kbInput = input("Enter a youtube video URL: ")
        
        # check for exit command
        if kbInput == "q" or kbInput == "Q" or kbInput == "quit" or kbInput == "exit":
            print("Exiting...")
            raise SystemExit
        else:
            videoUrl = kbInput
            try:
                ytVid = YouTube(videoUrl)
            except Exception as err:
                print("\nThere was a problem with the provided URL. Check that the URL is valid.")
                print("Exception says: " + str(err) + "\n")
                continue
            
            try:
                vidToDownload = ytVid.get('mp4', '720p')
            except Exception as err:
                print("\n720p unavailable. Trying 480p...")
                try:
                    vidToDownload = ytVid.get('mp4', '480p')
                except Exception as err:
                    print("480p unavailable. Trying 360p...")
                    try:
                        vidToDownload = ytVid.get('mp4', '360p')
                    except Exception as err:
                        print("\nNo videos (of type mp4) are available. Unable to download video. Sorry!")
                        raise SystemExit
                    
            try:
                time.sleep(1)
                print("Downloading your video, please be patient.")
                downloadThread = threading.Thread(target = vidToDownload.download, args = (fullVidDownloadLocation, ))
                downloadThread.start()
                downloadThread.join()
                print("Video downloaded.")
            except Exception as err:
                print("\nThere was a problem downloading the video.")
                print("Exception says: " + str(err) + "\n")
                continue
            
            
            
            pprint(getSongTimes(makeTimestampsList(getAnchorTags(getVideoDescription(createSoup(getPageHTML(videoUrl)))))))
            
            
            #vidClip = VideoFileClip("C:/Users/Kyle/Code/Personal_Projects/Youtube_Mix_Downloader/temp_video_files/" + vid.filename + ".mp4")
            
            #song2 = vidClip.subclip(228, 512)
            #song2Audio = song2.audio
            #song2Audio.write_audiofile("/songs/song2.mp3")
            print("done")

"""
The plan is to extract the timestamps of each song in the video by looking at the times provided in the video's description by the uploader. The video will be downloaded and by will be separated based on the song lengths found from the description. The user will be able to select which songs they want 'downloaded' (even though the whole video will be downloaded) and those selected will be converted to MP3's put in a directory.

"""