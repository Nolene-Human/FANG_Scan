
from flask import Flask, render_template, request,redirect, url_for, flash

# WTF manage form entry validations
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp



#Database
import sqlite3


#from email.mime.application import MIMEApplication

#Security features 
import nmap
import pyfile.otp
import pyfile.password_check


app = Flask(__name__)  

#key make it a environment variable
app.config['SECRET_KEY'] = '18b88266e62d2c2b21666239e31215d5'

@app.route('/')
def index():
    return render_template('register.html')

# if user exist direct to info_gather else deny access
@app.route('/registration',methods=['POST','GET'])
def login():

    if request.method =='POST':
        conn=sqlite3.connect('database/clients.db')
        c= conn.cursor()
        
        name1=request.form["username"]
        key=request.form["uniqekey"]
    

        validate="SELECT email,key FROM clients where username='"+name1+"'and key ='"+key+"'" 
        c.execute(validate)

        result=c.fetchall()
        

    #validate 
        if len(result)==0:
            return("You are not authorised to enter the site with credentials provided")
        else:
            return render_template('verify.html')
        
@app.route('/validate',methods=['POST','GET'])
def validation():
    
    if request.method =='POST':
        password=request.form["password"]
        conf_password=request.form["conf_password"]
        
        SpecialSym =['$', '@', '#', '%','!']
        
        if len(password) < 6:
            msg='Length should be at least 6 characters'
            return render_template('verify.html',msg=msg)
    
        if not any(char.isdigit() for char in password):
            msg=('Password should have at least one numeral value')
            return render_template('verify.html',msg=msg)            
        
        if not any(char.isupper() for char in password):
            msg=('Password should have at least one uppercase letter')
            return render_template('verify.html',msg=msg)
            
        if not any(char.islower() for char in password):
            msg=('Password should have at least one lowercase letter')
            return render_template('verify.html',msg=msg)
        
        if not any(char in SpecialSym for char in password):
            msg=("Password should have at least one of the symbols '$', '@', '#', '%', '!' ")
            return render_template('verify.html',msg=msg)
        
        if password!=conf_password:
            msg= ("Passwords do not match")
            return render_template('verify.html',msg=msg)
                
        else:
            msg=("Password updated")
            return render_template('verify.html',msg=msg)

@app.route('/otp')
def otp():
    
    key=pyfile.otp.key()
    otp=pyfile.otp.generate_qr(key)
    print (otp)
    
    return render_template('verify.html')
    



    # class passwordform(FlaskForm):


    #     password=PasswordField('Password',
    #                         validators=[DataRequired(),
    #                             Length(min=8, message='Password has to be at least 8 characters'),
    #                             Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!$%^&*])[A-Za-z\d!$%^&*]{8,}$",
    #                             message="Your password did not meet the minimum requirements of a lower/upper and number")])
        
    #     password_confirm=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #     pass_submit=SubmitField('Save Password')


#Validates the password
# @app.route('/password')
# def password():  
#     form=passwordform()
#     return render_template('verify.html', title='Password', form=form)
    
#     #validate form
#     # if form.validate_on_submit():
#     #     password1=form.password.data
#     #     form.password.data=""
#     #     #msg=pyfile.password_check.password_check(password1)
        
    
    



@app.route('/Intel_gather')
def intel(): 

    return render_template('intel_gather.html')



#Called when 'Scan' button is pressed on intel_gather.html
@app.route('/scan',methods=['POST','GET'])
def scan():    
    #todos.clear()
    
    conn_devices=sqlite3.connect('database/clients.db')

    #create cursor
    c_d= conn_devices.cursor()


    #create a database
    c_d.execute("""
    CREATE TABLE IF NOT EXISTS devices (
            ip text,
            macaddress text,
            manufacturer text)
    """)

    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')
                        
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]["addresses"]["mac"]
            manufacturer = nm[host]["vendor"].get(mac_address, "Unknown")
            #device={"IP":host,"MAC":mac_address,"MAN":manufacturer}
            #device=(host,mac_address,manufacturer,)
            #todos.append(device)
            #insert to database
            
            c_d.execute("INSERT INTO devices (ip, macaddress,manufacturer) VALUES(?,?,?)",(host, mac_address, manufacturer))
            conn_devices.commit()
    
    conn_devices.close()
 #-------------------------------------------------------------------------------#
    return redirect(url_for('list'))

@app.route("/list")
def list():

    con = sqlite3.connect("devices.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM devices") 

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("list.html", rows=rows)


@app.route('/delete',methods=['POST','GET'])
def delete():
       if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('devices.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM devices WHERE rowid="+rowid)
                    con.commit()
        except:
            con.rollback()

        finally:
            con.close()
        
        return redirect(url_for('list'))

#if __name__=="__main__":
 #   app.run(host='0.0.0.0')