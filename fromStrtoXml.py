from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
import os
import re

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
    #comment = Comment('Digital Humanities Work')
    #top.append(comment)
    teiHeader = SubElement(top, 'teiHeader')
    fileDesc = SubElement(teiHeader,'fileDesc')
    titleStmt = SubElement(fileDesc,'titleStmt')
    title = SubElement(titleStmt, 'title')
    title.text = songName + ' song'
    respStmt = SubElement(titleStmt,'respStmt')
    resp = SubElement(respStmt,'resp')
    resp.text = 'compiled by'
    name1 = SubElement(respStmt,'name')
    name2 = SubElement(respStmt,'name')
    name1.text = 'Yarden Vaknin'
    name2.text = 'Alex Mongait'
    orgName = SubElement(respStmt,'orgName',ref='https://www.cs.bgu.ac.il/~dhcs202/Main')
    orgName.text = 'Ben Gurion University ,Digital Humanities course by Dr. Yael Netzer'
    publicationStmt = SubElement(fileDesc,'publicationStmt')
    publisher = SubElement(publicationStmt,'publisher')
    publisher.text = 'AZlyrics'
    pubPlace = SubElement(publicationStmt,'pubPlace',ref = url)
    pubPlace.text = 'link to publisher website'
    sourceDesc = SubElement(fileDesc,'sourceDesc')
    bibl = SubElement(sourceDesc,'bibl')
    bibltitle = SubElement(bibl,'title', level='j')
    bibltitle.text = songName
    author = SubElement(bibl,'author')
    author.text = songWriter
    biblPublisher = SubElement(bibl,'publisher')
    biblPublisher.text = 'Album' + albumName
    date = SubElement(bibl ,'date')
    fixed_year = yearOfAlbum[2]+yearOfAlbum[3]+yearOfAlbum[4]+yearOfAlbum[5]
    date.text = 'Album publication year: '+fixed_year
    text = SubElement(top,'text')
    body = SubElement(text,'body')
    bodyHead = SubElement (body , 'head')
    bodyHead.text = songName    
    arr = lyrics.split("\n\n")
    for i in range(1,len(arr)):    #fileDesc.text = 'c'
        p = SubElement(body, 'p')
        lines = arr[i].split("\n")
        for line in range(0,len(lines)):
            l = SubElement(p,'l')
            l.text = lines[line]    
    #title = SubElement ()

#    child_with_tail = SubElement(top, 'child_with_tail')
 #   child_with_tail.text = 'This child has regular text.'
  #  child_with_tail.tail = 'And "tail" text.'

   # child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
   # child_with_entity_ref.text = 'This & that'
   
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        
    xml_str  = (prettify(top))
    #save_path_file = "yarden.xml"
    
    with open(path, "w") as f: 
        f.write(xml_str)

#createFile()


