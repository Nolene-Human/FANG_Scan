
#flask libraries
from flask import Flask, render_template, request, session, redirect, url_for

#python libraries
import nmap

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

user=[]
devices=[]

@app.route('/')
def index():
    session['attempt'] = 3
    return render_template('landing.html')

# if user exist direct to info_gather else deny access
@app.route('/form_login',methods=['POST','GET'])
def login():        
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
        user.append(name)
        return redirect(url_for("intel"))
    
@app.route('/Intel_gather')
def intel(): 
    return render_template('intel_gather.html')

#Called when 'Scan' button is pressed on intel_gather.html
@app.route('/scan',methods=['POST','GET'])
def scan():
    dev=sqlite3.connect('devices.db')
    d= dev.cursor()

    for u in user:
        u=u

    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')

    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]["addresses"]["mac"]
            manufacturer = nm[host]["vendor"].get(mac_address, "Unknown")
            device={"IP":host,"MAC":mac_address,"MAN":manufacturer}
            device=(host,mac_address,manufacturer,)
            devices.append(device)

            
            d.execute("INSERT INTO devices (user, ip, macaddress,manufacturer) VALUES(?,?,?,?)",(u,host, mac_address, manufacturer))
            dev.commit()
    
    dev.close()
  #-------------------------------------------------------------------------------#

    # return ("Scan complete")
    return redirect(url_for('list'))

@app.route("/list")
def list():

    con = sqlite3.connect("devices.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    listd = "SELECT rowid, ip,macaddress, manufacturer FROM devices"
    cur.execute(listd)

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
                    deldev="DELETE FROM devices WHERE rowid = ?"
                    cur.execute(deldev,(rowid))
                    con.commit()
        except:
            con.rollback()

        finally:
            con.close()
        
        return redirect(url_for('list'))

@app.route("/exit")
def exit():
    user.clear()
    devices.clear()
    return render_template("exit.html")

@app.route("/welcome")
def welcome():
    return render_template('otp.html')
    # if valid==0:
    #     # pyfile.otp.generate_code(key)
    #     # unq_code=pyfile.otp.generatepin(key)
    #     # print(unq_code)
    #     savecode="QRCODE"
    #     #savecode='static/codes/'+qr
    #     return render_template('otp.html', savecode=savecode)
    # else:
    #     return("This account has already been verified")



if __name__ == "__main__":
  app.run()
