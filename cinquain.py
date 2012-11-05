"""
generates a Cinquain from the stored token data.
cinquain is a poetic form with a 5 line pattern
the form I am using here is Tanka - an unrhymed syllable pattern of 5-7-5-7-7
"""
import curses, nltk, re, sys, json
from curses.ascii import isdigit
from nltk import NgramModel
from nltk.corpus import cmudict
from nltk.probability import WittenBellProbDist


dictionary= cmudict.dict()

#utilizes CMU Pronunciation Dictionary to count syllables by counting those marked for stress with an integer
#returns the minimum syllable count to accomodate words with multiple pronunciations.
def syll_count(word):
    word = word.lower()
    try:
        return min([len(list(c for c in phoneme if isdigit(c[-1]))) for phoneme in dictionary[word]])
    except KeyError:
        #word not found in CMU dict...
        #time to roll our own way of counting syllables
        
        #first try splitting word by vowels and counting 
        array = re.split("[^aeiouy]+", word)
       
        for i, x in enumerate(array):
            if x == '':
                del array[i]
        
        count = len(array)

        #remove (likely) silent 'e' from the syllable count
        if word[-1] == 'e' and count > 1:
            count -= 1

        return count


  
def generate(body_tokens):
    #return a 5 line string object following the Cinquain syllable pattern.
    #stores the pattern rule for the Cinquain
    #this could be parameterized to handle other formats
    syl_per_line = [5,7,5,7,7]
    line_syl_counts=[0]*len(syl_per_line)
    lines=[""]*len(syl_per_line)

    #much like the generator code for random article text
    estimator = lambda fdist, bins: WittenBellProbDist(fdist,len(fdist)+1)
    source = NgramModel(min(syl_per_line) ,body_tokens, estimator)
    seed_words = source.generate(100)[-2:] 
    generated_text = source.generate(sum(syl_per_line)*2, seed_words)
    

  
    for i in range(len(syl_per_line)):
        target = syl_per_line[i]
        while True:
            word = generated_text[0]
            s = syll_count(word)            
            if (s + line_syl_counts[i] < target):
                line_syl_counts[i] += syll_count(word)
                lines[i] += word + " "
                word = generated_text.pop(0)
            elif (s + line_syl_counts[i] == target):
                line_syl_counts[i] += syll_count(word)
                lines[i] += word + " "
                word = generated_text.pop(0)
                break
            else:
                word = generated_text.pop(0)
                break
            
            

    for i, text in enumerate(lines):
        if line_syl_counts[i] < syl_per_line[i]:
            target = syl_per_line[i] - line_syl_counts[i]
            for word in (generated_text):
                if syll_count(word) == target:
                    text += word 
                    break  

           
    return "\n".join(lines)




if __name__ == '__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'foxNewsInputSet.json'

    #read the pre-processed tokens back from json serialization
    with open(filename, 'r') as fp:
       tokens = json.load(fp)

    body_tokens = tokens["body_tokens"]

    print generate(body_tokens)

      

