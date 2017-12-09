# all the imports
import os, sys
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from oit_chatbot import text_processor
from oit_chatbot import database

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'chatbot.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initialize database with various sql statements.
    Specifically loads the tables, knowledgebase and admin users
    """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    with app.open_resource('knowledge.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    with app.open_resource('users.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database"""
    init_db()
    print('Initialized the database')

def get_db():
    """Opens a new database connection if there is none yet for there
    current application content.
    """
    
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_chat():
    """Shows the main chat page"""
    #db = get_db()
    #cur = db.execute('select title, text from entries order by id desc')
    #entries = cur.fetchall()
    return render_template('show_chat.html')

@app.route('/process_message', methods=['POST'])
def rudeness():
    """Accepts input from the chatpage and returns a response"""
    txt = request.form['text']
    response = process(txt)
    return response

# Login Verification of User
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and login logic for the admin portal"""
    # create dict of users
    db = get_db()
    cursor = db.execute('select * from users')
    desc = cursor.description
    col_names = [col[0] for col in desc]
    rows = cursor.fetchall()
    data = [dict(zip(col_names, row)) for row in rows]

    data = {x['id'] : x['pwd'] for x in data}

    print('before post')
    print(data)
    error = None
    if request.method == 'POST':
        print('after post')
        if not request.form['username'] in data.keys():
            print('bad username')
            error = 'Invalid username'
        elif request.form['password'] != data[request.form['username']]:
            print('bad password')
            error = 'Invalid Password'
        else:
            print('We made it here')
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_admin'))
    return render_template('login.html', error=error)

#Logout Verification of User
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_chat'))

def process(txt):
    """Queries database for an answer and keeps a tally of missed answers.
    After 5 missed topics, it redirects to live support
    """
    #db = get_db()
    #cur = db.execute('select answer from knowledge order by random() limit 1')

    noun_phrases = text_processor.find_objects(txt)
    #if not noun_phrases:
    #    response = "wtf??"
    #elif len(noun_phrases) == 1:
    #    topic = noun_phrases[0]
    #    response = 'It looks like you\'re talking about ' + topic
    #else:
    #    topic = noun_phrases[-1]
    #    qualifier = ' '.join(noun_phrases[:-1])
    #    response = 'It looks like you\'re talking about ' + topic + ', specifically the ' + qualifier

    try:
        response = database.find_question(get_db(), noun_phrases)
        return response
    except LookupError as e:
        session['misses'] = session.get('misses', 0) + 1
        if session['misses'] == 5:
            return 'I need to transfer you to my superior, Mr. Lake'
        if session['misses'] > 5:
            return 'Really, I can\'t help you anymore'
        
        return '... idk what to tell you'
    
    
    return response + '. <br \>... idk what to tell you'

# display the admin page
@app.route('/admin')
def show_admin():
    return render_template('show_admin.html')

# allow admin to add new FAQ
@app.route('/add', methods = ['GET', 'POST'])
def add():
    """Add question to the database"""
    if request.method == 'POST':
        top = request.form['topic']
        qual = request.form['qual']
        answer = request.form['ans']
        pri = request.form['pl']
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO knowledge (topic, qualifier, answer, lvl) VALUES (?, ?, ?, ?)", (top, qual, answer, pri))
        cur.close()
        db.commit()
        return redirect(url_for('show_admin'))
    return render_template('add.html')

# display the FAQ's in the database
@app.route('/view')
def view():
    """View the questions in the database"""
     """Delete questions from the database"""
    if request.method == 'POST':
        id = request.form['id']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM knowledge WHERE id = ?", (id,))
        cursor.close()
        db.commit()
        return redirect(url_for('view'))
    else:
        db = get_db()
        cursor = db.execute('select * from knowledge')
        questions = [dict(ID = row[0], TOPIC = row[1], QUAL = row[2], ANS = row[3], PL = row[4]) for row in cursor.fetchall()]
        db.close()
        return render_template('view.html', quest = questions)

# allow the admin to remove an entry
#@app.route('/delete', methods = ['GET', 'POST'])
#def delete():
#    """Delete questions from the database"""
#    if request.method == 'POST':
#        id = request.form['value']
#        db = get_db()
#        cursor = db.cursor()
#       cursor.execute("DELETE FROM knowledge WHERE id = ?", (id,))
#        cursor.close()
#       db.commit()
#      return redirect(url_for('view'))
#   db = get_db()
#   cursor = db.execute('select * from knowledge')
#   questions = [dict(ID = row[0], TOPIC = row[1], QUAL = row[2], ANS = row[3], PL = row[4]) for row in cursor.fetchall()]
#   db.close()
#   return render_template('delete.html', quest = questions)

# allow the admin to edit an entry
@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    """Edit a question in the knowledge database"""
    if request.method == 'POST':
        return redirect(url_for('view'))
    return render_template('edit.html')

# display statistical information for the admin
@app.route('/stats')
def stats():
    return render_template('stats.html')

# allow admin to add admins
@app.route('/addAdmin', methods = ['GET', 'POST'])
def addAdmin():
    if request.method == 'POST':
        un = request.form['username']
        pd = request.form['password']
        lv = request.form['level']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (id, pwd, lvl) VALUES (?, ?, ?)", (un, pd, lv))
        cursor.close()
        db.commit()
        return redirect(url_for('show_admin'))
    return render_template('addAdmin.html')

# allow admin to delete admins
@app.route('/delAdmin', methods = ['GET', 'POST'])
def delAdmin():
    if request.method == 'POST':
        un = request.form['username']
        pd = request.form['password']
        db = get_db()
        cursor = db.cursor()
        if un != None:
            cursor.execute("DELETE FROM users WHERE id = ?", (un,))
            cursor.close()
            db.commit()
        elif pd != None:
            cursor.execute("DELETE FROM users WHERE pwd = ?", (pd,))
            cursor.close()
            db.commit()
        return redirect(url_for('viewAdmin'))
    return render_template('delAdmin.html')

# display all admins
@app.route('/viewAdmin', methods=['GET', 'POST'])
def viewAdmin():
    db = get_db()
    cursor = db.execute('select * from users')
    users = [dict(UN = row[0], LVL = row[2]) for row in cursor.fetchall()]
    db.close()
    return render_template('viewAdmin.html', users = users)
