# -*- coding: utf-8 -*-


from flask import Flask,render_template,request,jsonify,Blueprint,views
import difflib
import re
import os
import sys
import subprocess
import pexpect
from lvm_flask import lvmStart
from datetime import timedelta
#from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
#bootstrap = Bootstrap(app)


def shell_pvcreate(str_disk):
    str_disk_name='/dev/%s' % str_disk
    if str_disk_name:
        child = pexpect.spawn(str("pvcreate" + " " + str_disk_name))
        i = child.expect(['successfully created',pexpect.TIMEOUT,pexpect.EOF])
        if i == 0 :
            print ('%s successfully created' % str_disk_name)
            return True
        else:
            print ('%s fail created' % str_disk_name)
            return False


def shell_pvremove(str_disk):
    if str_disk:
        child = pexpect.spawn(str("pvremove" + " " + str_disk))
        i = child.expect(['successfully wiped',pexpect.TIMEOUT,pexpect.EOF])
        if i == 0 :
            print ('%s successfully wiped' % str_disk)
            return True
        else:
            print ('%s fail wiped' % str_disk)
            return False


def shell_pvs():
    data_pvs=subprocess.getoutput("pvs")
    data_pvs=data_pvs.split('\n')
    pvs_lis=[]
    for line in data_pvs:
        line_lis = line.split(' ')
        for data in line_lis:
            if data.find('/dev/sd') != -1:
                pvs_lis.append(data)
    return pvs_lis


def shell_pvscan():
    data_pvscan=subprocess.getoutput("pvscan")
    data_pvscan=data_pvscan.split('\n')
    pvscan_lis=[]
    for line in data_pvscan:
        line_lis = line.split(' ')
        for data in line_lis:
            if data.find('/dev/sd') != -1:
                pvscan_lis.append(data)
    print ('pvscan_lis:', pvscan_lis)
    return pvscan_lis


def shell_vgdisplay_vgname():
    data_vgdisplay=subprocess.getoutput("vgdisplay")
    data_vgdisplay=data_vgdisplay.split('\n')
    vg_name_lis=[]
    for line in data_vgdisplay:
        if line.find('VG Name') != -1:
            reVGName = re.compile('(?<=VG Name).*')
            if reVGName.search(line):
                a = reVGName.search(line).group().strip()
                vg_name_lis.append(a)
    return vg_name_lis

def shell_vgdisplay_pv(vgname):
    shell="vgdisplay -v " + str(vgname)
    data_vgdisplay_pv=subprocess.getoutput(str(shell))
    data_vgdisplay_pv=data_vgdisplay_pv.split('\n')
    vg_pv_name_lis=[]
    for line in data_vgdisplay_pv:
        if line.find('PV Name') != -1:
            rePVName = re.compile('(?<=PV Name).*')
            if rePVName.search(line):
                a = rePVName.search(line).group().strip()
                vg_pv_name_lis.append(a)
    return vg_pv_name_lis

def shell_vgcreate(vg_name,pv_to_vg_lis):
    pv_str=''
    for pv_name in pv_to_vg_lis:
        pv_str=pv_str + ' ' + pv_name
    if pv_to_vg_lis:
        shell="vgcreate" + " " + vg_name + pv_str
        child = pexpect.spawn(str(shell))
        i = child.expect(['successfully created', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            print('%s successfully created' % vg_name)
            return True
        else:
            print('%s fail created' % vg_name)
            return False

def shell_vgremove(vg_name):
    if vg_name:
        child = pexpect.spawn(str("vgremove" + " " + vg_name))
        i = child.expect(['successfully removed',pexpect.TIMEOUT,pexpect.EOF])
        if i == 0 :
            print ('%s successfully removed' % vg_name)
            return True
        else:
            print ('%s fail removed' % vg_name)
            return False

def shell_vgextend(vg_name,extend_pv_lis):
    pv_str = ''
    for pv_name in extend_pv_lis:
        pv_str = pv_str + ' ' + pv_name
    if extend_pv_lis:
        shell = "vgextend" + " " + vg_name + pv_str
        child = pexpect.spawn(str(shell))
        i = child.expect(['successfully extended', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            print('%s successfully extended' % vg_name)
            return True
        else:
            print('%s fail extended' % vg_name)
            return False

def shell_vgreduce(vg_name,reduce_pv):
    if reduce_pv:
        shell = "vgreduce" + " " + vg_name + " " + reduce_pv
        print ('shell',shell)
        child = pexpect.spawn(str(shell))
        i = child.expect(['Removed', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            print('%s successfully reduceed' % vg_name)
            return True
        else:
            print('%s fail reduceed' % vg_name)
            return False

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

#[{vgname:vgname,pvname:['/dev/sd1','/dev/sda2']},{},{}]
#[{vgname:vgname , options : [{pvname:pvname,size:size}]}]
def all_vg_pv():
    vg_name_lis=shell_vgdisplay_vgname()
    all_vg_pv=[]
    for vg_name in vg_name_lis:
        pv_name=shell_vgdisplay_pv(vg_name)
        for i in range(len(pv_name)):
            pv_name[i]={'pvname':pv_name[i],'Size':'暫未開放'}
        dic_vg_pv = {'vgname': vg_name}
        dic_vg_pv['options'] = pv_name
        all_vg_pv.append(dic_vg_pv)
    return all_vg_pv







@app.route('/receive_pvremove')
def receive_pvremove():
    global pvremove_data
    pvremove_data = []
    pvremove_disk = request.args['pvremove']
    if pvremove_disk:
        if shell_pvremove(pvremove_disk):
            pvremove_data.append({'disk': pvremove_disk, 'status': 'True'})
        else:
            pvremove_data.append({'disk': pvremove_disk, 'status': 'fales'})
    return 'test'


@app.route('/rev_partition',methods=['GET'])
def rev_partition():
    global data_table
    data_table=[]
    rev_data = request.args['pvcreate'].strip()
    rev_data=rev_data.split(',')
    for data in rev_data:
        if data:
            if shell_pvcreate(data):
                data_table.append({'disk':data ,'status': 'True'})
            else:
                data_table.append({'disk':data ,'status': 'false'})
    return 'test'

@app.route('/pvremove')
def web_pvremove():
    pvs_data=shell_pvs()
    return render_template('pv/deletepv.html',pvs_data=pvs_data)

@app.route('/vgs')
def web_vgs():
    return render_template('vg/vgs.html')

@app.route('/vgcreate')
def web_vgcreate():
    return render_template('vg/vgcreate.html')



@app.route('/vgremove',methods=['GET','POST'])
def web_vgremove():
    global vg_name
    if request.method == 'GET':
        vg_name = request.args['vgname_web']
    return render_template('vg/vgremove.html')


@app.route('/pvcreate')
def web_pvcreate():
    Diskdata, Diskdata_pv = data_to_json()
    return render_template('pv/pvcreate.html',Diskdata_pv=Diskdata_pv)

@app.route('/scanpv')
def web_scanpv():
    return render_template('pv/scanpv.html')

@app.route('/vg',methods=['GET','POST'])
def web_vg():
    vg_data=all_vg_pv()
    vg_name=shell_vgdisplay_vgname()
    if request.method=='GET':
        data=request.values.get('selectfunct')
    return render_template('vg/vg.html',VGdata=vg_data,VGname=vg_name)


@app.route('/pvs')
def web_pvs():
    pvs_data=shell_pvs()
    return render_template('pv/pvs.html',pvs_data=pvs_data)

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

@app.route('/return_data',methods=['GET'])
def return_data():
    Diskdata, Diskdata_pv = data_to_json()
    message_json={
        "diskdata":Diskdata_pv
    }
    return jsonify(message_json)


@app.route('/diskdata',methods=['GET','POST'])
def diskdata():
    Diskdata, Diskdata_pv = data_to_json()
    return Diskdata


@app.route("/San2", methods=['POST', 'GET'])
def hello():
    if request.method == "POST":
        yjfq = request.values.get('yjfq')  # 一键分区
        yufenqu = request.values.get('yufenqu')  # 预分区磁盘
        fengquhao = request.values.get('fengquhao')  # 分区号
        start = request.values.get('start')  # 开始
        end = request.values.get('end')  # 结束
        ygzcpm = request.values.get('ygzcpm')  # 预挂载磁盘
        wjjlj = request.values.get('wjjlj')  # 文件夹路径输入
        hidden = request.values.get('hidden')  # 文件类型选择
        xxx = request.values.get('xxx')  # 当前磁盘分区

        # 格式化文件类型
        if hidden and xxx:
            os.popen("mkfs.%s /dev/%s " % (hidden, xxx))
            print("格式化成功")
        else:
            # print("格式化失败")
            pass

        # 一键分区
        # print(yjfq)
        if yjfq:
            child = pexpect.spawn("sudo fdisk /dev/%s" % (yjfq), timeout=3)
            child.sendline('n')
            child.sendline('\n')
            child.sendline('\n')
            child.sendline('\n')
            child.sendline('\n')
            child.sendline('w')
            print("Successful to Partition")
        else:
            # print("faild to Partition")
            pass

        # 手动分区
        if yufenqu and fengquhao and start and end:
            child = pexpect.spawn("sudo fdisk /dev/%s" % (yufenqu), timeout=3)
            child.sendline('n')
            child.sendline('p')
            child.sendline('%s' % (fengquhao))
            child.sendline('%s' % (start))
            child.sendline('%s' % (end))
            child.sendline('w')
            print("Successful to Partition")
        else:
            # print("faild to Partition")
            pass

        # 磁盘挂载
        if ygzcpm and wjjlj:
            os.system("mkdir %s" % (wjjlj))
            print("创建文件夹成功")
            os.system("mount /dev/%s %s" % (ygzcpm, wjjlj))
            print("挂载成功")
        else:
            pass

    data_key = datapc().keys()
    return render_template("San2.html",
                           data_key=data_key,
                           data=datapc()
            )


app.register_blueprint(lvmStart)

@app.route('/',methods=['GET','POST'])
def hello_world():
    lis_disk=[]
    Diskdata,Diskdata_pv=data_to_json()
    # if request.method == 'POST':
    #     disk_Partition=request.values.get('hidden')
    #     #print ('122' , type(disk_Partition),disk_Partition)
    #     disk_pvcreate(disk_Partition)
    return render_template('index.html',Diskdata=Diskdata,Diskdata_pv=Diskdata_pv)



if __name__ == '__main__':
    app.run( debug=True,port=9090)
