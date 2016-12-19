# This program crawls a list of news articles in Shandong Experimental High School's website and saves it into
# newsURL.txt
# Currently the website only has 8 pages of news, you can manually change the for loop on line 18 to crawl more pages

import urllib.request
import re

base = "http://www.sdshiyan.cn/english/news/default"  # Base for the catalog url
p = "p"
tail = ".htm"
catalog = [base + tail]  # A list of urls for the catalog pages
catalogData = []

# Creates regex expressions
pattern = re.compile(r'<div class="title">.*</div>')
hrefPattern = re.compile('href="(.+?)"')

# Completes the rest of the catalog url list
for x in range(2, 9):
    catalog.append(base + p + str(x) + tail)

# Crawls all the catalog pages in "catalog" and stores them into catalogData
for url in catalog:
    data = urllib.request.urlopen(url).read()
    data = data.decode('UTF-8')
    catalogData.append(pattern.findall(data))

# Opens the output file
outputFile = open("newsURL.txt", "w+")

# Finds all the href properties
urlList = hrefPattern.findall(str(catalogData))

# Initializes a new base for the url
newBase = "http://www.sdshiyan.cn/english"

# Appends the urls to change them from relative to absolute and stores the results in the opened file
for url in urlList:
    outputFile.write(newBase + url[2:] + "\n")
    print(newBase + url[2:] + "\n")

# Closes the output file
outputFile.close()
