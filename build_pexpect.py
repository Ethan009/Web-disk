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
            self.objCMD.expect(str,pexpect.EOF,pexpect.TIMEOUT)
        except:
            self.objCMD.close(force=True)
        return True


class p_disk(pe):
    """docstring for p_disk"""
    def __init__(self, disk, size=None):
        # super(p_disk, self).__init__()
        # self.arg = arg
        self.objCMD = pexpect.spawn('fdisk /dev/%s' % str(disk))
        self.size=size
        # self.exist_part =

    def start(self):
        if self.expect('Command (m for help)'):
            return True
        else:
            print('No such file or directory')

    def new_part(self):
        self.sendline('n')
        if self.expect('default'):
            return True
        elif self.expect('No free sectors available.'):
            print('No Space Left...')

    def partition_munber(self):
        self.sendline('\n')
        if self.expect('Partition number'):
            return True

    def first_sector(self):
        self.sendline('\n')
        if self.expect('First sector'):
            return True

    def last_sector(self):
        self.sendline('\n')
        if self.expect('Last sector'):
            return True

    def confirm(self):
        self.sendline('\n')
        if self.expect('Created a new partition'):
            return True

    def confirm_size(self,size):
        self.sendline(str(size))
        if self.expect('Created a new partition'):
            return True

    def partition_write(self):
        self.sendline('w')
        if self.expect('The partition table has been altered'):
            return True

    def create_only_one_part(self):
        try:
            self.start()
            self.new_part()
            self.partition_munber()
            self.first_sector()
            self.last_sector()
            self.confirm()
            self.partition_write()
            print ('successful create partition')
        except Exception:
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