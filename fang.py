
from flask import Flask, render_template, request, session,flash

#Security features 
import pyfile.otp
import pyfile.password_check
import pyfile.randomkey

from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)  

key=pyfile.randomkey.generate_password()
app.secret_key=key
csrf=CSRFProtect(app)

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
db_path='database\clients.db'



@app.route('/')
def index():
    session['attempt'] = 3
    return render_template('landing.html')

# if user exist direct to info_gather else deny access
@app.route('/form_login',methods=['POST','GET'])
def login():
        
    #while attempt <3:
        conn=sqlite3.connect('clients.db')
        c=conn.cursor()
        name=request.form["username"]
        session['username'] = name
        password=request.form["password"]
        otp=request.form["otp"]

        # Reduce risk for SQL injection by sanatise user input for commented sql injection
        newname = ""
        for n in name:
            if n == "'" or n =="--" or n =="=":
                n = ""
            else:
                newname=newname+n

        sql = "SELECT username, pass, otp_pin FROM clients WHERE username = ? AND key = ? AND otp_pin = ?"
        c.execute(sql,(newname,password,otp))
        result=c.fetchall()
        attempt= session.get('attempt')
        attempt -= 1
        session['attempt']=attempt

        if attempt == 0:
            return render_template('block.html')
    #validate 
        if len(result)==0:
            error=("You did not provide the correct credentials.")
            return render_template('landing.html',error=error)
 
        else:
            conn.close()
            return ("You are logged in")
        


@app.route('/validate',methods=['POST','GET'])
def verify():
    key=pyfile.otp.key()
    pyfile.otp.generate_qr(key)

    return render_template('otp.html')

if __name__ == "__main__":
  app.run()