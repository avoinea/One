#!/usr/bin/python
import re 
from jarowpy import jarow

def get_stop_words():
    #returns a list of Romanian stopwords from file
    with open("romanian.stoplist") as f:
         s_w = [line.strip('\n') for line in f]
    short = filter(lambda x: len(x) <= 3, s_w) 
    s_w = filter(lambda x: len(x) > 3, s_w)
   
    return (s_w,short)         

def get_words(alist):
    #Splits the initial string into lists of words 
    result = re.split("[,.?!:]", alist)
    result = map(lambda x: re.split(" ", x), result)
             
    return result

def get_imp_words(allist):
    #returns the important words from a list of words
    #an important word is one that contains capital letters
    result = []
    
    func = lambda x: len(x) > 0 and not x.islower()
    for list in allist:
         united = ""
         for word in list:
             if func(word):
                 united += word + " "
             else:
                 if united:
                     result.append(united)
                     united = ""
         if united:
             result.append(united)
      
    return result

def contains(alist, x):
    for element in alist:
        if element == x:
            return True
    return False

def contains_pro(alist, x):
    for element in alist:
        if jarow(element, x, 0.3) > 0.9:
            return True
    return False

def process(alist, stop):
    #eliminates irrelevant words from the lists
    newlist = []
    func1 = lambda x: len(x) > 3
    func3 = lambda x: x.lower()
    func2 = lambda x: not contains(stop,x)
 
    for list in alist:
        aux = filter(func1, list)
        aux = filter(func2, aux)
        aux = map(func3, aux)
        newlist.append(aux)
    return newlist    
    
def intersect(alist, anotherlist):
    #return the common elements from the union of each list's sublists
    aset = set().union(*alist)
    anotherset = set().union(*anotherlist)
   
    return list(aset.intersection(anotherset))

#def combine(alist):
    #returns a list of important word sequences
 #   result = []
  #  for list in alist:
   #     result.append(" ".join(list))
   # return result

def sort_intersect(title, abstract, is_important = None):
    #returns a sorted (by relevance according to title) intersection
    #if is_important is non None, the abstract is so important that it will
    #only be sorted
     
    top = []
    rest = []
        
    for group in abstract:
        similar = get_similar(group, title)
        if similar:
             top.append(group)            
        else:
            rest.append(group)
 
    return top + rest
    

def is_similar(word, group):
    #tests wether a word is similar to any from a group of words
    for aword in re.split(' ', group):
        if jarow(word, aword) > 0.9:
            return True
    return False

def get_similar(group, title):
    #returns word from title that is most similar to any of the words in group
    for word in  title:
        if is_similar(word, group):
            return word
    return ''

def is_similar_to_any(word, lgroup):
    for group in lgroup:
        if is_similar(word, group):
            return True
    return False


def get_less_imp_words(title, labstract):
    #Returns common words from title and abstract
    last = filter(lambda x: len(x) <=3, labstract) 
    abstract = map(lambda x: " ".join(x), last)    
    result = sort_intersect(title, abstract)
    
    return result

def get_rest(title):
    #Returns the words that were not selected before
    result = filter(lambda x: len(x) > 3, title)
    result = sorted(result, key = lambda x: -len(x))
    return result
    

def difference(alist, toremove):
    #Returns the elements in alist that are not similar to any of the elements
    #in toremove
    result = []
    for list in alist:
        result. append(filter(lambda x: not is_similar_to_any(x, toremove), list))
                    
    return result
        

def get_search_words(L1 = None, L2 = None):
    #Creates 4 lists of important words
    #1.important_words -  a list with the most important words: names, 
    #abbreviations and acronyms; OBS: these words are extracted only from 
    #the abstract
    #2.less important words - a list containing common words from the two
    #lists
    #3. less important than the less important words - a list of possible 
    #relevant combinations of words
 
    first = re.split('[,. !?:]', L1)
    second = get_words(L2)  
    #1. 
    important_words = sort_intersect(first, get_imp_words(second), first)
    important_words = map(lambda x: x.lower(), important_words)
    print important_words
    #TODO De scos stop words care incep cu majuscula! 
    
    #2.
    (stop_words, short) = get_stop_words()
    important_words = filter(lambda x: contains(short, x), important_words)
    print important_words
    proc_title =  process([first], stop_words)
    proc_abstract = process(second, stop_words)
    print process([important_words], stop_words)
    proc_title = difference(proc_title, important_words)
    proc_abstract = difference(proc_abstract, important_words)

    func = lambda x: len(x) > 0
    less_important_words = get_less_imp_words(proc_title[0], proc_abstract)
    less_important_words = filter(func, less_important_words)
    print less_important_words
    #3. 
    proc_title = difference(proc_title, less_important_words)
    proc_abstract = difference(proc_abstract, less_important_words)

    not_important_words = get_rest(proc_title[0])
    not_important_words = filter(func, not_important_words) 
    print not_important_words
    return [important_words, less_important_words, not_important_words]


