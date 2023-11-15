
from flask import Flask, render_template, request,redirect, url_for, flash

app = Flask(__name__)  

@app.route('/')
def index():
    return render_template('landing.html')

# Login
@app.route('/form_login',methods=['POST','GET'])
def login():

    if request.method =='POST':
        conn=sqlite3.connect('database/clients.db')
        c= conn.cursor()
        
        name=request.form["username"]
        password=request.form["password"]
        otp=request.form["otp"]
    

        validate="SELECT username,pass,otp FROM clients where username='"+name+"'and pass ='"+password+"'and otp ='"+otp+"'" 
        c.execute(validate)

        result=c.fetchall()


    #validate 
        if len(result)==0:
            return("You are not authorised to enter the site with credentials provided")
        else:
            return render_template('intel_gather.html')
