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
        cursor = db.execute('select answer from knowledge where topic = ? and qualifier is NULL', 
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

def add_question(db, question):
    """Adds question to database"""
    cur = db.cursor()
    cur.execute('''INSERT INTO knowledge (topic, qualifier, answer, lvl) 
                    VALUES (?, ?, ?, ?)''', 
                    question)
    cur.close()
    db.commit()

def get_all_questions(db):
    """Returns list of tuples of all questions in DB"""
    cursor = db.execute('select * from knowledge')
    questions = [dict(ID = row[0], TOPIC = row[1], QUAL = row[2], ANS = row[3], PL = row[4]) for row in cursor.fetchall()]
    cursor.close()
    return questions

def get_question_on_id(db, id):
    """Returns question number ID"""
    cursor = db.cursor()
    cursor.execute('SELECT * FROM knowledge WHERE id = ?', (id,))
    q = cursor.fetchone()
    cursor.close()
    return q

def delete_question_on_id(db, id):
    """Delete question with ID"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM knowledge WHERE id = ?", (id,))
    cursor.close()
    db.commit()

def update_question(db, question):
    """Update question based on id"""

    # Python renders null SQL as "None", and if its
    # passed back its as the string "None", not null
    # as it should be
    for i, q in enumerate(question):
        if q == 'None' or q == '':
            question[i] = None

    cursor = db.cursor()
    cursor.execute('''UPDATE knowledge SET 
                        topic = ?, 
                        qualifier = ?, 
                        answer = ?, 
                        lvl = ? 
                        WHERE id = ?
                        ''', question)
    cursor.close()
    db.commit()

def add_admin(db, admin):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (id, pwd, lvl) VALUES (?, ?, ?)", admin)
    cursor.close()
    db.commit()

def get_all_admins(db):
    cursor = db.execute('select * from users')
    users = [dict(UN = row[0], LVL = row[2]) for row in cursor.fetchall()]
    db.close()
    return users

def delete_admin(db, name):
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (name,))
    cursor.close()
    db.commit()