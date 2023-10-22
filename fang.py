from flask import Flask, render_template, request,redirect, url_for
import sqlite3

import nmap

app = Flask(__name__)

database={'nina@gmail.com':'123'}    

@app.route('/')
def index():
    return render_template('index.html')

# if user exist direct to info_gather else deny access
@app.route('/form_login',methods=['POST'])
def login():
    name1=request.form["username"]
    password=request.form["uniqekey"]
    
    if name1 in database and password=='123':
        return redirect(url_for("intel"))
    else:
        return ("Access Denied")
    

    
@app.route('/Intel_gather')
def intel():
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