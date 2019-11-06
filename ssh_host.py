#coding:utf-8
import pexpect

def login(user, passwd, ip, command):
    child = pexpect.spawn('ssh  %s@%s "%s"' % (user, ip, command))
    fout = open('cmd.txt','wb')
    child.logfile = fout
    o = ''
    try:
        i = child.expect(['[Pp]assword:', 'continue connecting (yes/no)?'])
        if i == 0:
            child.sendline(passwd)
        elif i == 1:
            child.sendline('yes')
        else:
            pass
    except pexpect.EOF:
        child.close()
    else:
        o = child.read()
        child.expect(pexpect.EOF)
        child.close()
    return o


def data():
    hosts = file('hosts2.list', 'r')
    for line in hosts.readlines():
        host = line.strip("\n")
        if host:
            ip, user, passwd, commands = host.split(":")
        for command in commands.split(","):
            data = login(user, passwd, ip, command)
    return data
    hosts.close()