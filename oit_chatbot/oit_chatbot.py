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
    # if someone is already logged in, redirect them to the logout page
    if session.get('logged_in', None):
        return redirect(url_for('logout'))

    # create dict of users
    db = get_db()
    cursor = db.execute('select * from users')
    desc = cursor.description
    col_names = [col[0] for col in desc]
    rows = cursor.fetchall()
    data = [dict(zip(col_names, row)) for row in rows]

    data = {x['id'] : x['pwd'] for x in data}

    error = None
    if request.method == 'POST':
        if not request.form['username'] in data.keys():
            #print('bad username')
            error = 'Invalid username'
        elif request.form['password'] != data[request.form['username']]:
            #print('bad password')
            error = 'Invalid Password'
        else:
            #print('We made it here')
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_admin'))
    return render_template('login.html', error=error)

#Logout Verification of User
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('misses', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('show_chat'))

def process(txt):
    """Queries database for an answer and keeps a tally of missed answers.
    After 5 missed topics, it redirects to live support
    """
    
    noun_phrases = text_processor.find_objects(txt)

    try:
        response = database.find_question(get_db(), noun_phrases)
        return response
    except LookupError as e:
        database.add_miss(get_db(), noun_phrases)
        session['misses'] = session.get('misses', 0) + 1
        if session['misses'] == 5:
            return 'I need to transfer you to my superior. Please navigate to <a href="http://oitconnect.utsa.edu/">http://oitconnect.utsa.edu/</a>'
        if session['misses'] > 5:
            return 'Really, I can\'t help you anymore'
        
        return '... idk what to tell you'
    
    
    return response + '. <br \>... idk what to tell you'

# display the admin page
@app.route('/admin')
def show_admin():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    return render_template('show_admin.html')

# allow admin to add new FAQ
@app.route('/add', methods = ['GET', 'POST'])
def add():
    """Add question to the database"""
    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if request.method == 'POST':
        top = request.form['topic']
        qual = request.form['qual']
        answer = request.form['ans']
        pri = request.form['pl']
        db = get_db()
        database.add_question(db, [top, qual, answer, pri])
        database.remove_miss(db, [top, qual])
        return redirect(url_for('show_admin'))
    return render_template('add.html')

# display the FAQ's in the database
@app.route('/view', methods=['GET', 'POST'])
def view():
    """View the questions in the database"""
    """Delete questions from the database"""

    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if request.method == 'POST':
        id = request.form['id']
        database.delete_question_on_id(get_db(), id)
        return redirect(url_for('view'))
    else:
        questions = database.get_all_questions(get_db())
        return render_template('view.html', quest = questions)

# allow the admin to edit an entry
@app.route('/edit/', methods = ['GET', 'POST'])
def edit():
    """Edit a question in the knowledge database"""
    
    if not session.get('logged_in', None):
        return redirect(url_for('login'))


    if request.method == 'POST':
        i = request.form['id']
        top = request.form['topic']
        q = request.form['qual']
        ans = request.form['ans']
        lv = request.form['pl']
        database.update_question(get_db(), [top, q, ans, lv, i])
        return redirect(url_for('view'))
    else:
        id = request.args['id']
        row = database.get_question_on_id(get_db(), id)
        i, t, q, an, pl, count = row
        q = dict(ID = i, TOPIC = t, QUAL = q, ANS = an, PL = pl, COUNT = count)
        return render_template('edit.html', q=q)
                            

# display statistical information for the admin
@app.route('/stats')
def stats():
    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    
    questions = database.get_all_misses(get_db())
    return render_template('stats.html', quest = sorted(questions.items(), key=lambda q: q[1], reverse=True))

# allow admin to add admins
@app.route('/addAdmin', methods = ['GET', 'POST'])
def addAdmin():

    if not session.get('logged_in', None):
        return redirect(url_for('login'))

    if request.method == 'POST':
        un = request.form['username']
        pd = request.form['password']
        lv = request.form['level']
        database.add_admin(get_db(), (un, pd, lv))
        return redirect(url_for('show_admin'))
    return render_template('addAdmin.html')

# display all admins with delete button
@app.route('/viewAdmin', methods = ['GET', 'POST'])
def viewAdmin():

    if not session.get('logged_in', None):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        un = request.form['username']
        db = get_db()
        database.delete_admin(db, un)
        return redirect(url_for('viewAdmin'))
    else:
        db = get_db()
        users = database.get_all_admins(db)
        return render_template('viewAdmin.html', users = users)
