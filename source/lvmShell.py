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


class PhysicalVolume(pe):
    def __init__(self):
        pass

    def shell_pvcreate(self,str_disk):
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
