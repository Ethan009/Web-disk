#coding:utf-8
import pexpect

class myerorr(Exception):
    pass

class Faleserorr(myerorr):
    pass

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
            print ('11')
        return True


class p_disk():
    """docstring for p_disk"""
    def __init__(self, disk):
        self.objCMD = pexpect.spawn('fdisk /dev/%s' % str(disk))
        a=pexpect.run('fdisk /dev/%s' % str(disk))



    def start(self):
        a = self.objCMD.expect('Command (m for help)')
        if a==0:
            print ('111')
            return True
        else:
            print('No such file or directory')

    def new_part(self):
        self.objCMD.sendline('n')
        if self.objCMD.expect('default'):
            return True
        elif self.objCMD.expect('No free sectors available.'):
            print('No Space Left...')

    def partition_munber(self):
        self.objCMD.sendline('\n')
        if self.objCMD.expect('Partition number'):
            return True

    def first_sector(self):
        self.objCMD.sendline('\n')
        if self.objCMD.expect('First sector'):
            return True

    def last_sector(self):
        self.objCMD.sendline('\n')
        if self.objCMD.expect('Last sector'):
            return True

    def confirm(self):
        self.objCMD.sendline('\n')
        if self.objCMD.expect('Created a new partition'):
            return True

    def confirm_size(self,size):
        self.objCMD.sendline(str(size))
        if self.objCMD.expect('Created a new partition'):
            return True

    def partition_write(self):
        self.objCMD.sendline('w')
        if self.objCMD.expect('The partition table has been altered'):
            return True

    def create_only_one_part(self):
        if self.start():
            self.new_part()
            self.partition_munber()
            self.first_sector()
            self.last_sector()
            self.confirm()
            self.partition_write()
            print ('successful create partition')
        else:
            print ('partition fales')



    def create_fix_size_part(self,size):
        try:
            self.start()
            self.new_part()
            self.partition_munber()
            self.first_sector()
            self.last_sector()
            self.confirm_size(str(self.size))
            self.partition_write()
            print('successful create partition')
        except Exception:
            print ('pattition fales')