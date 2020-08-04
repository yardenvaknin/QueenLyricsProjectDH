import os
import re
import codecs
import urllib.request 
from bs4 import BeautifulSoup,NavigableString, Tag
from xml.dom import minidom 
from fromStrtoXml import createFile

#using a dictionary to save the albums and publication years.
dict = {}

#create folders for each album and create an xml with tei for each song
def creatSongsFiles(url,dict,num):
    queenLyrics = urllib.request.urlopen(url)
    queenLyricsHtml = queenLyrics.read()
    queenLyrics.close()
    soup = BeautifulSoup(queenLyricsHtml)
    mydivs = soup.findAll("div", {"class": "album"})
    for album in mydivs:
        #create folder for each album
        try:
            album_name = album.findAll(text=True)[1]        
            if not os.path.exists(os.path.dirname(album_name+"/")):
                    os.makedirs(os.path.dirname(album_name+"/"))
            album_year = album.findAll(text=True)[2]
            dict[album_name] = album_year
        except:
            continue
    creatXmlsFiles(soup,num)

def creatXmlsFiles(soup,num):   
    listalbum = soup.findAll("div" ,{"class": "listalbum-item"})
    count = 0
    #iterates over all the alnbums and create xml file for each song.
    for i in listalbum:
        if (count < num and count != 170) :
            song_name = i.findAll(text=True)[0]
            href_song = i.find('a')
            href_url = href_song.get('href')
            fixAdress = "https://www.azlyrics.com"+href_url[2:]
            createSongXml(fixAdress,song_name,count) 
        count = count + 1 

#get the lyrics of the song
def getSongLyrics(soup,songName):
    for br in soup.find_all("br"):
        br.replace_with("\n")
    parsedText = soup.get_text()
    found = 0    
    lines = parsedText.split('\n')
    lyrics = ""
    count = 0
    done = 0
    for x in lines:
        st = x.strip() 
        if(st =="\""+songName+"\""):
            found = 1 
            count = 1
        if(st =="Submit Corrections"): 
           break
        if (found == 1):
            if(count == 1):
                lyrics = lyrics + st+"\n"  
            if(count > 3 and done == 1):
                lyrics = lyrics + st+"\n" 
            if(count == 2):          
                done = 1
            count = count + 1    
    return "\n".join(lyrics.split("\n")[:-22])    

#preserve the sturcture of the lyrics clean unnecessary empty lines
def fixLyrics(lyrics):
    arr = lyrics.split("\n")
    ans = ""
    ans = ans + arr[0] + "\n\n"
    for i in range(4,len(arr)):
        if (i < len(arr)-4):
            if(arr[i]== '' and arr[i+1]== '' and arr[i+2]== ''):
                ans = ans + arr[i]+ "\n"   
                i = i + 4
        if (i < len(arr)-1):      
             if (arr[i] != '' and arr[i+1] == ''):   
                ans = ans + arr[i] + "\n"  
                i = i + 1  
        if (i == len(arr)-1):
            ans = ans + arr[i]                  
    return ans

#get album name                
def findAlbumName(queenLyricsHtml,soup):
    songinalbum = soup.find("div", {"class": "songinalbum_title"})          
    albumdiv = songinalbum.find('b')
    albumName = albumdiv.findAll(text=True)[0]
    return albumName

#get song writer 
def findSongWriter(soup):
    songWriter = soup.findAll("div", {"class": "smt"})  
    writer = songWriter[2].findAll('small')[0].findAll(text=True)[0]
    return writer

def createSongXml(url,songName,count):
    queenLyrics = urllib.request.urlopen(url)
    queenLyricsHtml = queenLyrics.read()
    queenLyrics.close()
    soup = BeautifulSoup(queenLyricsHtml,"lxml")
    albumName = findAlbumName(queenLyricsHtml,soup)
    yearOfAlbum = dict.get(albumName)
    writer = findSongWriter(soup)  
    path = albumName+"/"+songName+".txt"
    lyrics = getSongLyrics(soup,songName)
    print(songName)
    path = albumName+"/"+songName+".xml"
    createFile(path,songName,albumName,fixLyrics(lyrics),writer,yearOfAlbum,url)

#this is the main function 
creatSongsFiles("https://www.azlyrics.com/q/queen.html",dict,10)

