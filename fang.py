
from flask import Flask, render_template, request,redirect, url_for, flas


app = Flask(__name__)  

@app.route('/')
def index():
    return render_template('landing.html')

#if __name__=="__main__":
 #   app.run(host='0.0.0.0')
