#coding:utf-8
import build_pexpect as p
import pexpect

a = p.p_disk('sdd')
a.create_only_one_part()