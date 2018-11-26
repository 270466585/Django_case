#!/usr/bin/python3
#coding:utf8
import requests
import re
import time
from News import models

from threading import Thread
class main(object):
    def __init__(self):
        self.url='http://daily.zhihu.com/'
        self.l=list()
        self.n=0
        self.req=requests.Session()
        self.header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'daily.zhihu.com',
            'Referer':'https://www.baidu.com/link?url=Eh6CKs72Buyf0LEjPd1795QSL8ZK74kwItBvzaybausT6proAZIr3UkkmMPSDfk7&wd=&eqid=d1bd8fd9004118c90000000258bd8149',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36'
        }
    def getpage(self):
        html=self.req.get(url=self.url,headers=self.header)
        pattern=re.compile(u'<span class="title">(.*?)</span>.*?'+
        u'<a href="(.*?)".*?'+
        u'<img src="(.*?)".*?'
        ,re.S)
        T=list()
        self.l=re.findall(pattern,html.text)
        author = models.BBS_user.objects.get(user__username='cb')

        for i in self.l:
            if(self.n<29):
                self.getimg(i[2],self.n)
            # t=Thread(target=self.getimg,args=(i[2],self.n))
                picture_name=str(self.n)+'.jpg'
                #self.getimg(i[2],self.n)
                title = str(i[0])
                content = "http://daily.zhihu.com"+str(i[1])
                summary="本文来自知乎。"
                models.BBS.objects.create(
                title=title,
                bbs_category_id=int(1),
                picture=picture_name,
                content=content,
                author=author,
                summary=summary,
            )

            # T.append(t)
            # t.start()
            #print(i)
            self.n+=1
            #time.sleep(1)
        # for tt in T:
        #     tt.join()

    # def bbs_sub(request):
    #     author = models.BBS_user.objects.get(user__username=request.user)
    #     picture_name = request.POST.get('summary_pictrue')
    #     # picture=request.FILES['summary_pictrue']
    #     # print(picture)
    #     # print(picture)
    #     # print(picture)
    #     title = request.POST.get('title')
    #     content = request.POST.get('content')
    #     summary = request.POST.get('summary')
    #     models.BBS.objects.create(
    #         title=title,
    #         picture=picture_name,
    #         summary=summary,
    #         content=content,
    #         author=author,
    #
    #     )
    def getimg(self,src,n):
        try:
            h=self.req.get(url=src)
            s=open('./static/img/zh/'+str(n)+'.jpg','wb')
            s.write(h.content)
            s.close()
        except requests.exceptions.MissingSchema:
            print('这个url无效',n)

if __name__=='__main__':
    p=main()
    p.getpage()
