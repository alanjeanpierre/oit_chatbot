# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from oit_chatbot import text_processor

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
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
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
    #db = get_db()
    #cur = db.execute('select title, text from entries order by id desc')
    #entries = cur.fetchall()
    return render_template('show_chat.html')

@app.route('/process_message', methods=['POST'])
def rudeness():
    txt = request.form['text']
    response = process(txt)
    return response

# Login Verification of User
@app.route('/login', methods=['GET', 'POST'])
def login():
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
    #db = get_db()
    #cur = db.execute('select answer from knowledge order by random() limit 1')

    noun_phrases = text_processor.find_objects(txt)
    if not noun_phrases:
        response = "wtf??"
    elif len(noun_phrases) == 1:
        topic = noun_phrases[0]
        response = 'It looks like you\'re talking about ' + topic
    else:
        topic = noun_phrases[-1]
        qualifier = ' '.join(noun_phrases[:-1])
        response = 'It looks like you\'re talking about ' + topic + ', specifically the ' + qualifier

    return response + '. <br \>... idk what to tell you'

#display the admin page
@app.route('/admin')
def show_admin():
    return render_template('show_admin.html')

@app.route('/add', methods = 'GET', 'POST')
def add():
    print("You made it here")
    return render_template('add.html')

@app.route('/view')
def view():
    db = get_db()
    cursor = db.execute('select * from knowledge')
    questions = [dict(ID = row[0], TOPIC = row[1], QUAL = row[2], ANS = row[3], PL = row[4]) for row in cursor.fetchall()]
    dp.close()
    return render_template('view.html', quest = questions)