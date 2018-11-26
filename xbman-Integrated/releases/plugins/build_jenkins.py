#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import jenkins
import time


class buildjob(object):
    def __init__(self,settings):
        self.__jenkins_server_url = settings[0].UrlLocation
        self.__user_id = settings[0].username
        self.__api_token = settings[0].password
        self.__server = jenkins.Jenkins(self.__jenkins_server_url, username=self.__user_id, password=self.__api_token)

    def checkjob(self,jobnames):
        for line in jobnames:
            try:
                self.__server.get_job_info(line)
            except jenkins.NotFoundException,e:
                return '[ERROR]:jobname:%s不存在'%str(line)
        else:
            return None

    def get_jeknins(self):
        return self.__server.get_all_jobs()
    def buildjobs(self,jobname):
        OUT = ''
        for line in jobname:
            #build项目
            try:
                self.__server.build_job(line)
            except jenkins.NotFoundException,e:
                return '[ERROR]:jobname:%s不存在\n'%str(line)
            time.sleep(10)
            #print jobname,self.__server.get_job_info(jobname)['lastBuild']['number']
            while self.__server.get_build_info(line,self.__server.get_job_info(line)['lastBuild']['number'])['building']:
                time.sleep(5)
            else:
                #print self.__server.get_build_info(line,self.__server.get_job_info(line)['lastBuild']['number'])['result']
                if self.__server.get_build_info(line,self.__server.get_job_info(line)['lastBuild']['number'])['result'] == 'FAILURE':
                    aaa = self.__server.get_build_console_output(line,self.__server.get_job_info(line)['lastBuild']['number'])
                    bbb =  '[ERROR]:%s,编译失败\n'%str(line)
                    OUT += bbb + aaa.encode("utf-8")
                else:
                    OUT = OUT +'[SUCCESS]:%s,编译成功\n'%str(line)
        return OUT




if __name__ == '__main__':
    exit(1)

