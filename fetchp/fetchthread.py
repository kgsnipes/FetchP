'''
Created on 24-Jun-2014

@author: kaushik.ganguly
'''

from app.main import *

from jinja2 import Template
import datetime
import requests
import socket
from urllib.parse import urlparse

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
#            print(STATS[self.index])
            time.sleep(STATS[self.index].interval)
            

    def process_url(self):
        try:
            if self.is_connected():
                self.retval=self.getTheProcessedRequest(CONFIGS[self.index].uri,0)
                self.doTimeRelatedCalculation()
            else:
                self.updateParticularStat(0,1,"INTERNET CONNECTIVITY IS DOWN",0.0)
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
            STATS[self.index].lastfailurepoint= datetime.datetime.now()
            STATS[self.index].lasterrormessage=errormsg
            STATS[self.index].errorlogs.append(failuremessage(datetime.datetime.now(),errormsg))
            STATS[self.index].lasterrornotified=False
        
        if STATS[self.index].latency>0 :
            STATS[self.index].averagelatency=round(STATS[self.index].latency/STATS[self.index].successpollcount,2)
        if STATS[self.index].successpollcount>0 :
            STATS[self.index].successpercentage=round((float(STATS[self.index].successpollcount)/float(STATS[self.index].pollcount))*100,2)
        if STATS[self.index].failurepollcount>0 :
            STATS[self.index].errorpercentage=round((float(STATS[self.index].failurepollcount)/float(STATS[self.index].pollcount))*100,2)
#        print(STATS[self.index])
        self.updateSiteStatsToOutputFile()
        if  STATS[self.index].lasterrornotified!=True:
            print("NEED TO SEND MAIL")
        else:
            print("EMAIL ALREADY SENT")
        if len(STATS[self.index].errorlogs)>50:
            STATS[self.index].errorlogs=STATS[self.index].errorlogs[40:]
        
    def readFileToString(self,filename):
        file=open(self.getCurrentDirectoryPath()+filename,"r")
        retval=file.read(self.getFileSize(self.getCurrentDirectoryPath()+filename))
        file.close()
        return retval
    
    def getCurrentDirectoryPath(self):
        filepath=os.path.dirname(os.path.realpath(__file__))
        if os.name.find("nt",0,len(os.name))!=-1:
            index=filepath.rfind("\\", 0 ,len(filepath))
            return filepath[0:index+1]
    
        
    def getFileSize(self,filename):
        st = os.stat(filename)
        return st.st_size
    
    
    def updateSiteStatsToOutputFile(self):
        file=open(self.getCurrentDirectoryPath()+"output.html","w")
        file.write(self.renderSiteStatsOnTemplate("page_templates\\site_stats.txt"))
        file.close()
        
    def renderSiteStatsOnTemplate(self,filename):
        mytemplate = Template(self.readFileToString(filename))
        return mytemplate.render({"stats":STATS})

    def is_connected(self):
        try:
            o = urlparse(CONFIGS[self.index].uri)
            host = socket.gethostbyname(o.netloc)
            s = socket.create_connection((host, 80),CONFIGS[self.index].threshold)
            s.close()
            return True
        except:
            pass
        return False

