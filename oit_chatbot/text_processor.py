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
        'dr niu\' office', 
        'where\'s dr. nius office',  
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
        print(noun_phraser(t))
        print()
