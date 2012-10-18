"""
My first python program.
Structured to allow me to explore the language features and learn.

"""
import json
import getopt
import nltk
from nltk import NgramModel


#constants - some may be well suited to command line options
GENERATED_TEXT_LENGTH = 100
NGRAM_LENGTH = 2
URL_START_STRINGS = ['http://','https://']




#generates random text based on ngram analysis of the parsed data
#returned text is not a list - it is in paragraph format
def generateContentFromTokens(text_length, ngram_length, token_list):
    source_ngrams = NgramModel(ngram_length, token_list)
    seed_words = source_ngrams.generate(text_length)[-2:]
    generated_text = source_ngrams.generate(text_length, seed_words)
    return ' '.join(generated_text)


tokens =[]


#read the pre-processed tokens back from json serialization
with open('tokenizedData.json', 'r') as fp:
    tokens = json.load(fp)


print generateContentFromTokens(GENERATED_TEXT_LENGTH, NGRAM_LENGTH, tokens)


    



