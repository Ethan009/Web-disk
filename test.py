#coding:utf-8
import subprocess , re


def datapvs():
    data_pvs=subprocess.getoutput("pvs")
    re_pvs = r'(/^\/dev\/sd/$)'
    data_pvs=data_pvs.split('\n')
    for line in data_pvs:
        pass

    print ('data_pvs:',data_pvs)

datapvs()