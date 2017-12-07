import sqlite3
from oit_chatbot import oit_chatbot

def find_question(noun_phrases):
    
    db = oit_chatbot.get_db()
    
    answers = []
    
    if not noun_phrases:
        raise LookupError('No noun phrases found')
    elif len(noun_phrases) == 1:
        cursor = db.execute('select answer from knowledge where topic = ?', 
                            (noun_phrases))
        answers = cursor.fetchall()
    else:
        cursor = db.execute('select answer from knowledge where topic = ? and qualifier = ?', 
                            ( noun_phrases[-1], noun_phrases[-2]) )
        answers = cursor.fetchall()
        if not answers: # nothing with that qualifier, try just the topic
            cursor = db.execute('select answer from knowledge where topic = ?', 
                            (noun_phrases[-1]))
    
    if not answers:
        raise LookupErorr('No answers for that question')
    else:
        return answers[0][0]
    
    
