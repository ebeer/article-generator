"""
My first python program.
Structured to allow me to explore the language features and learn.

"""
import json
import getopt
import nltk
from nltk import util
from nltk import word_tokenize


#constants - some may be well suited to command line options
GENERATED_TEXT_LENGTH = 100
NGRAM_LENGTH = 2
URL_START_STRINGS = ['http://','https://']



#calls the nltk libraries to strip html tags from the contect at the given url
#returns token set for that content set
#simply ignores url strings that do not start with either "http://" or "https://"
def tokenizeContentFromURL (url):  
    for pattern in URL_START_STRINGS:  
        if url.startswith(pattern):
            tree = util.clean_url(url)
            tokens_from_url = word_tokenize(tree) #this is _so_ much easier than I thought it was
            break
        else:
            tokens_from_url = ''

    return tokens_from_url





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

for url in url_list:
    tokens.extend(tokenizeContentFromURL(url))
    

#save the tokenized data out
#TODO - new problem - special charactes in escaped html are not playing nicely with the json uf encoding!
with open('tokenizedData.json', 'w') as fp:
    json.dump(tokens, fp, encoding='latin1')


    







    
