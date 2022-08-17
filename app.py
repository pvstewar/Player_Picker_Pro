from flask import Flask, render_template, request, redirect
import sqlite3 as sql
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = 'r3JEzW1*mK%nuiMl7tSX'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'

@app.before_first_request
def create_all():
    db.create_all()

@app.route('/welcome')
@login_required
def blog():
    return render_template('welcome.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/welcome')

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/welcome')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/welcome')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/welcome')

@app.route('/')
def hello():
    return render_template('index.html', content= "testing")

@app.route('/team_ratings')
def team_ratings():
    return render_template('team.html', content= "Team Ratings")

@app.route('/pick_player')
def pick_player():
    return render_template('pick_player.html', content= "Pick a Player by Wage")

@app.route('/about')
def about():
    return render_template('about.html', content= "about this site")

@app.route('/player_stats')
def player_stats():
    return render_template('player_stats.html', content= "Player Stats")

@app.route('/fifa_player')
def fifa_player():
    return render_template('fifa_player.html', content= "FIFA Player Ratings")

@app.route('/league_stat')
def league_stat():
    return render_template('league_stat.html', content= "Team Statistics")

@app.route('/pick_player_val')
def pick_player_val():
    return render_template('pick_player_val.html', content= "Pick a Player by Value")

@app.route('/myteam')
def my_team():
    return render_template('myteam.html', content= "Your Team")

@app.route('/teamrec',methods = ['POST', 'GET'])
def teamrec():
    if request.method == 'POST':
        tn = request.form['tn']

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * from teams WHERE Name LIKE ?",('%'+tn+'%',))
        rows = cur.fetchall();
        return render_template("team_result.html",rows = rows)
    con.close()

@app.route('/plyrrec',methods = ['POST', 'GET'])
def plyrrec():
    if request.method == 'POST':
        pn = request.form['pn']

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * from plyr_stat WHERE player_name LIKE ?",('%'+pn+'%',))
        rows = cur.fetchall();
        return render_template("plyr_result.html",rows = rows)
    con.close()

@app.route('/fifa_plyrrec',methods = ['POST', 'GET'])
def fifa_plyrrec():
    if request.method == 'POST':
        fpi = request.form['fpi']

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * from plyr_atr WHERE FullName LIKE ?",('%'+fpi+'%',))
        rows = cur.fetchall();
        return render_template("fifa_plyr_result.html",rows = rows)
    con.close()



@app.route('/pickrec',methods = ['POST', 'GET'])
def pickrec():
    if request.method == 'POST':
        wg = request.form.get('wg')
        pos = request.form.get('pos')

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * from plyr_atr WHERE WageEUR <= {wage} ORDER BY {col} DESC LIMIT 25'.format(wage=wg, col=pos))
        rows = cur.fetchall();
        return render_template("pickresult.html",rows = rows)
    con.close()

@app.route('/leaguerec',methods = ['POST', 'GET'])
def leaguerec():
    if request.method == 'POST':
        lg = request.form['lg']

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * from league WHERE squad LIKE ?",('%'+lg+'%',))
        rows = cur.fetchall();
        return render_template("league_result.html",rows = rows)
    con.close()

@app.route('/pickrec_val',methods = ['POST', 'GET'])
def pickrec_val():
    if request.method == 'POST':
        val = request.form.get('val')
        pos = request.form.get('pos')

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * from plyr_atr WHERE ValueEUR <= {value} ORDER BY {col} DESC LIMIT 25'.format(value=val, col=pos))
        rows = cur.fetchall();
        return render_template("pick_valresult.html",rows = rows)
    con.close()

@app.route('/playerdet',methods = ['POST', 'GET'])
def playerdet():
    if request.method == 'POST':
        pi = request.form['pi']

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * from plyr_atr WHERE ID = ?",(pi,))
        rows = cur.fetchall();
        return render_template("player_details.html",rows = rows)
    con.close()

@app.route('/playeradd',methods = ['POST', 'GET'])
@login_required
def playeradd():
    if request.method == 'POST':
        add = request.form.get('add')
        slot = request.form.get('slot')
        usr = current_user.username
        con = sql.connect("/home/peeves/mysite/ud.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("UPDATE users SET {slot}= {add} WHERE username='{user}'".format(slot=slot,add = add,user=usr));
        con.commit()
        con = sql.connect("/home/peeves/mysite/ud.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username='{user}'".format(user=usr));
        players = cur.fetchall();

        con = sql.connect("/home/peeves/mysite/fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM plyr_atr WHERE ID ={add}".format(add = add));
        rows = cur.fetchall();
        return render_template("player_added.html",rows = rows, players=players)
    con.close()

@app.route('/team_view',methods = ['POST', 'GET'])
@login_required
def team_view():
    usr = current_user.username
    idlst = []
    con = sql.connect("/home/peeves/mysite/ud.db")
    con.row_factory = None
    cur = con.cursor()
    cur.execute("SELECT player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11 FROM users  WHERE username='{user}'".format(user=usr));
    for i in cur.fetchall():
        idlst.append(str(i))
    con.commit();

    #need to clean up my list of strings
    idlst = idlst[0].split(", ")
    char = '('
    char2 = ')'
    char3 = ','
    char4 = ' '
    for idx, ele in enumerate(idlst):
        idlst[idx] = ele.replace(char, '')
    for idx, ele in enumerate(idlst):
        idlst[idx] = ele.replace(char2, '')
    for idx, ele in enumerate(idlst):
        idlst[idx] = ele.replace(char3, '')
    for idx, ele in enumerate(idlst):
        idlst[idx] = ele.replace(char4, '')

    con = sql.connect("/home/peeves/mysite/fb.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM plyr_atr WHERE ID in ({},{},{},{},{},{},{},{},{},{},{})".format(idlst[0],idlst[1],idlst[2],idlst[3],idlst[4],idlst[5],idlst[6],idlst[7],idlst[8],idlst[9],idlst[10]))
    rows = cur.fetchall();
    cur.execute("SELECT avg(Overall),sum(WageEUR) FROM plyr_atr WHERE ID in ({},{},{},{},{},{},{},{},{},{},{})".format(idlst[0],idlst[1],idlst[2],idlst[3],idlst[4],idlst[5],idlst[6],idlst[7],idlst[8],idlst[9],idlst[10]))
    sta = cur.fetchall();
    con.close()

    return render_template("myteam.html",rows = rows, sta = sta)

app.debug = False
toolbar = DebugToolbarExtension(app)
#app.debug = True
if __name__ == "__main__":
    app.run(debug=True)