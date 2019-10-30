# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import difflib
import re
import os
import sys
import subprocess
import pexpect

app = Flask(__name__)


def shell_pvcreate(str_disk):
    str_disk_name = '/dev/%s' % str_disk
    if str_disk_name:
        child = pexpect.spawn(str("pvcreate" + " " + str_disk_name))
        i = child.expect(['successfully created', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0 :
            print ('%s successfully created' % str_disk_name)
            return True
        else:
            print ('%s fail created' % str_disk_name)
            return False


def shell_pvremove(str_disk):
    str_disk_name = '/dev/%s' % str_disk
    if str_disk_name:
        child = pexpect.spawn(str("pvremove" + " " + str_disk_name))
        i = child.expect(['successfully wiped', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0 :
            print ('%s successfully wiped' % str_disk_name)
            return True
        else:
            return False


def shell_pvs():
    data_pvs = subprocess.getoutput("pvs")
    data_pvs = data_pvs.split('\n')
    pvs_lis = []
    for line in data_pvs:
        line_lis = line.split(' ')
        for data in line_lis:
            if data.find('/dev/sd') != -1:
                pvs_lis.append(data)
    return pvs_lis


def shell_pvscan():
    data_pvscan = subprocess.getoutput("pvscan")
    data_pvscan = data_pvscan.split('\n')
    pvscan_lis = []
    for line in data_pvscan:
        line_lis = line.split(' ')
        for data in line_lis:
            if data.find('/dev/sd') != -1:
                pvscan_lis.append(data)
    print ('pvscan_lis:', pvscan_lis)
    return pvscan_lis


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
    return dicDI


def data_to_json():
    lis_data = []
    lis_data_pv = []
    Diskdata_pc = datapc()
    keys = Diskdata_pc.keys()
    values = Diskdata_pc.values()
    for key, lis_value in zip(keys, values):
        dic_data = {}
        dic_data_pv = {}
        dic_data['disk'] = key
        dic_data_pv['disk'] = key
        dic_data['options'] = []
        dic_data_pv['options'] = []
        for value in lis_value:
            dic_child_data = {}
            dic_child_data['name'] = value[0]
            dic_child_data['file_system'] = value[1]
            dic_child_data['file_name'] = value[2]
            dic_child_data['status'] = value[3]
            dic_data['options'].append(dic_child_data)
            if not value[1] :
                dic_data_pv['options'].append(value[0])
        lis_data.append(dic_data)
        lis_data_pv.append(dic_data_pv)
    # print (lis_data)
    return lis_data, lis_data_pv


@app.route('/receive_pvremove')
def receive_pvremove(disk):
    global pvremove_data
    pvremove_data = []
    pvremove_str = request.args['pvremove'].strip()
    pvremove_lis = pvremove_str.split(',')
    for pvremove_disk in pvremove_lis:
        if pvremove_disk:
            if shell_pvremove(data):
                pvremove_data.append({'disk': data, 'status': 'True'})
            else:
                pvremove_data.append({'disk': data, 'status': 'fales'})
    return 'test'


@app.route('/rev_partition', methods=['GET'])
def rev_partition():
    global data_table
    data_table = []
    rev_data = request.args['pvcreate'].strip()
    rev_data = rev_data.split(',')
    for data in rev_data:
        if data:
            if shell_pvcreate(data):
                data_table.append({'disk':data , 'status': 'True'})
            else:
                data_table.append({'disk':data , 'status': 'fales'})
    return 'test'


@app.route('/pvremove')
def web_pvremove():
    pvs_data = shell_pvs()
    return render_template('pv/deletepv.html', pvs_data=pvs_data)


@app.route('/pvcreate')
def web_pvcreate():
    Diskdata, Diskdata_pv = data_to_json()
    return render_template('pv/pvcreate.html', Diskdata_pv=Diskdata_pv)


@app.route('/scanpv')
def web_scanpv():
    return render_template('pv/scanpv.html')


@app.route('/pvs')
def web_pvs():
    pvs_data = shell_pvs()
    return render_template('pv/pvs.html', pvs_data=pvs_data)


@app.route('/layer_table')
def layer_table():
    global data_table
    return render_template('test1.html', Diskdata=data_table)

# @app.route('/send_message', methods=['GET'])
# def send_message():
#     global message_get
#     message_get = ""
#     message_get = request.args['message']
#     print("收到前端发过来的信息：%s" % message_get)
#     print("收到数据的类型为：" + str(type(message_get)))
#     return "收到消息"
#
# @app.route('/change_to_json', methods=['GET'])
# def change_to_json():
#
#     global message_get
#     message_get=''
#     message_json = {
#         "message": message_get
#     }
#
#     return jsonify(message_json)


@app.route('/return_data', methods=['GET'])
def return_data():
    Diskdata, Diskdata_pv = data_to_json()
    message_json = {
        "diskdata":Diskdata_pv
    }
    return jsonify(message_json)


@app.route('/diskdata', methods=['GET', 'POST'])
def diskdata():
    Diskdata, Diskdata_pv = data_to_json()
    return Diskdata


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    lis_disk = []
    Diskdata, Diskdata_pv = data_to_json()
    # if request.method == 'POST':
    #     disk_Partition=request.values.get('hidden')
    #     #print ('122' , type(disk_Partition),disk_Partition)
    #     disk_pvcreate(disk_Partition)

    return render_template('index.html', Diskdata=Diskdata, Diskdata_pv=Diskdata_pv)


@app.route("/San2", methods=['POST', 'GET'])
def hello():
    
    data_key = dicDI.keys()
    return render_template("San2.html",
                           data_key=data_key,
                           data=dicDI 
            )

    
def send_message():
    global message_get_ll
#     一键分区
    message_get = request.args['message']
#     详细分区
    yufenqu = request.args['yufenqu']
    fqh = request.args['fqh']
    start = request.args['start']
    end = request.args['end']
#     类型
    hidden = request.args['hidden']
    xxx = request.args['xxx']
#     挂载
    wjlj = request.args['wjlj']
    ygzcpm = request.args['ygzcpm']
    if message_get:
        child = pexpect.spawn("sudo fdisk /dev/%s" % (yjfq), timeout=3)
        child.sendline('n')
        child.sendline('\n')
        child.sendline('\n')
        child.sendline('\n')
        child.sendline('\n')
        child.sendline('w')
        index = child.expect("Syncing disks") 
        if (index == 0):
            message_get_ll = "执行成功"
            return message_get_ll
        else:
            message_get_ll = "执行失败"
            return message_get_ll
    else:
        pass
    
    if yufenqu and fqh and start and end:
        child = pexpect.spawn("sudo fdisk /dev/%s" % (yufenqu), timeout=3)
        child.sendline('n')
        child.sendline('p')
        child.sendline('%s' % (fqh))
        child.sendline('%s' % (start))
        child.sendline('%s' % (end))
        child.sendline('w')
        index = child.expect("Syncing disks") 
        if (index == 0):
            message_get_ll = "执行成功"
            return message_get_ll
        else:
            message_get_ll = "执行失败"
            return message_get_ll

    else:
        pass
    
    if xxx and hidden:
        os.popen("mkfs.%s /dev/%s " % (hidden, xxx))
        message_get_ll = "执行成功"
        return message_get_ll
    else:
        pass
    
    if ygzcpm and wjlj:
        os.system("mkdir %s" % (wjjlj))
        os.system("mount /dev/%s %s" % (ygzcpm, wjjlj))
        message_get_ll = "挂载成功"
        return message_get_ll
    else:
        pass


@app.route('/change_to_json', methods=['GET'])
def change_to_json():
    global message_get_ll
    message_json = {
        "message": message_get_ll
    }
    return jsonify(message_json)


if __name__ == '__main__':
    app.run()
