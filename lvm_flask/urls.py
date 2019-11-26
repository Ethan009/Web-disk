from flask import Flask,views,render_template
from source import lvmShell

class lvmHome(views.View):
    def dispatch_request(self):
        return render_template('htmlModel/base.html')

class lvmInstall(views.View):
    def dispatch_request(self):
        return render_template('lvmInstall.html')

class lvmShow(views.View):
    def dispatch_request(self):
        return render_template('lvmChild.html')


class PhysicalVolume(views.View):
    pass