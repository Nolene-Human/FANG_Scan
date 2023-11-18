
from flask import Flask, render_template, request,redirect, url_for, flash

# WTF manage form entry validations


#from email.mime.application import MIMEApplication

#Security features 
import nmap
import pyfile.otp
import pyfile.password_check


app = Flask(__name__)  


#Security headers
# @app.after_request
# def security_headers(resp):
#     # preventing man-in-the-middle (MITM) attack
#     resp.headers['Strict-Transport-Security'] = 'max-age=31536000'

#     resp.headers['Content-Security-Policy'] = 'default-src "self"'
#     # prevent cross-site scripting (XSS) attack.
#     resp.headers['X-Content-Type-Options'] = 'nosniff'
#     # prevents external sites from embedding your site in an iframe (clickjacking)
#     resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    #return resp


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
    
        step1="SELECT username,pass,otp FROM clients where username='"+name+"'and pass ='"+password+"'and otp ='"+otp+"'"
        c.execute(step1)
        result=c.fetchall()


    #validate 
        if len(result)==0:
            return("You are not authorised to enter the site with credentials provided")
        else:
            conn.close()
            return render_template('intel_gather.html')
            


@app.route('/first',methods=['POST','GET'])
def verify():
    return render_template('verify.html')

@app.route('/validate',methods=['POST','GET'])
def validation():

    if request.method =='POST':
        conn=sqlite3.connect('clients.db')
        c=conn.cursor()

        name1=request.form["username"]
        key=request.form["uniqekey"]
    
        verify="SELECT email,key FROM clients where username='"+name1+"'and key ='"+key+"'" 
        c.execute(verify)
        verifya=c.fetchall()

        if len(verifya)==0:
             return("You are not authorised to enter the site with credentials provided")
    
        else:
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
                key=pyfile.otp.key()
                pyfile.otp.generate_qr(key)
                msg=("Password updated")
                #update database
                pss="UPDATE clients SET pass='"+password+"'where username='"+name1+"'"
                otp="UPDATE clients SET otp='"+key+"'where username='"+name1+"'"
                c.execute(pss)
                c.execute(otp)
                conn.commit()
                conn.close()

                return render_template('otp.html')
  

@app.route('/otp',methods=['POST','GET'])
def otp():

    if request.method =='POST':
        conn=sqlite3.connect('clients.db')
        c=conn.cursor()
        
        c.execute("SELECT otp FROM clients WHERE username='Dragonfly'")
        call_otp=c.fetchall()
        print(call_otp)
        key=pyfile.otp.generatepin(call_otp)
        print(key)


    # pyfile.otp.generate_code(key)
    # unq_code=pyfile.otp.generatepin(key)
    # print(unq_code)
 
    # savecode='static/codes/'+qr
       

    # if request.method =='POST':
    #     conn=sqlite3.connect('clients.db')
    #     c=conn.cursor()
        
    #     code=request.form["otp_code"]

    #     if code=="":
    #         return render_template('otp.html',savecode=savecode)
    #     if code!=unq_code:
    #         msg="No Access"
    #         return render_template('otp.html',msg=msg,savecode=savecode)
    #     else:
    #         return ("Key confirmed")
    return render_template('otp.html')
    

# @app.route('/Intel_gather')
# def intel(): 

#     return render_template('intel_gather.html')



# #Called when 'Scan' button is pressed on intel_gather.html
# @app.route('/scan',methods=['POST','GET'])
# def scan():    
#     #todos.clear()
    
#     conn_devices=sqlite3.connect('database/clients.db')

#     #create cursor
#     c_d= conn_devices.cursor()


#     #create a database
#     c_d.execute("""
#     CREATE TABLE IF NOT EXISTS devices (
#             ip text,
#             macaddress text,
#             manufacturer text)
#     """)

#     nm = nmap.PortScanner()
#     nm.scan(hosts='192.168.1.0/24', arguments='-sn')
                        
#     for host in nm.all_hosts():
#         if 'mac' in nm[host]['addresses']:
#             mac_address = nm[host]["addresses"]["mac"]
#             manufacturer = nm[host]["vendor"].get(mac_address, "Unknown")
#             #device={"IP":host,"MAC":mac_address,"MAN":manufacturer}
#             #device=(host,mac_address,manufacturer,)
#             #todos.append(device)
#             #insert to database
            
#             c_d.execute("INSERT INTO devices (ip, macaddress,manufacturer) VALUES(?,?,?)",(host, mac_address, manufacturer))
#             conn_devices.commit()
    
#     conn_devices.close()
#  #-------------------------------------------------------------------------------#
#     return redirect(url_for('list'))

# @app.route("/list")
# def list():

#     con = sqlite3.connect("devices.db")
#     con.row_factory = sqlite3.Row

#     cur = con.cursor()
#     cur.execute("SELECT rowid, * FROM devices") 

#     rows = cur.fetchall()
#     con.close()
#     # Send the results of the SELECT to the list.html page
#     return render_template("list.html", rows=rows)


# @app.route('/delete',methods=['POST','GET'])
# def delete():
#        if request.method == 'POST':
#         try:
#              # Use the hidden input value of id from the form to get the rowid
#             rowid = request.form['id']
#             # Connect to the database and DELETE a specific record based on rowid
#             with sqlite3.connect('devices.db') as con:
#                     cur = con.cursor()
#                     cur.execute("DELETE FROM devices WHERE rowid="+rowid)
#                     con.commit()
#         except:
#             con.rollback()

#         finally:
#             con.close()
        
#         return redirect(url_for('list'))

# #if __name__=="__main__":
#  #   app.run(host='0.0.0.0')