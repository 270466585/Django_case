#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import paramiko
import time
class modify_keep(object):
    def __init__(self,settings,page,pages,action):
        self.__lvshostip = settings[0].IntranetIP
        self.__port = 22
        self.__username = settings[0].username
        self.__password = settings[0].password
        self.__reload = 'sudo /etc/init.d/keepalived reload'
        self.__ipvs = 'sudo /sbin/ipvsadm -ln |wc -l'
        if page == '0':
            self.__cmd = None
        elif page == '1':
            self.__cmd = 'sudo /usr/bin/python2.6 %smodify_keep.py %s %s'%(settings[0].ScriptLocation,' '.join(settings[0].Intranetonegroup.split(',')),action)
        elif page == '2':
            self.__cmd = 'sudo /usr/bin/python2.6 %smodify_keep.py %s %s'%(settings[0].ScriptLocation,' '.join(settings[0].Intranettwogroup.split(',')),action)
        elif page == '3':
            self.__cmd = 'sudo /usr/bin/python2.6 %smodify_keep.py %s %s' %(settings[0].ScriptLocation, ' '.join(pages.split(',')), action)

    def ipvsadm(self):
        time.sleep(5)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.__lvshostip, self.__port, self.__username, self.__password)
        stdin, stdout, stderr = ssh.exec_command(self.__ipvs)
        OUT = stdout.read()
        ssh.close()
        return OUT


    def Landed(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.__lvshostip,self.__port,self.__username,self.__password)
        stdin, stdout, stderr = ssh.exec_command(self.__cmd)
        OUT = stdout.read()
        ssh.close()
        return OUT

    def Reload(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.__lvshostip, self.__port, self.__username, self.__password)
        stdin, stdout, stderr = ssh.exec_command(self.__reload)
        OUT = stdout.read()
        ssh.close()
        return OUT


if __name__ == '__main__':
    exit(1)



