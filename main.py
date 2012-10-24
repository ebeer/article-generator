"""
Process urls from a file
save tokenized data for later use

"""
import json
import urllib2, sys
from tokenizer import Tokenizer

#maps individual styles from the url patterns
#first element is the domain
#second is the class value of the article title h1 tag
#third is the class value of the article body tag
formats = [('foxnews.com', 'entry-title', 'article-text'),
           ('techcrunch.com', 'headline', 'body-copy'),
           ('nbcnews.com', 'gl_headline', 'articleText')]




if __name__ == '__main__':

    tokenizer = Tokenizer()

    for pattern in formats:
        tokenizer.add_format(*pattern)
        
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'foxNewsInputSet.txt'
        
    if '.' in filename:
        output_file = filename[:filename.index('.') +1] + 'json'
    else:
        output_file = filename + '.json'
        
  
    url_list = [ x.strip('\n') for x in open(filename) ]

    #initialize our list for the tokenized content
    tokens = []
    title_tokens = []

    for url in url_list:
        try:
            new_title, new_content = tokenizer.tokenize(url)
            title_tokens.extend(new_title)
            tokens.extend(new_content)
        except:
            pass #ignoring errors and continuing with parsing
        

    #save the tokenized data out
    with open(output_file, 'w') as fp:
        json.dump({"body_tokens" : tokens, "title_tokens": title_tokens}, fp)
    
    print "data saved to "+ output_file
#    print string with the output file name to the user
#







    
