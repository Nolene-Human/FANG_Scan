from flask import Flask, render_template, request,redirect, url_for
import sqlite3

import nmap

app = Flask(__name__)   
database={'client@gmail.com':'123'}

@app.route('/')
def index():
    return render_template('index.html')

# if user exist direct to info_gather else deny access
@app.route('/form_login',methods=['POST','GET'])
def login():

    if request.method =='POST':
        conn=sqlite3.connect('clients.db')
        c= conn.cursor()
    
    
        name1=request.form["username"]
        key=request.form["uniqekey"]
    


        validate="SELECT email,key FROM clients where email='"+name1+"'and key ='"+key+"'" 
        c.execute(validate)

        result=c.fetchall()
        print(result)

    #validate 
        if len(result)==0:
            return("You are not authorised to enter the site with credentials provided")
        else:
            return redirect(url_for('intel'))

@app.route('/Intel_gather')
def intel():   
        
    if request.method =='POST':
        return ('You scanned the network')


    else:
        return render_template('intel_gather.html')

@app.route('/Scan_network')
def scan_network_devices():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')
                    
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]["addresses"]["mac"]
            manufacturer = nm[host]["vendor"].get(mac_address, "Unknown")
            return ("IP Address: {}, MAC Address: {}, Manufacturer: {}".format(host, mac_address, manufacturer))
    
#if __name__=="__main__":
 #   app.run(host='0.0.0.0')