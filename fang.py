
from flask import Flask, render_template, request,redirect, url_for, flash

# WTF manage form entry validations


#from email.mime.application import MIMEApplication

#Security features 
import nmap
import pyfile.otp
import pyfile.password_check


app = Flask(__name__)  


#Security headers
@app.after_request
def security_headers(resp):
    # preventing man-in-the-middle (MITM) attack
    resp.headers['Strict-Transport-Security'] = 'max-age=31536000'

    resp.headers['Content-Security-Policy'] = 'default-src "self" https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'
    # prevent cross-site scripting (XSS) attack.
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    # prevents external sites from embedding your site in an iframe (clickjacking)
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return resp


#connection to database
import sqlite3
import database.database

db_path='database\clients.db'



@app.route('/')
def index():
    return render_template('landing.html')

# if user exist direct to info_gather else deny access
@app.route('/form_login',methods=['POST','GET'])
def login():
        conn=sqlite3.connect('clients.db')
        c=conn.cursor()
        name=request.form["username"]
        password=request.form["password"]
        otp=request.form["otp"]
    
        step1="SELECT username,pass,otp FROM clients where username='"+name+"'and key ='"+password+"'and otp ='"+otp+"'"
        c.execute(step1)
        result=c.fetchall()


    #validate 
        if len(result)==0:
            return("You are not authorised to enter the site with credentials provided")
        else:
            conn.close()
            return render_template('landing.html')
            


@app.route('/first',methods=['POST','GET'])
def verify():
    key=pyfile.otp.key()
    pyfile.otp.generate_qr(key)

    return render_template('otp.html')
