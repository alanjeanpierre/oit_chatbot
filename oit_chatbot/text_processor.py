from textblob import TextBlob
from textblob.blob import Word
import string

"""List of non-standard "nouns" we want to target"""
NOUN_LIST = {
    'blackboard',
    'asap',
    'degreeworks',
    'oit',
}

def find_verb(sentence):
    pass

def find_objects(sentence):
    """Find the objects in a sentence based on noun-phrases"""
    objects = noun_phraser(TextBlob(sentence))
    #objects = sentence.noun_phrases
    return objects

def find_question(sentence):
    """Find the questionword in the sentence if there is one
        based on the part of speech tag. Question words start
        with W
    """
    for word, part_of_speech in sentence.pos_tags:
        if part_of_speech.startswith('W'):
            return word

def noun_phraser(sentence):  
    """Parses sentence to pick out a list of noun phrases

    Args:
        sentence (TextBlob) - sentence in the form of a textblob object
    
    Returns:
        list of str - list of noun-phrases. Could be an empty list

    The function iterates through each word in the sentence. 
    If the word is an adjective or a noun or in the list of
    non-standard words NOUN_LIST, it appends it to a temporary
    noun-phrase list. If the word isn't one of those, it appends
    whatever noun-phrase had been constructed to the list of noun-phrases
    to return.

    """  
    nouning = False
    noun_phrases = []
    nouns = []
    for word, part_of_speech in sentence.pos_tags:
        stdword = standardize_word(word)
        if nouning and not (part_of_speech.startswith(('NN', 'JJ', )) or stdword in NOUN_LIST):
            nouning = False
            noun_phrases.append(' '.join(nouns))
            nouns = []
        if part_of_speech.startswith(('NN', 'JJ', )) or stdword in NOUN_LIST:
            nouning = True
            nouns.append(stdword)
    if nouns:
        noun_phrases.append(' '.join(nouns))
    return noun_phrases

def standardize_word(word):
    """Returns standard form of a word, accounting for typos,
    plurals, synonyms, case, and any other form"""


    # This doens't work
    # corrects things like 'tuition' to 'suction'
    # word = word.correct()

    # finds the root of the word
    word = word.lemma
    
    #removes punctuation and case
    word = word.lower().translate(str.maketrans('', '', string.punctuation)) 
    return word

if __name__ == '__main__':
    qs = [
        'Where is blackboard?',
        'How do I upload grades?',
        'When is the due date for financial aid?', 
        'When is the due date for tuition?', 
        'When is the last day to drop classes?', 
        'When are my final exams?',
        'What is the phone number for tech support?', 
        'Where is Dr. Niu\'s office?', 
        'What are Dr. Niu\'s office hours?', 
        'What is Dr. Niu\'s phone number?', 
        'What is Dr. Niu\'s email address?', 
        'Where is degreeworks?',
        'degreeworks',
        'dr niu\'s office', 
        'where\'s dr. niu\'s office',  
        'How do I register for classes?',
        ]
        
    for q in qs:
        print(q)
        t = TextBlob(q)
        for w in t.pos_tags:
            print('{:10s}'.format(w[0]), end=' ')
        print()
        for w in t.pos_tags:
            print('{:10s}'.format(w[1]), end=' ')
        print()
        nouns = noun_phraser(t)
        print(nouns)
        print()
