#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import os,sys
import subprocess
import time



Time_join = time.strftime("%Y%m%d", time.localtime())
usercode = '--username yunweimerge --password yunweimerge61'
dir_cd = os.getcwd()

class marge_svn(object):
    def __init__(self,co_Branch_inputs):
        self.__co_Branch_input = co_Branch_inputs.strip()

        self.branches_list = self.__co_Branch_input.strip('/').split('/')
        self.old_name = self.branches_list[-1]
        self.branches_data = self.branches_list[-1].split('_')[0][:6]
        self.trunk_ad = False
        self.log = []
        if 'branches' in self.branches_list:
            self.project_name = \
                self.__co_Branch_input.strip('/').split('/')[:self.__co_Branch_input.strip('/').split('/').index('branches')][-1]
            self.project_dir = '/'.join(
                self.__co_Branch_input.strip('/').split('/')[:self.__co_Branch_input.strip('/').split('/').index('branches')])
        elif 'pre-trunk' in self.branches_list:
            self.project_name = \
                self.__co_Branch_input.strip('/').split('/')[:self.__co_Branch_input.strip('/').split('/').index('pre-trunk')][-1]
            self.project_dir = '/'.join(
                self.__co_Branch_input.strip('/').split('/')[:self.__co_Branch_input.strip('/').split('/').index('pre-trunk')])
            self.pre_name = 'pre-trunk'
            self.trunk_ad = True
        elif 'pretrunk' in self.branches_list:
            self.project_name = \
                self.__co_Branch_input.strip('/').split('/')[:self.__co_Branch_input.strip('/').split('/').index('pretrunk')][-1]
            self.project_dir = '/'.join(
                self.__co_Branch_input.strip('/').split('/')[:self.__co_Branch_input.strip('/').split('/').index('pretrunk')])
            self.pre_name = 'pretrunk'
            self.trunk_ad = True


    def sub_cmd(self,cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()
        return p

    def publisthed(self):
        svn_back_cmd = 'svn list http://10.10.1.21/svn/hnapay/development/published %s'%usercode
        p = self.sub_cmd(svn_back_cmd)
        for line in p:
            if Time_join in line.strip('\n'):
                return True
        else:
            svn_back_cmd = "svn mkdir http://10.10.1.21/svn/hnapay/development/published/%s %s -m 'mkdir'"%(Time_join,usercode)
            self.sub_cmd(svn_back_cmd)
            return True

    def Archive_check(self,project_dir,date_svn):
        svn_list_cmd = 'svn list %s %s'%(project_dir,usercode)
        p = self.sub_cmd(svn_list_cmd)
        for i in p:
            if 'old' in i.strip('\n'):
                break
        else:
            svn_mkdir_old = "svn mkdir %s %s -m 'mkdirold' "%(project_dir+'/'+'old',usercode)
            self.log.append( '执行创建old目录命令：' + svn_mkdir_old +  '\n')
            p = self.sub_cmd(svn_mkdir_old)

        svn_list_datacmd = 'svn list %s %s' % (project_dir + '/' + 'old/', usercode)
        p = self.sub_cmd(svn_list_datacmd)
        for line in p:
            if date_svn in line.strip('\n'):
                break
        else:
            svn_mkdir_cmd = "svn mkdir %s %s -m 'mkdir' "%(project_dir + '/' + 'old/' +date_svn,usercode)
            self.log.append( '执行创建归档目录命令：' + svn_mkdir_cmd + '\n')
            p = self.sub_cmd(svn_mkdir_cmd)
        return True

    def backup(self,old_dir,input_dir,date_join,name):
        svn_backup_cmd =  "svn move %s %s %s -m 'backup' " %(input_dir,old_dir + '/' + 'old/' + date_join + '/' + name,usercode)
        self.log.append('执行分支/准主干归档命令：' + svn_backup_cmd + '\n')
        self.sub_cmd(svn_backup_cmd)


    def pretrunk_check(self,project_dir,project_name):
        svn_project_cmd = 'svn list %s %s' %(project_dir,usercode)
        p = self.sub_cmd(svn_project_cmd)
        pretrunk_name = ''
        for line in p:
            if 'pre' in line.strip('\n'):
                pretrunk_name = line.strip('\n')
                break
        svn_pre_cmd = "svn list %s %s "%(project_dir+'/'+ pretrunk_name ,usercode)
        p = self.sub_cmd(svn_pre_cmd)
        for line in p:
            if 'pre' in line.strip('\n'):
                self.log.append('准主干%s已经存在，合并暂停，请验证！！'%line.strip('\n') + '\n')
                return False

        else:
            #创建准主干
            #生成主干
            trunk = project_dir+'/trunk'
            pretrunk = project_dir+'/'+pretrunk_name+Time_join+'_'+project_name+'_pretrunk'
            mkdir_pretrunk_cmd = "svn copy %s %s %s -m 'create' "%(trunk,pretrunk,usercode)
            self.log.append('执行创建准主干命令：' + mkdir_pretrunk_cmd  + '\n')
            p = self.sub_cmd(mkdir_pretrunk_cmd)
            for line in p:
                self.log.append(line + '\n')
            return pretrunk

    def marge(self,co_Branch,ci_Branch):
        # 生成取出准主干的命令
        co_cmd = 'svn co %s --username yunweimerge --password yunweimerge61' % co_Branch
        self.log.append( '执行取出准主干命令：' + co_cmd +  '\n')
        p = self.sub_cmd(co_cmd)
        for line in p:
            self.log.append(line+'\n')

        os.chdir(co_Branch.split('/')[-1])

        # 生成获取版本号的命令
        cmd_Branch = 'svn log --stop-on-copy %s --username yunweimerge --password yunweimerge61' % ci_Branch

        self.log.append(  '执行取版本号命令：' + cmd_Branch + '\n')
        p = self.sub_cmd(cmd_Branch)
        try:
            old_num = p[-4].split('|')[0].strip(' ')
            new_num = p[1].split('|')[0].strip(' ')
            for line in p:
                self.log.append(line + '\n')
        except IndexError, e:
            self.log.append(  '你确定你填写的是正确的SVN地址？？' +  '\n')

        # 测试合并
        try_cmd = 'svn merge --dry-run -%s:%s %s --username yunweimerge --password yunweimerge61' % (
        old_num, new_num, ci_Branch)
        self.log.append( '执行测试合并命令：' + try_cmd +'\n')
        p = self.sub_cmd(try_cmd)
        for line in p:
            self.log.append(line + '\n')
        if old_num == new_num:
            self.log.append('[警告]！分支版本号无变化，请检查分支是否修改？（准主干已建立，但未合并。）' + '\n')
            return False

        # 生成合并的命令
        cmd_pretrunk = 'svn merge -%s:%s %s --accept postpone --username yunweimerge --password yunweimerge61' % (
        old_num, new_num, ci_Branch)
        self.log.append('执行合并命令：' + cmd_pretrunk  + '\n')
        p = self.sub_cmd(cmd_pretrunk)
        for line in p:
            self.log.append(line + '\n')
        #
        # #解决冲突命令
        cmd_resolved = 'svn resolved --username yunweimerge --password yunweimerge61 -R .'
        self.log.append('执行解决冲突命令：' + cmd_resolved + '\n')
        p = self.sub_cmd(cmd_resolved)
        for line in p:
            self.log.append(line + '\n')

        # 提交命令
        messge = 'merge -%s:%s %s' % (old_num, new_num, ci_Branch)
        ci_cmd = "svn ci -m '%s' --username yunweimerge --password yunweimerge61" % messge
        self.log.append( '执行提交命令：' + ci_cmd + '\n')
        p = self.sub_cmd(ci_cmd)
        for line in p:
            self.log.append(line + '\n')
        os.system('rm -rf %s' % (str(dir_cd) + '/' + str(co_Branch.split('/')[-1])))
        self.log.append( '合并完成！' + '\n')
        return True

    def run(self):
        if self.trunk_ad:
            self.log.append( '执行准主干合并到主干操作！' + '\n')
            self.publisthed()
            svn_back_cmd = "svn copy %s %s %s -m 'backup' "%(self.project_dir + '/trunk','http://10.10.1.21/svn/hnapay/development/published/'+Time_join+'/'+self.project_name,usercode)
            self.log.append('执行备份主干命令：'+svn_back_cmd + '\n')
            p = self.sub_cmd(svn_back_cmd)
            for line in p:
               self.log.append(line+'\n')
            #生成主干地址
            svn_trunk_dir = self.project_dir+'/trunk'
            return_value = self.marge(svn_trunk_dir,self.__co_Branch_input)
            if return_value !=False:
                self.Archive_check(self.project_dir+'/'+self.pre_name,self.branches_data)
                self.backup(self.project_dir+'/'+self.pre_name,self.__co_Branch_input,self.branches_data,self.old_name)
                return self.log
            else:
                return self.log
        else:
            self.log.append( '执行分支合并到准主干操作！' +'\n')
            pretrunk_name = self.pretrunk_check(self.project_dir,self.project_name)
            if pretrunk_name != False:
                return_value = self.marge(pretrunk_name, self.__co_Branch_input)
                if return_value != False:
                    self.Archive_check(self.project_dir + '/' + 'branches',self.branches_data)
                    self.backup(self.project_dir + '/' + 'branches', self.__co_Branch_input, self.branches_data,self.old_name)
                    return self.log
                else:
                    return self.log
            else:
                return self.log