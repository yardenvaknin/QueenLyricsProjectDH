from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
import os
import re


def createHTML(xmlstr,path,songName):
    contents = """
<!DOCTYPE html>
<html>
    <style> 
    body {
        background: #FFF;
        color: #111;
        font: 20px Baskerville, "Palatino Linotype", "Times New Roman", Times, serif;
        text-align: center;
        }      
    div, h1, h2, p {
        margin: 0;
        padding: 0;
    }
    div.heading {
        padding: 100px
    }
    titleStmt,sourceDesc,lg{
        white-space: pre-line;    
    }
    </style>
    <body>""" +'\n' +addTab(xmlstr) +"""    </body>
    </html>"""
    browseLocal(contents,songName+".html")

def addTab(xmlstr):
    splitted = xmlstr.split('\n') 
    ans = ""
    for i in range(0,len(splitted)-1):
        ans = ans +"    "+ splitted[i]+'\n'
    return ans    

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    #webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac


def Remove(xml_str):
    splitted = xml_str.split('\n') 
    ans = ""
    for i in range(1,len(splitted)-1):
        ans = ans + splitted[i]+'\n'
    return ans   

#this function prettify the xml's by adding tabs
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#create xml file with TEI format as we learned at the course
def createFile(path,songName,albumName,lyrics,songWriter,yearOfAlbum,url):
    top = Element('TEI',xmlns='http://www.tei-c.org/ns/1.0')
    teiHeader = SubElement(top, 'teiHeader')
    fileDesc = SubElement(teiHeader,'fileDesc')
    titleStmt = SubElement(fileDesc,'titleStmt')
    title = SubElement(titleStmt, 'title')
    title.text = songName + ' song'
    respStmt = SubElement(titleStmt,'respStmt')
    resp = SubElement(respStmt,'resp')
    resp.text = 'Compiled by:'
    name1 = SubElement(respStmt,'name')
    name2 = SubElement(respStmt,'name')
    name1.text = 'Yarden Vaknin'
    name2.text = 'Alex Mongait'
    orgName = SubElement(respStmt,'orgName',ref='https://www.cs.bgu.ac.il/~dhcs202/Main')
    orgName.text = 'Ben Gurion University ,Digital Humanities course by Dr. Yael Netzer'
    publicationStmt = SubElement(fileDesc,'publicationStmt')
    publisher = SubElement(publicationStmt,'publisher')
    publisher.text = 'Publisher: AZlyrics'
    pubPlace = SubElement(publicationStmt,'pubPlace',ref = url)
    pubPlace.text = ''
    sourceDesc = SubElement(fileDesc,'sourceDesc')
    bibl = SubElement(sourceDesc,'bibl')
    bibltitle = SubElement(bibl,'title', level='j')
    bibltitle.text = songName
    author = SubElement(bibl,'author')
    author.text = songWriter
    biblPublisher = SubElement(bibl,'publisher')
    biblPublisher.text = 'Album:' + albumName
    date = SubElement(bibl ,'date')
    fixed_year = yearOfAlbum[2]+yearOfAlbum[3]+yearOfAlbum[4]+yearOfAlbum[5]
    date.text = 'Album publication year: '+fixed_year
    text = SubElement(top,'text')
    body = SubElement(text,'body')
    div1 = SubElement(body,'div',type ='heading')
    head = SubElement(div1,'head')
    head.text = songName   
    div2 = SubElement(body,'div',type='lyrics')
    arr = lyrics.split("\n\n")
    for i in range(1,len(arr)):    
        p = SubElement(div2, 'lg')
        lines = arr[i].split("\n")
        for line in range(0,len(lines)):
            l = SubElement(p,'l')
            l.text = lines[line]   
   
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        
    xml_str  = (prettify(top))
    with open(path, "w") as f: 
        f.write(xml_str)
    createHTML(Remove(xml_str),path,songName)
        
 



