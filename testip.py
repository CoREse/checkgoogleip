#!/usr/bin/python2
import shlex
from subprocess import Popen, PIPE
import threading

f302=open('ip_302.txt', 'w')
f200=open('ip_200.txt', 'w')
f302.write('')
f200.write('')
f302.close()
f200.close()
f302=open('ip_302.txt', 'a')
f200=open('ip_200.txt', 'a')

is200First=True
is302First=True

ips=[]

imutex=threading.RLock()
fmutex=threading.RLock()

with open('ip_tmpok.txt') as f:
    for line in f:
        ips.append(line.split()[0])

index=0;

class reqUrl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop=False

    def run(self):
        global index
        global imutex
        global fmutex
        global is200First
        global is302First
        while not self.thread_stop:
            imutex.acquire()
            if index>=len(ips):
                imutex.release()
                break
            ip=ips[index]
            index=index+1
            imutex.release()
            print "checking "+ip
            cmd= 'curl https://www.google.com --resolve www.google.com:443:'+ip+' -s -o /dev/null -w %{http_code}'
            args=shlex.split(cmd)
            output,error=Popen(args,stdout=PIPE,stderr=PIPE).communicate()
    
            fmutex.acquire()
            if output=='200':
                if is200First:
                    f200.write(ip)
                    is200First=False
                else:
                    f200.write("\n"+ip)
            if output=='302':
                if is302First:
                    f302.write(ip)
                    is302First=False
                else:
                    f302.write("\n"+ip)
            fmutex.release()
    def stop(self):
        self.thread_stop=True
    
def startThs(n):
    threads=[]
    for i in range(n):
        threads.append(reqUrl())
    i=0
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return
    
startThs(100)

f302.close()
f200.close()
