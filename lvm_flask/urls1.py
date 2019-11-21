from flask import Flask,views


class allLvm(views.View):
    def get_pv(self):
        return 'get_pv'


class PhysicalVolume(views.View):
    pass