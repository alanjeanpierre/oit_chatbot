import sqlite3
from datetime import datetime

def add_miss(db, noun_phrases):
    if not noun_phrases:
        return
    elif len(noun_phrases) == 1:
        noun_phrases = (None, noun_phrases[0])

    db.execute('''INSERT INTO unknown values(?, ?, ?)''', (datetime.now(), noun_phrases[-1], noun_phrases[-2]))
    db.commit()

def remove_miss(db, q):
    if q[0] == 'None' or q[0] == '':
        return

    if q[1] == 'None' or q[1] == '':
        db.execute('''DELETE FROM unknown WHERE topic=? AND qualifier IS NULL''', (q[0],))
    else:
        db.execute('''DELETE FROM unknown WHERE topic=? AND qualifier=?''', q)
    db.commit()

def get_all_misses(db):
    cursor = db.execute('select topic, qualifier from unknown')
    d = dict()
    for row in cursor.fetchall():
        d[row] = d.get(row, 0) + 1
    cursor.close()
    return d

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
    if not noun_phrases:
        raise LookupError('No noun phrases found')
    elif len(noun_phrases) == 1:
        cursor = db.execute('select id, answer, count from knowledge where topic = ? and qualifier is NULL', 
                            (noun_phrases))
        answers = cursor.fetchone()
    else:
        #print(noun_phrases[-1])
        #print(noun_phrases[-2])
        cursor = db.execute('select id, answer, count from knowledge where topic = ? and qualifier = ?', 
                            ( noun_phrases[-1], noun_phrases[-2]) )
        answers = cursor.fetchone()
        if not answers: # nothing with that qualifier, try just the topic
            cursor = db.execute('select id, answer, count from knowledge where topic = ?', 
                            (noun_phrases[-1],)) # comma is necessary to make it a tuple and not an enclosed statement
            answers = cursor.fetchone()
    
    if not answers:
        raise LookupError('No answers for that question')
    else:
        #print(answers[0], answers[1], answers[2])
        db.execute('UPDATE knowledge SET count=? WHERE id=?', (answers[2]+1, answers[0]))
        db.commit()
        return answers[1]

def add_question(db, question):
    """Adds question to database"""
    for i, q in enumerate(question):
        if q == 'None' or q == '':
            question[i] = None
            
    cur = db.cursor()
    cur.execute('''INSERT INTO knowledge (topic, qualifier, answer, lvl, count) 
                    VALUES (?, ?, ?, ?, 0)''', 
                    question)
    cur.close()
    db.commit()

def get_all_questions(db):
    """Returns list of tuples of all questions in DB"""
    cursor = db.execute('select * from knowledge')
    questions = [dict(
                    ID = row[0], 
                    TOPIC = row[1], 
                    QUAL = row[2], 
                    ANS = row[3], 
                    PL = row[4], 
                    CT = row[5]) for row in cursor.fetchall()]
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
                        lvl = ?,
                        count = 0
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
