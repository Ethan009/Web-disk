#coding:utf-8
import pexpect,subprocess,re

class pe(object):
    """docstring for pe"""
    def __init__(self, cmd):
        # super(pe, self).__init__()
        self.objCMD = pexpect.spawn(cmd)

    def sendline(self, sub_cmd):
        self.objCMD.sendline(sub_cmd)

    def expect(self, str):
        try:
            self.objCMD.expect(str)
        except:
            return False
        return True

class DiskStatus(pe):
    def __init__(self):
        pass

    def datapc(self):

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

    def data_to_json(self):
        lis_data = []
        lis_data_pv = []
        Diskdata_pc = self.datapc()
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
                if not value[1]:
                    dic_data_pv['options'].append(value[0])
            lis_data.append(dic_data)
            lis_data_pv.append(dic_data_pv)
        # print (lis_data)
        return lis_data, lis_data_pv


class PhysicalVolume(pe):
    def __init__(self):
        pass

    def shell_pvcreate(self,str_disk):
        str_disk_name='/dev/%s' % str_disk
        if str_disk_name:
            child = pexpect.spawn(str("pvcreate" + " " + str_disk_name))
            i = child.expect(['successfully created',pexpect.TIMEOUT,pexpect.EOF])
            if i == 0 :
                #print ('%s successfully created' % str_disk_name)
                return True
            else:
                #print ('%s fail created' % str_disk_name)
                return False

    def shell_pvremove(self,str_disk):
        if str_disk:
            child = pexpect.spawn(str("pvremove" + " " + str_disk))
            i = child.expect(['successfully wiped',pexpect.TIMEOUT,pexpect.EOF])
            if i == 0 :
                print ('%s successfully wiped' % str_disk)
                return True
            else:
                print ('%s fail wiped' % str_disk)
                return False


    def shell_pvs(self):
        data_pvs=subprocess.getoutput("pvs")
        data_pvs=data_pvs.split('\n')
        pvs_lis=[]
        for line in data_pvs:
            line_lis = line.split(' ')
            for data in line_lis:
                if data.find('/dev/sd') != -1:
                    pvs_lis.append(data)
        return pvs_lis


    def shell_pvscan(self):
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


class VolumeGroup(pe):
    def __init__(self):
        pass

    def shell_vgdisplay_vgname(self):
        data_vgdisplay = subprocess.getoutput("vgdisplay")
        data_vgdisplay = data_vgdisplay.split('\n')
        vg_name_lis = []
        for line in data_vgdisplay:
            if line.find('VG Name') != -1:
                reVGName = re.compile('(?<=VG Name).*')
                if reVGName.search(line):
                    a = reVGName.search(line).group().strip()
                    vg_name_lis.append(a)
        return vg_name_lis

    def shell_vgdisplay_pv(self,vgname):
        shell = "vgdisplay -v " + str(vgname)
        data_vgdisplay_pv = subprocess.getoutput(str(shell))
        data_vgdisplay_pv = data_vgdisplay_pv.split('\n')
        vg_pv_name_lis = []
        for line in data_vgdisplay_pv:
            if line.find('PV Name') != -1:
                rePVName = re.compile('(?<=PV Name).*')
                if rePVName.search(line):
                    a = rePVName.search(line).group().strip()
                    vg_pv_name_lis.append(a)
        return vg_pv_name_lis

    def shell_vgcreate(self,vg_name, pv_to_vg_lis):
        pv_str = ''
        for pv_name in pv_to_vg_lis:
            pv_str = pv_str + ' ' + pv_name
        if pv_to_vg_lis:
            shell = "vgcreate" + " " + vg_name + pv_str
            child = pexpect.spawn(str(shell))
            i = child.expect(['successfully created', pexpect.TIMEOUT, pexpect.EOF])
            if i == 0:
                print('%s successfully created' % vg_name)
                return True
            else:
                print('%s fail created' % vg_name)
                return False

    def shell_vgremove(self,vg_name):
        if vg_name:
            child = pexpect.spawn(str("vgremove" + " " + vg_name))
            i = child.expect(['successfully removed', pexpect.TIMEOUT, pexpect.EOF])
            if i == 0:
                print('%s successfully removed' % vg_name)
                return True
            else:
                print('%s fail removed' % vg_name)
                return False

    def shell_vgextend(self,vg_name, extend_pv_lis):
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

    def shell_vgreduce(self,vg_name, reduce_pv):
        if reduce_pv:
            shell = "vgreduce" + " " + vg_name + " " + reduce_pv
            print('shell', shell)
            child = pexpect.spawn(str(shell))
            i = child.expect(['Removed', pexpect.TIMEOUT, pexpect.EOF])
            if i == 0:
                print('%s successfully reduceed' % vg_name)
                return True
            else:
                print('%s fail reduceed' % vg_name)
                return False

class LogicalVolume(pe):
    def __init__(self):
        pass

    def shell_lvdisplay(self):
        data_lvdisplay = subprocess.getoutput("lvdisplay")
        data_lvdisplay = data_lvdisplay.split('\n')
        lv_name_lis = []
        for line in data_lvdisplay:
            if line.find('LV Name') != -1:
                reLVName = re.compile('(?<=LV Name).*')
                if reLVName.search(line):
                    a = reLVName.search(line).group().strip()
            if line.find('VG Name') != -1:
                reVGName = re.compile('(?<=VG Name).*')
                if reVGName.search(line):
                    b = reVGName.search(line).group().strip()
                    lvname=b+'-'+a
                    lv_name_lis.append(lvname)
        return lv_name_lis


