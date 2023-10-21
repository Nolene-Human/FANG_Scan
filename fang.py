from flask import Flask, render_template, request,redirect, url_for
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
    password=request.form["uniqekey"]
    
    if name1 in database and password=='123':
        return redirect(url_for("intel"))
    else:
        return "Access Denied"
    



@app.route('/Intel_gather')
def intel():

    return render_template('intel_gather.html')
    
if __name__=="__main__":
    app.run(host='0.0.0.0')