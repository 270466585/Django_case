#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'weihaoxuan'

import threading
from releases.plugins import svn_marge

class Svninfo(object):
    def __init__(self):
        self.__log = []
        self.__mutex = threading.Lock()
    def marge_svn(self,svnurl):
        svn_logs = svn_marge.marge_svn(svnurl).run()
        self.__mutex.acquire()
        for i in svn_logs:
            self.__log.append(i)
        self.__mutex.release()
        return True

    def start(self,svnurl):
        threads = []
        for item in svnurl.split(','):
            threads.append(threading.Thread(self.marge_svn(item)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.__log