

from flask import Flask,request, render_template, url_for, redirect, session
import os
import html2text
from login_database import Login_DataBase
from tv import show
tvobj = show()

cl = os.path.dirname(os.path.abspath(__file__))
login_db_path = os.path.join(cl, "login_database.db")
login_db_obj = Login_DataBase(login_db_path)

all_shows = None

app = Flask(__name__)
app.secret_key = 'danielle'

@app.route('/')
def index():
    return render_template('index.html')


#   login page
@app.route('/login')
def login():
    return render_template('login.html')


# verify login
@app.route('/login', methods=['POST'])
def veify_login():
    us = request.form['username']
    ps = request.form['password']
    
    flag = login_db_obj.verify_login(us,ps)
    if flag:
        session['user'] = us
        return redirect(url_for('home'))
    else:
        return redirect('/signup')


# sign up
@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method=="POST":
        us = request.form['username']
        ps = request.form['password']
        ans = login_db_obj.register(us,ps)
        if ans:
            return redirect('/login')
        else:
            return redirect('/signup')
    return render_template('signup.html')


# home page of user
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method=="POST":
        searchq1 = request.form['searchq']
        return redirect(url_for('search',term=searchq1))

    return render_template('logged_home.html')


#search list shows here
@app.route('/search/<term>',methods = ['POST','GET'])
def search(term):
    images = []
    names = []
    ids = []
    shows = tvobj.search(term)
    if len(shows)==0:

        return render_template('no_match.html')
    else:
        length = len(shows)
        global all_shows
        all_shows = shows
        for show in shows:
            if show['image'] is not None and show['image']['medium'] is not None:
                images.append(show['image']['medium'])
            else:
                images.append('http://www.movienewz.com/img/films/poster-holder.jpg')
            names.append(show['name'])
            ids.append(show['id'])
        return render_template('show_matches.html',images = images,names = names,term=term,length=length,ids=ids)
    
    
@app.route('/show_details/<id>',methods=['POST','GET'])
def search_details(id):
    global all_shows
    shows = all_shows
    for show in shows:
        if show['id'] == int(id):
            break
    summary = show['summary']
    summary = html2text.html2text(summary)

    return render_template('show_details.html',id=id,show=show,summary=summary)




if __name__=='__main__':
    app.run(debug=True)