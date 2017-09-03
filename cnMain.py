import urllib.request
import bs4 as bs
import re


# Gets the last string after "/"
def get_current_folder(input_string):
    if input_string != "/":
        while input_string.find("/") != -1:
            input_string = input_string[input_string.find('/') + 1:]
    return input_string

# Declaration will be inserted to the start of each article
declaration = "This article was automatically crawled from the old Shandong Experimental High School's English Website by SEHS Crawler and is for archival purposes only. Its contents may be outdated and/or no longer relevant."
urlList = [line.rstrip('\n') for line in open('cnURL.txt')]  # Reads a list of urls from cnURL.txt
outputFile = open("outputCN.csv", "w+")  # Opens the output file
outputFile.write("title`date`content`img\n")  # Writes the column names

for link in urlList:
    source = urllib.request.urlopen(link).read()  # Reads URL list
    print("Crawling " + link)
    soup = bs.BeautifulSoup(source, 'lxml')
    outputFile.write(soup.title.text + "`")  # Outputs title

    # Matches and outputs date
    datePattern = re.compile('\d\d\d\d-\d\d-\d\d')
    date = datePattern.findall(str(soup))
    for text in date:
        outputFile.write(text + "`")

    soup = bs.BeautifulSoup(str(soup.find_all(id='content')), 'lxml')  # Strips out content div

    # Replaces all br tags with spaces
    for br in soup.select('br'):
        br.insert_after(" ")
        br.unwrap()

    imgBaseURL = "http://www.sdshiyan.cn/upload/"
    imgUploadedBase = "http://intl.cn.sehs.science/wp-content/uploads/2017/07/"
    imgPattern = re.compile('src="../../../upload/(.+?)"')
    emptyPattern = re.compile('\S+?')
    imgList = []

    # outputFile.write("<p class=\"declaration\">" + declaration + "</p>")  # Outputs declaration

    # Outputs content
    for text in soup.find('div').find_all(True, recursive=False):
        for element in text.find_all('img'):
            outputFile.write("<img src=\"" + imgUploadedBase + get_current_folder(element['src']) + "\" />")
            imgList.append(imgPattern.findall(str(element))[0])
        if len(emptyPattern.findall(text.text)) > 0:
            outputFile.write("<p>" + str(text.text).replace("\n", " ") + "</p>")
    outputFile.write("`")

    # Outputs img links
    for url in imgList:
        outputFile.write(imgBaseURL + url + ";")
    if len(imgList) == 0:
        outputFile.write("http://intl.cn.sehs.science/wp-content/uploads/2016/12/placeholder_600x400.png" + ";")
    outputFile.write("\n")
