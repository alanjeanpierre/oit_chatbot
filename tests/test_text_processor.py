import pytest

from oit_chatbot.text_processor import *
from textblob import TextBlob

qs = {
    'Where is blackboard?' : ('where', ['blackboard']),
    'How do I upload grades?' : ('how', ['upload grades']),
    'When is the due date for financial aid?' : ('when', ['due date', 'financial aid']),
    'When is the due date for tuition?' : ('when', ['due date', 'tuition']),
    'When is the last day to drop classes?' : ('when', ['last day', 'classes']),
    'When are my final exams?': ('when', ['final exams']),
    'What is the phone number for tech support?': ('what', ['phone number',  'tech support']),
    'Where is Dr. Niu\'s office?': ('where', ['dr. niu',  'office']),
    'What are Dr. Niu\'s office hours?': ('what', ['dr. niu', 'office hours']),
    'What is Dr. Niu\'s phone number?': ('what', ['dr. niu', 'phone number']),
    'What is Dr. Niu\'s email address?': ('what', ['dr. niu', 'email address']),
    'Where is degreeworks?': ('where', ['degreeworks']),
}
    

    


def test_questions():
    """Questions should be parsed correctly"""
    
    for question, answer in qs.items():
        q_word = find_question(TextBlob(question.lower()))
        assert q_word.lower() == answer[0]

def test_objects():
    for question, answer in qs.items():
        obj = find_object(question.lower())
        assert obj == answer[1]