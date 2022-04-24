from flask import Flask,request, render_template, url_for, redirect, session
import os
import html2text
from login_database import Login_DataBase
from user_database import User_Database
from tv import show
tvobj = show()

cl = os.path.dirname(os.path.abspath(__file__))
login_db_path = os.path.join(cl, "login_database.db")
login_db_obj = Login_DataBase(login_db_path)
user_db_path = os.path.join(cl, "user_databse.db")
user_db_obj = User_Database(user_db_path)

logged_in = False

all_shows = None

uname = None

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
        global uname
        global logged_in
        uname = us
        session['user'] = us
        logged_in = True
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

    global logged_in
    if logged_in:
        return render_template('logged_home.html')
    else:
        return redirect('/login')


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
    show = tvobj.get_show_details(id)
    summary = show['summary']
    summary = html2text.html2text(summary)
    genres = show['genres']
    genres = ', '.join(genres)
    owner = ''
    if show['network']:
        owner = show['network']['name']
    if owner == '':
        owner = show['webChannel']['name']

    cast,cast_list = tvobj.get_cast(id)
    cast_list = ', '.join(cast_list)
    try:
        streamat  = str(show['schedule']['time'])
    except:
        streamat = ''
    try:
        tzone = str(show['network']['country']['timezone'])
    except:
        tzone = ''
    try:
        days = show['schedule']['days']
        days = ','.join(days)
    except:
        days = ''
    return render_template('show_details.html',id=id,tzone=tzone,stramat=streamat,days=days,cast_list=cast_list,owner=owner,genres=genres,show=show,summary=summary)



@app.route('/rmas',methods=['POST','GET'])
def rmas():
    global uname
    shows_today = tvobj.get_shows_today()
    rec = False
    for show in shows_today:
        id = show['id']
        recomm_list = list(user_db_obj.get_rec_shows(uname))
        if str(show['id']) not in recomm_list:
            user_db_obj.add_show(uname,str(id))
            rec = True
            break
        else:
            continue
    if rec:
        summary = show['summary']
        summary = html2text.html2text(summary)
        genres = show['genres']
        genres = ', '.join(genres)
        if show['image'] is not None and show['image']['medium'] is not None:
            image = show['image']['medium']
        else:
            image = 'http://www.movienewz.com/img/films/poster-holder.jpg'
        owner = ''
        if show['network']:
            owner = show['network']['name']
        if owner == '':
            owner = show['webChannel']['name']

        cast,cast_list = tvobj.get_cast(id)
        cast_list = ', '.join(cast_list)
        try:
            streamat  = str(show['schedule']['time'])
        except:
            streamat = ''
        try:
            tzone = str(show['network']['country']['timezone'])
        except:
            tzone = ''
        try:
            days = show['schedule']['days']
            days = ','.join(days)
        except:
            days = ''
        return render_template('r_show_details.html',id=id,tzone=tzone,stramat=streamat,days=days,image=image,cast_list=cast_list,owner=owner,genres=genres,show=show,summary=summary)
    else:
        return render_template('no_show.html')


@app.route('/rbui',methods=['POST','GET'])
def rbui():
    shows_today = tvobj.get_shows_today()
    langs = []
    genres = []
    for x in shows_today:
        if x['language'] and x['language'] not in langs:
            langs.append(x['language'])
        if x['genres']:
            gl = x['genres']
            for g in gl:
                if g not in genres:
                    genres.append(g)
    
    if request.method=="POST":
        lang = request.form['language']
        genre = request.form['genre']
        rec_list = []
        global uname
        for show in shows_today:
            if lang in show['language'] and genre in show['genres']:
                rec_list.append(show['id'])
        if len(rec_list)>0:
            for sid in rec_list:
                recomm_list = list(user_db_obj.get_rec_shows(uname))
                if str(sid) not in recomm_list:
                    user_db_obj.add_show(uname,str(sid))
                    return redirect(url_for('show_info',id=sid))
                else:
                    continue
            return render_template('no_show.html')
        else:
            return render_template('no_show.html')



    return render_template('rec_user_input.html',genres=genres,langs=langs,ll=len(langs),gl=len(genres))


@app.route('/reset')
def reset_recom():
    global uname
    user_db_obj.reset_recommendations(uname)
    return redirect('home')

@app.route('/show_infos/<id>',methods = ['POST','GET'])
def show_info(id):
    show = tvobj.get_show_details(id)
    summary = show['summary']
    summary = html2text.html2text(summary)
    genres = show['genres']
    genres = ', '.join(genres)
    if show['image'] is not None and show['image']['medium'] is not None:
        image = show['image']['medium']
    else:
        image = 'http://www.movienewz.com/img/films/poster-holder.jpg'
    owner = ''
    if show['network']:
        owner = show['network']['name']
    if owner == '':
        owner = show['webChannel']['name']

    cast,cast_list = tvobj.get_cast(id)
    cast_list = ', '.join(cast_list)
    try:
        streamat  = str(show['schedule']['time'])
    except:
        streamat = ''
    try:
        tzone = str(show['network']['country']['timezone'])
    except:
        tzone = ''
    try:
        days = show['schedule']['days']
        days = ','.join(days)
    except:
        days = ''
    return render_template('r_show_details.html',id=id,tzone=tzone,stramat=streamat,days=days,image=image,cast_list=cast_list,owner=owner,genres=genres,show=show,summary=summary)


if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')