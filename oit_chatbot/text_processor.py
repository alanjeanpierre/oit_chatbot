from textblob import TextBlob

NOUN_LIST = {
    'blackboard',
    'asap',
    'degreeworks',
}

def find_verb(sentence):
    pass

def find_objects(sentence):
    objects = noun_phraser(TextBlob(sentence))
    #objects = sentence.noun_phrases
    return objects

def find_question(sentence):
    for word, part_of_speech in sentence.pos_tags:
        if part_of_speech.startswith('W'):
            return word

def noun_phraser(sentence):    
    nouning = False
    noun_phrases = []
    nouns = []
    for word, part_of_speech in sentence.pos_tags:
        if nouning and not (part_of_speech.startswith(('NN', 'JJ', )) or word.lower() in NOUN_LIST):
            nouning = False
            noun_phrases.append(' '.join(nouns))
            nouns = []
        if part_of_speech.startswith(('NN', 'JJ', )) or word.lower() in NOUN_LIST:
            nouning = True
            nouns.append(word)
    if nouns:
        noun_phrases.append(' '.join(nouns))
    return noun_phrases