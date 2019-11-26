#coding:utf-8
from flask import Blueprint,url_for
from lvm_flask import urls

lvmHome=urls.lvmHome()
lvmInstall=urls.lvmInstall()
lvmShow=urls.lvmShow()

lvmStart = Blueprint('lvm', __name__, static_folder='static', template_folder='templates', url_prefix='/lvmStart')

lvmStart.add_url_rule('/', view_func=lvmHome.as_view('/'))
lvmStart.add_url_rule('/lvmInstall/', endpoint='lvmInstall', view_func=lvmInstall.as_view('lvmInstall'))
lvmStart.add_url_rule('/lvmShow/', endpoint='lvmShow', view_func=lvmShow.as_view('lvmShow'))
