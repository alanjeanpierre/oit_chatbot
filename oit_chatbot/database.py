import sqlite3

def find_question(db, noun_phrases):
    """Locates relevant question in the database based on the noun phrases

    Args:
        db (sqlite3 database) - database connection to search in
        noun_phrases (list of str) - noun phrases
    
    Returns:
        str - First response in the sql database that matches the noun_phrases
    
    Raises:
        LookupError - On no noun phrases or no relevant row in the database

    """
    
    answers = []
    print(noun_phrases)
    if not noun_phrases:
        raise LookupError('No noun phrases found')
    elif len(noun_phrases) == 1:
        cursor = db.execute('select answer from knowledge where topic = ?', 
                            (noun_phrases))
        answers = cursor.fetchall()
    else:
        print(noun_phrases[-1])
        print(noun_phrases[-2])
        cursor = db.execute('select answer from knowledge where topic = ? and qualifier = ?', 
                            ( noun_phrases[-1], noun_phrases[-2]) )
        answers = cursor.fetchall()
        if not answers: # nothing with that qualifier, try just the topic
            cursor = db.execute('select answer from knowledge where topic = ?', 
                            (noun_phrases[-1],)) # comma is necessary to make it a tuple and not an enclosed statement
    
    if not answers:
        raise LookupError('No answers for that question')
    else:
        return answers[0][0]
    
    
