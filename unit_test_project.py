#coding:utf-8
import build_pexpect as p
import pexpect

a=pexpect.spawn('ls')
c=pexpect.run('ls')

b=a.expect(['111111','eeeeeeee','README.md'])

print (b)