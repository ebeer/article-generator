import nltk
import urllib2, sys
import re
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString
from nltk import util
from nltk import word_tokenize

class Tokenizer:
    formats = []

    def tokenize(self, url):
        title_attr, body_attr = self.find_format(url)
        
        try:
            soup = BeautifulSoup(urlopen(url))    
            title = soup.find("h1", title_attr).text         
            body = soup.find("div", body_attr).text
            return (word_tokenize(title), word_tokenize(body))
        except:
            raise Exception("failure parsing url or html")

        

    def add_format(self, pattern, title, body):
        self.formats.append((re.compile(pattern), {"class" : re.compile(title)}, {"class" : re.compile(body)}))

                       

    def find_format(self, url):
        for f in self.formats:
            if f[0].search(url): return f[1:]
        return ({}, {})

    
        
                       
