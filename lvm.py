#coding:utf-8
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/formts')
def formts():
    return render_template('form.html')

@app.route('/')
def index():
    return render_template('lvm.html')

if __name__ == '__main__':
    app.run()
