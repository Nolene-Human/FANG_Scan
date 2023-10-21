from flask import Flask, render_template, request,redirect
import sqlite3


app = Flask(__name__)

database={'nina@gmail.com':'123'}    

@app.route('/')
def index():
    return render_template('login.html')

# if user exist direct to info_gather else deny access
@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form["username"]
    
    if name1 in database:
        return render_template('info_gather.html')
    else:
        return "Access Denied"


@app.route('/Intelligence-Gathering')
def intel():

    return render_template('info_gather.html')
    
if __name__=="__main__":
    app.run(host='0.0.0.0')