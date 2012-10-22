"""
Pocess urls from a file
save tokenized data for later use

"""
import json
import getopt
import nltk
import urllib2, sys
import re
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString
from nltk import util
from nltk import word_tokenize


#constants - some may be well suited to command line options
NGRAM_LENGTH = 2

FOX_NEWS_ARTICLE_DIV = "article-text"
FOX_NEWS_TITLE_DIV = "entry-title"

TECH_CRUNCH_ARTICLE_DIV = "body-copy"
TECH_CRUNCH_TITLE_DIV = "headline"

MSNBC_ARTICLE_DIV = "articleText"
MSNBC_TITLE_DIV = "gl_headline"


#calls the nltk libraries to strip html tags from the contect at the given url
#returns token set for that content set - title and body text are treated separately
#supresses errors int data to generate empty strings
def tokenizeContentFromURL(url, div_article_pattern, div_title_pattern):
    title_tokens_from_url = ""
    article_tokens_from_url = ""

    try:
        soup = BeautifulSoup(urlopen(url))    
        title_div = soup.find("h1", {"class" : re.compile(div_title_pattern)}).text 
        title_tokens_from_url = word_tokenize(title_div)    
        content_div = soup.find("div", {"class" : re.compile(div_article_pattern)}).text
        article_tokens_from_url = word_tokenize(content_div) #this is _so_ much easier than I thought it was       
    except:
        pass
    
    return (article_tokens_from_url, title_tokens_from_url)





#opens the selected file and reads each line into our array of urls
#presumes one complete url per line and strips the newline chars
def readURLListFromFile(filename):
    #initialize our list of urls to process
    input_list = []
    url_list = []

    try:
        a = open(filename, "r")
    except IOError:
        print "unable to find input file " + filename
        return ""
    
    input_list = a.readlines()

    for url in input_list:
        url_list.append (url.strip('\n')) #removing newline characters from the lines

    return url_list





url_list = readURLListFromFile("inputList.txt")

#initialize our list for the tokenized content
tokens = []
title_tokens = []

for url in url_list:
    new_content, new_title = tokenizeContentFromURL(url, FOX_NEWS_ARTICLE_DIV, FOX_NEWS_TITLE_DIV)
    tokens.extend(new_content)
    title_tokens.extend(new_title)


#save the tokenized data out
#TODO - new problem - special charactes in escaped html are not playing nicely with the json uf encoding!
with open('tokenizedArticleData.json', 'w') as fp:
    json.dump(tokens, fp, encoding='latin1')

with open('tokenizedTitleData.json', 'w') as fp:
    json.dump(title_tokens, fp, encoding='latin1')


    







    
