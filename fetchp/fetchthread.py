'''
Created on 24-Jun-2014

@author: kaushik.ganguly
'''

import threading
import time

from app.main import CONFIGS
from app.main import STATS
from app.main import NOTIFIER
from app.main import REPORTING
from app.main import THD_LOCK

import requests

from fetchp.fetchutil import *
import sys




class url_monitor_thread (threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index=index
        self.retval=None
    def run(self):
        while True:
            # Get lock to synchronize threads
            THD_LOCK.acquire()
            self.process_url()
        
            # Free lock to release next thread
            THD_LOCK.release()
            print(STATS[self.index])
            time.sleep(STATS[self.index].interval)
            

    def process_url(self):
        try:
            self.retval=self.getTheProcessedRequest(CONFIGS[self.index].uri,0)
            self.doTimeRelatedCalculation()
        except:
            e = sys.exc_info()[0]
            self.updateParticularStat(0,1,e,self.retval[1])
        
    def doTimeRelatedCalculation(self):
        if self.retval[0].status_code>=200 and self.retval[0].status_code<=300:
            self.updateParticularStat(1,0,None,self.retval[1])
        else:
            self.updateParticularStat(0,1,str(self.retval[0].status_code),self.retval[1])

        
    def getTheProcessedRequest(self,url,timetaken):
        start_time=time.time()
        r = requests.get(url)
        stop_time=time.time()
        process_time=stop_time-start_time
        process_time=process_time+timetaken
        retval=[r,process_time]
        if r.status_code!=302:
            return retval
        elif r.status_code==302:
            return self.getTheProcessedRequest(r.headers['Location'],process_time)
       

    def updateParticularStat(self,success,error,errormsg,latency):
        if success==1:
            STATS[self.index].pollcount= STATS[self.index].pollcount+1
            STATS[self.index].successpollcount=STATS[self.index].successpollcount+1
            STATS[self.index].latency=STATS[self.index].latency+latency
        elif error==1:
            STATS[self.index].pollcount=STATS[self.index].pollcount+1
            STATS[self.index].failurepollcount=STATS[self.index].failurepollcount+1
            STATS[self.index].lastfailurepoint=time.time()
            STATS[self.index].lasterrormessage=errormsg
            STATS[self.index].errorlogs.append(errormsg)
        
        if STATS[self.index].latency>0 :
            STATS[self.index].averagelatency=STATS[self.index].latency/STATS[self.index].successpollcount
        if STATS[self.index].successpollcount>0 :
            STATS[self.index].successpercentage=(float(STATS[self.index].successpollcount)/float(STATS[self.index].pollcount))*100
        if STATS[self.index].failurepollcount>0 :
            STATS[self.index].errorpercentage=(float(STATS[self.index].failurepollcount)/float(STATS[self.index].pollcount))*100
        print(STATS[self.index])
    

   

