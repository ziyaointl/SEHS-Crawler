# This code is only experimental and does not function properly

import urllib.request
import os
import re

def getCurrentFolder(inputString):
    if inputString != "/":
        while inputString.find("/") != -1:
            inputString = inputString[inputString.find('/') + 1:]
    return inputString

outputFile = open("output.xml", "w+")
imgBaseURL = "http://www.sdshiyan.cn/english/upload/"
imgUploadedBase = "http://localhost:8888/wp-content/uploads/2016/12/"

urlList = [line.rstrip('\n') for line in open('newsURL.txt')]

# pattern = re.compile('<div id="content">(.+?)</div>')
pTagPattern = re.compile('<p>.+?</p>')
imgPattern = re.compile('src="../../upload/(.+?)"')
datePattern = re.compile('\d\d\d\d-\d\d-\d\d')
transPattern = re.compile('Translated by:  (.+?)<')
titlePattern = re.compile('<h1 class="aTitle">(.+?)</h1>')

# for url in urlList:
#     data = urllib.request.urlopen(url).read()

data = urllib.request.urlopen(urlList[1]).read()
data = str(data).replace("<br />", "")
data = str(data).replace("&nbsp;", " ")
data = str(data).replace("&amp;", "")
data = str(data).replace("\\xe2\\x80\\x9d", "\"")
data = str(data).replace("\\xe2\\x80\\x9c", "\"")
data = str(data).replace("\\xef\\xbc\\x82", "\"")
data = str(data).replace("\\xe2\\x80\\x98", "\"")
data = str(data).replace("\\xe2\\x80\\x99", "\"")
data = str(data).replace("&ldquo;", "\"")
data = str(data).replace("&rdquo;", "\"")
data = str(data).replace("&rsquo;", "\'")
data = str(data).replace("&lsquo;", "\'")

imageList = imgPattern.findall(data)
paragraphList = pTagPattern.findall(data)
date = datePattern.findall(data)
translators = transPattern.findall(data)
title = titlePattern.findall(data)

outputFile.write("<Post>" + "\n")

outputFile.write("<Title>" + "\n")
outputFile.write(title[0] + "\n")
outputFile.write("</Title>" + "\n")

outputFile.write("<Translators>" + "\n")
outputFile.write(translators[0] + "\n")
outputFile.write("</Translators>" + "\n")

outputFile.write("<Date>" + "\n")
outputFile.write(date[0] + "\n")
outputFile.write("</Date>" + "\n")

outputFile.write("<Content>" + "\n")
for p in paragraphList:
    if p.find("<span") == -1 & p.find("<img") == -1:
        outputFile.write(p + "\n")
if len(imageList) > 1:
    for x in range (1, len(imageList)):
        outputFile.write("<img scr=\"" + imgUploadedBase + "\" />")
    outputFile.write("\n")
outputFile.write("</Content>" + "\n")

outputFile.write("<Images>" + "\n")
for imgURL in imageList:
    imgURL = imgBaseURL + imgURL
    outputFile.write(imgURL + ";")
outputFile.write("\n" + "</Images>" + "\n")

outputFile.write("</Post>")
outputFile.write("\n\n")

print(getCurrentFolder(imageList[0]))

# directory = os.getcwd()
# currentFolder = os.getcwd()
# if os.getcwd() != "/":
#     while currentFolder.find("/") != -1:
#         currentFolder = currentFolder[currentFolder.find('/') + 1:]
#     directory = directory[:-len(currentFolder)]
# print(directory)
# print(currentFolder)


