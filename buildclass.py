#coding:utf-8
import pexpect

#規則：



class shell_pexpect:
    def __init__(self,cmd,partition='n',select='\n',partition_number='\n',sector='\n',partition_size='\n',write_cmd='w'):
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

    # def disk_single_partition(self):
    #     lis_info=[['Command (m for help)'],['Select(default p)'],['Partition number'],['First sector'],['Last sector'],['Command (m for help)']]
    #     lis_info_CN=[['命令(输入m获取帮助)'],['Select(default p)'],[('分区号')],['First sector'],['Last sector'],['命令(输入m获取帮助)']]
    #     lis_shell=['n','\n','\n','\n','\n','w']
    #     try:
    #         for i,j in lis_info,lis_shell:
    #             if self.child.expect(i)==self.value:
    #                 self.child.sendline(j)
    #             else:
    #                 return 'partition failed'
    #                 self.child.close()
    #     except pexpect.EOF or pexpect.TIMEOUT:
    #         self.child.close()
    #         return'partition failed'
    #     return 'partition successful'
    # def disk_manual_partition(self):
    #     pass

#返回值--0：進入幫助頁  1：無此文件
    def enter_command(self):
        str_command=['Command (m for help)','No such file or directory']
        try:
            i=self.child.expect(str_command)
            if i==self.value:
                return '0'
            elif i==1:
                return '01'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

#返回值--0:主分區 01：拓展分區 02：免費分區 11：無空閒扇區  12：將主分區拓展爲拓展分區
    def enter_select(self, enter_cmd):
        str_command = ['Select(default p)','Select(default e)','No free sectors available',
                       'All primary partitions are in use','To create more partitions']
        try:
            self.child.sendline(enter_cmd)
            i = self.child.expect(str_command)
            if i == self.value:
                return '0'
            elif i == 1:
                return '01'
            elif i == 2:
                return '11'
            elif i == 3:
                return '02'
            elif i == 4:
                return '12'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

#返回值--0：默認值  01：超出範圍，重新輸入
    def enter_partition_number(self, enter_cmd):
        str_command=['Partition number','Value out of range']
        try:
            self.child.sendline(enter_cmd)
            i = self.child.expect(str_command)
            if i == self.value:
                return '0'
            elif i == 1:
                return '01'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

#返回值--0：默認或者輸入值  01：超出範圍重新輸入
    def enter_First_sector(self,enter_cmd):
        str_command = ['Value out of range','First sector']
        try:
            self.child.sendline(enter_cmd)
            i = self.child.expect(str_command)
            if i == 1:
                return '0'
            elif i == 0:
                return '01'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

#返回值--0：默認
    def enter_partition_size(self, enter_cmd):
        str_command = ['Last sector, +sectors or +size','Value out of range']
        try:
            self.child.sendline(enter_cmd)
            i = self.child.expect(str_command)
            if i == self.value:
                return '0'
            elif i == 1:
                return '01'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

    def enter_size(self,enter_cmd):
        str_command = ['Created a new partition','Last sector, +sectors or +size','Value out of range']
        try:
            self.child.sendline(enter_cmd)
            i = self.child.expect(str_command)
            if i == self.value:
                return '0'
            elif i == 1:
                return '01'
            else:
                return '1'
        except pexpect.EOF or pexpect.TIMEOUT:
            return 'partition failed'

    def disk_single_partition(self):
        self.enter_command()

