# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,jsonify
import difflib
import re
import os
import sys
import subprocess
import pexpect

# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)

def disk_view():
    diskmount = subprocess.getoutput("lsblk -lf ")
    return diskmount


def datapc():

    datapc = subprocess.getoutput("lsblk -lf ")
    # 正则表达式
    re_disk_device = r'(sd[a-z]{1,2}\b)'
    re_partition_no_fs = r'.*(sd\D{1,2}\d{1,2})'
    re_partition_fs_not_mount = r'.*(sd\D{1,2}\d{1,2}) (\S+).*[^/]'
    re_partition_fs_mounted = r'(sd\D{1,2}\d{1,2}) (\S+).* (/.*)'

    lst_line = datapc.split('\n')

    lstDisk = []
    dicDI = {}

    for line in lst_line:
        re_disk_device_result = re.match(re_disk_device, line)
        re_partition_no_fs_result = re.match(re_partition_no_fs, line)
        re_partition_fs_not_mount_result = re.match(re_partition_fs_not_mount, line)
        re_partition_fs_mounted_result = re.match(re_partition_fs_mounted, line)

        if re_disk_device_result:
            disk_device = str(re_disk_device_result.group())
            lstDisk.append(disk_device)
            dicDI[disk_device] = []
            continue
        else:
            if re_partition_fs_mounted_result:
                lstPartion = re_partition_fs_mounted_result.groups()
                lstPartion = list(lstPartion)
                lstPartion.append('0')
                if lstDisk:
                    dicDI[lstDisk[-1]].append(list(lstPartion))
                continue
            elif re_partition_fs_not_mount_result:
                lstPartion = re_partition_fs_not_mount_result.groups()
                lstPartion = list(lstPartion)
                lstPartion.append('')
                lstPartion.append('1')
                if lstDisk:
                    dicDI[lstDisk[-1]].append(list(lstPartion))
                continue
            elif re_partition_no_fs_result:
                lstPartion = re_partition_no_fs_result.groups()
                lstPartion = list(lstPartion)
                lstPartion.append('')
                lstPartion.append('')
                lstPartion.append('2')
                if lstDisk:
                    dicDI[lstDisk[-1]].append(list(lstPartion))
                continue
    # print(lstDisk)
    # pprint.pprint(dicDI)
    #print (dicDI)
    return dicDI
# keys: <class 'dict_keys'> dict_keys(['sda', 'sdb', 'sdc', 'sdd', 'sde'])
# values: <class 'dict_values'> dict_values([[['sda1', '', '', '2']], 
#     [['sdb1', '', '', '2'], ['sdb2', '', '', '2'], ['sdb3', '', '', '2'], ['sdb4', '', '', '2']],
#      [['sdc1', '', '', '2'], ['sdc2', '', '', '2'], ['sdc3', '', '', '2'], ['sdc4', '', '', '2']],
#      [['sdd1', '', '', '2']], 
#      []])

def data_to_json():
    lis_data=[]
    lis_data_pv=[]
    Diskdata_pc = datapc()
    keys=Diskdata_pc.keys()
    values=Diskdata_pc.values()
    for key,lis_value in zip(keys,values):
        dic_data={}
        dic_data_pv={}
        dic_data['disk']=key
        dic_data_pv['disk']=key
        dic_data['options'] = []
        dic_data_pv['options'] = []
        for value in lis_value:
            dic_child_data={}
            dic_child_data['name']=value[0]
            dic_child_data['file_system']=value[1]
            dic_child_data['file_name']=value[2]
            dic_child_data['status']=value[3]
            dic_data['options'].append(dic_child_data)
            if not value[1] :
                dic_data_pv['options'].append(value[0])
        lis_data.append(dic_data)
        lis_data_pv.append(dic_data_pv)
    #print (lis_data)
    return lis_data,lis_data_pv



def disk_pvcreate(str_disk):
    str_disk_name='/dev/%s' % str_disk
    print ('str_disk_name',str_disk_name)
    if str_disk_name:
        child = pexpect.spawn(str("pvcreate" + " " + str_disk_name))
        i = child.expect(['successfully created',pexpect.TIMEOUT,pexpect.EOF])
        if i == 0 :
            print ('%s successfully created' % str_disk_name)
            return True
        else:
            return False


# @app.route('/pvcreate-data',methods=['GET','POST'])
# def pvcreate_data():
#     if request.method == 'POST':
#         disk_data=data_to_json()[0]
#     return disk_data




@app.route('/rev_partition',methods=['GET'])
def rev_partition():
    global data_table
    data_table=[]
    rev_data = request.args['pvcreate'].strip()
    rev_data=rev_data.split(',')
    for data in rev_data:
        if data:
            if disk_pvcreate(data):
                data_table.append({'disk':data ,'status': 'True'})
            else:
                data_table.append({'disk':data ,'status': 'fales'})
    print ('rev_data:',rev_data)
    print ('data_table:',data_table)
    return 'test'


@app.route('/layer_table')
def layer_table():
    global data_table
    return render_template('test1.html', Diskdata=data_table)


@app.route('/send_message', methods=['GET'])
def send_message():
    global message_get
    message_get = ""
    message_get = request.args['message']
    print("收到前端发过来的信息：%s" % message_get)
    print("收到数据的类型为：" + str(type(message_get)))
    return "收到消息"

@app.route('/change_to_json', methods=['GET'])
def change_to_json():

    global message_get
    message_get=''
    message_json = {
        "message": message_get
    }

    return jsonify(message_json)

@app.route('/diskdata',methods=['GET','POST'])
def diskdata():
    Diskdata, Diskdata_pv = data_to_json()
    return Diskdata

@app.route('/',methods=['GET','POST'])
def hello_world():
    #Diskdata=disk_view()
    lis_disk=[]
    Diskdata,Diskdata_pv=data_to_json()
    # if request.method == 'POST':
    #     disk_Partition=request.values.get('hidden')
    #     #print ('122' , type(disk_Partition),disk_Partition)
    #     disk_pvcreate(disk_Partition)

    return render_template('index.html',Diskdata=Diskdata,Diskdata_pv=Diskdata_pv)



if __name__ == '__main__':
    app.run()
