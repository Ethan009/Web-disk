#coding:utf-8
import pexpect

#規則：



class shell_pexpect:
    def __init__(self,cmd):
        cmd=self.cmd
        child=pexpect.spawn(cmd)
        data=pexpect.run(cmd)
        value=0

    def disk_pvcreate(self):
        try:
            if self.child.expect('successfully created')==self.value:
                return 'successfully created'
            else:
                return self.data
        except pexpect.EOF or pexpect.TIMEOUT:
            return self.data

    def disk_single_partition(self):
        lis_info=[['Command (m for help)'],['Select(default p)'],['Partition number'],['First sector'],['Last sector'],['Command (m for help)']]
        lis_info_CN=[['命令(输入m获取帮助)'],['Select(default p)'],[('分区号')],['First sector'],['Last sector'],['命令(输入m获取帮助)']]
        lis_shell=['n','\n','\n','\n','\n','w']
        try:
            for i,j in lis_info,lis_shell:
                if self.child.expect(i)==self.value:
                    self.child.sendline(j)
                else:
                    return 'partition failed'
                    self.child.close()
        except pexpect.EOF or pexpect.TIMEOUT:
            self.child.close()
            return'partition failed'
        return 'partition successful'





    def disk_manual_partition(self):
        pass


    def enter_command(self,next_command):
        str_command=['Command (m for help)']
        try:
            if self.child.expect(str_command)==self.value:
                return '0'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

#返回值--0:主分區 01：拓展分區 02：免費分區
    def enter_select(self, enter_cmd):
        str_command = ['Select(default p)','Select(default e)','No free sectors available','All primary partitions are in use']
        try:
            self.child.sendline(enter_cmd)
            i = self.child.expect(str_command)
            if i == self.value:
                return '0'
            elif i == 1:
                return '01'
            elif i == 2:
                return 'No free sectors available'
            elif i == 3:
                return '02'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

    def enter_partition_number(self,next_command):
        str_command=['Partition number']
        try:
            if self.child.expect(str_command) == self.value:
                self.child.sendline(next_command)
                return '0'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

    def enter_First_sector(self,next_command):
        str_command = ['First sector']
        try:
            if self.child.expect(str_command) == self.value:
                self.child.sendline(next_command)
                return '0'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

    def enter_First_sector(self, next_command):
        str_command = ['Last sector, +sectors or +size']
        try:
            if self.child.expect(str_command) == self.value:
                self.child.sendline(next_command)
                return '0'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

