import pytest

from oit_chatbot.text_processor import *
from textblob import TextBlob
from textblob.blob import Word

qs = {
    'Where is blackboard?' : ('where', ['blackboard']),
    'How do I upload grades?' : ('how', ['upload grade']),
    'When is the due date for financial aid?' : ('when', ['due date', 'financial aid']),
    'When is the due date for tuition?' : ('when', ['due date', 'tuition']),
    'When is the last day to drop classes?' : ('when', ['last day', 'class']),
    'When are my final exams?': ('when', ['final exam']),
    'What is the phone number for tech support?': ('what', ['phone number',  'tech support']),
    'Where is Dr. Niu\'s office?': ('where', ['dr niu',  'office']),
    'What are Dr. Niu\'s office hours?': ('what', ['dr niu', 'office hour']),
    'What is Dr. Niu\'s phone number?': ('what', ['dr niu', 'phone number']),
    'What is Dr. Niu\'s email address?': ('what', ['dr niu', 'email address']),
    'Where is degreeworks?': ('where', ['degreeworks']),
}
    

words = ( 
    (Word('hours', pos_tag='NNS'), 'hour'), 
    (Word('dates', pos_tag='NNS'), 'date'), 
    (Word('Dr.', pos_tag='NNP'), 'dr'),
    (Word('ran', pos_tag='VBD'), 'run'), 
    (Word('runs', pos_tag='VBZ'), 'run'),
    )


def test_standardize_word():
    for word_pair in words:
        w1 = word_pair[0]
        w2 = Word(word_pair[1])
        w1 = standardize_word(w1)
        print(w1, w2)
        assert w1 == w2

def test_questions():
    """Questions should be parsed correctly"""
    
    for question, answer in qs.items():
        q_word = find_question(TextBlob(question.lower()))
        assert q_word.lower() == answer[0]

def test_objects():
    for question, answer in qs.items():
        obj = find_objects(question.lower())
        assert obj == answer[1]
