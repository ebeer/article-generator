"""
My first python program.
Structured to allow me to explore the language features and learn.

"""
import json
import getopt
import nltk
from nltk import NgramModel
from nltk.probability import WittenBellProbDist



#generates random text based on ngram analysis of the parsed data
#returned text is not a list - it is in paragraph format
def generateContentFromTokens(text_length, ngram_length, token_list):
    estimator = lambda fdist, bins: WittenBellProbDist(fdist,len(fdist)+1)
    source_ngrams = NgramModel(ngram_length,token_list,estimator)

    seed_words = source_ngrams.generate(text_length)[-2:] 
    generated_text = source_ngrams.generate(text_length, seed_words)
    return ' '.join(generated_text)




if __name__ == '__main__':

    filename = "foxNewsInputSet.json"
    #constants 
    GENERATED_TEXT_LENGTH = 400
    GENERATED_TITLE_LENGTH = 10
    NGRAM_LENGTH = 5

    #read the pre-processed tokens back from json serialization
    with open(filename, 'r') as fp:
       tokens = json.load(fp)

    body_tokens = tokens["body_tokens"]
    title_tokens = tokens["title_tokens"]

    print generateContentFromTokens(GENERATED_TITLE_LENGTH, NGRAM_LENGTH, title_tokens) +'\n'

    print generateContentFromTokens(GENERATED_TEXT_LENGTH, NGRAM_LENGTH, body_tokens)


    



