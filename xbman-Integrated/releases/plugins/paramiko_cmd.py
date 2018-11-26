#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import paramiko



class modify_paramiko(object):
    def __init__(self,ip,username,password):
        self.__lvshostip = ip
        self.__port = 22
        self.__username = username
        self.__password = password


    def Landed(self,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.__lvshostip,self.__port,self.__username,self.__password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        OUT = stdout.read()
        ssh.close()
        return OUT



if __name__ == '__main__':
    exit(1)