import sqlite3

def find_question(db, noun_phrases):
    
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
        raise LookupError('No answers for that question')
    else:
        return answers[0][0]
    
    
