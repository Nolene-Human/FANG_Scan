from flask import Flask, render_template, request,redirect
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')


database={'nina@gmail.com':'123'}
    
@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form["username"]
    
    if name1 in database:
        return render_template('pre_engagement.html')
    else:
        return "Access Denied"

@app.route('/pre-engagement',methods=['POST','GET'])
def pre_eng():
    sign=request.form["name"]

    if sign == "nina":
        return render_template('info_gather.html')
    else:
        return render_template('pre_engagement.html')


@app.route('/Intelligence-Gathering')
def intel():

    return render_template('info_gather.html')
    
if __name__=="__main__":
    app.run(host='0.0.0.0', port=80)