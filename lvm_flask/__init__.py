#coding:utf-8
from flask import Flask,render_template,Blueprint,views,url_for,jsonify
from .Conf import config_lvm as conf


lvmStart = Blueprint('lvm', __name__, static_folder='static', template_folder='templates', url_prefix='/lvmStart')

class allLvm(views.View):
    def getpv(self):
        return 'get_pv'

@lvmStart.errorhandler(404)
def page_not_found(e):
   return render_template('404.html')

@lvmStart.route('/',methods=['GET','POST'])
def lvm_start():
    return render_template('lvmStart.html')


lvmStart.add_url_rule('/getpv/',endpoint='getpv',view_func=allLvm.as_view('getpv'))


#print ('url:',url_for('lvmStart.getpv'))