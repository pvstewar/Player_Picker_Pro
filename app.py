from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', content= "testing")

@app.route('/team_ratings')
def team_ratings():
    return render_template('team.html', content= "Team Ratings")

@app.route('/pick_player')
def pick_player():
    return render_template('pick_player.html', content= "Pick a Player by Wage")

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

@app.route('/teamrec',methods = ['POST', 'GET'])
def teamrec():
    if request.method == 'POST':
        tn = request.form['tn']
         
        con = sql.connect("fb.db")
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
         
        con = sql.connect("fb.db")
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
         
        con = sql.connect("fb.db")
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
        
        con = sql.connect("fb.db")
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
         
        con = sql.connect("fb.db")
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
        
        con = sql.connect("fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * from plyr_atr WHERE ValueEUR <= {value} ORDER BY {col} DESC LIMIT 25'.format(value=val, col=pos))
        rows = cur.fetchall();
        return render_template("pick_valresult.html",rows = rows)
    con.close()

#app.debug = True
if __name__ == "__main__":
    app.run(debug=True)