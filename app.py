from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', content= "testing")

@app.route('/team_stats')
def team_stats():
    return render_template('team.html', content= "Team Stats")

@app.route('/pick_player')
def pick_player():
    return render_template('pick_player.html', content= "Pick a Player")

@app.route('/player_stats')
def player_stats():
    return render_template('player_stats.html', content= "Player Stats")

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

@app.route('/pickrec',methods = ['POST', 'GET'])
def pickrec():
    if request.method == 'POST':
        wg = request.form.get('wg')
        pos = request.form.get('pos')
        
        con = sql.connect("fb.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * from plyr_atr WHERE WageEUR <= {wage} ORDER BY {col} DESC LIMIT 25'.format(wage=wg, col=pos))
        #cur.execute("SELECT * from plyr_atr WHERE WageEUR <= 27000 ORDER BY ? DESC LIMIT 25",(pos,))
        rows = cur.fetchall();
        return render_template("pickresult.html",rows = rows)
    con.close()


#app.debug = True
if __name__ == "__main__":
    app.run(debug=True)