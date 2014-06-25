'''
Created on 23-Jun-2014

@author: kaushik.ganguly
'''

from app.main import *
import xml.dom.minidom



def isNotNullOrEmpty(value):
    if  value == None or (isinstance(value, str) and value.isspace()):
        return False
    else:
        return True
     
       
def read_url_tag_config(config):
    if (config.hasAttribute("url") and isNotNullOrEmpty(config.getAttribute("url"))) and (config.hasAttribute("interval") and isNotNullOrEmpty(config.getAttribute("interval"))) and (config.hasAttribute("latencyThreshold") and isNotNullOrEmpty(config.getAttribute("latencyThreshold"))):
        c=fetchurlconfig(config.getAttribute("url"),int(config.getAttribute("interval")),int(config.getAttribute("latencyThreshold")))
        CONFIGS.append(c)
#        print(c)
    
def read_url_config(filename):
        DOMTree = xml.dom.minidom.parse(filename)
        collection = DOMTree.documentElement
        urlconfig = collection.getElementsByTagName("URLMonitor")
        for config in urlconfig:
            read_url_tag_config(config)
        return CONFIGS

def read_notifier_config(filename):
        DOMTree = xml.dom.minidom.parse(filename)
        collection = DOMTree.documentElement
        urlconfig = collection.getElementsByTagName("notifier")
        for config in urlconfig:
            read_notifier_config_tag(config)
        return NOTIFIER

def read_notifier_config_tag(config):
    if (config.hasAttribute("type") and isNotNullOrEmpty(config.getAttribute("type"))) \
    and (config.hasAttribute("enabled") and isNotNullOrEmpty(config.getAttribute("enabled"))) \
    and (config.hasAttribute("smtp") and isNotNullOrEmpty(config.getAttribute("smtp")))\
    and (config.hasAttribute("smtpPort") and isNotNullOrEmpty(config.getAttribute("smtpPort"))) \
    and (config.hasAttribute("tls") and isNotNullOrEmpty(config.getAttribute("tls"))) \
    and (config.hasAttribute("recipients") and isNotNullOrEmpty(config.getAttribute("recipients")))\
    and (config.hasAttribute("cc") and isNotNullOrEmpty(config.getAttribute("cc"))) \
    and (config.hasAttribute("bcc") and isNotNullOrEmpty(config.getAttribute("bcc"))) \
    and (config.hasAttribute("userName") and isNotNullOrEmpty(config.getAttribute("userName"))) \
    and (config.hasAttribute("password") and isNotNullOrEmpty(config.getAttribute("password"))):
        c=fetchnotifier(config.getAttribute("type"),bool(config.getAttribute("enabled")),config.getAttribute("smtp"),config.getAttribute("smtpPort"),bool(config.getAttribute("tls")),config.getAttribute("recipients").split(","),config.getAttribute("cc").split(","),config.getAttribute("bcc").split(","),config.getAttribute("userName"),config.getAttribute("password"))
        NOTIFIER.append(c) 
#        print(c)


def read_reporting_config(filename):
        DOMTree = xml.dom.minidom.parse(filename)
        collection = DOMTree.documentElement
        urlconfig = collection.getElementsByTagName("URLMonitor")
        for config in urlconfig:
            read_reporting_config_tag(config)
        return REPORTING
            
            
def read_reporting_config_tag(config):
    if (config.hasAttribute("type") and isNotNullOrEmpty(config.getAttribute("type"))) \
    and (config.hasAttribute("interval") and isNotNullOrEmpty(config.getAttribute("interval"))) \
    and (config.hasAttribute("enabled") and isNotNullOrEmpty(config.getAttribute("enabled"))) \
    and (config.hasAttribute("smtp") and isNotNullOrEmpty(config.getAttribute("smtp")))\
    and (config.hasAttribute("smtpPort") and isNotNullOrEmpty(config.getAttribute("smtpPort"))) \
    and (config.hasAttribute("tls") and isNotNullOrEmpty(config.getAttribute("tls"))) \
    and (config.hasAttribute("recipients") and isNotNullOrEmpty(config.getAttribute("recipients")))\
    and (config.hasAttribute("cc") and isNotNullOrEmpty(config.getAttribute("cc"))) \
    and (config.hasAttribute("bcc") and isNotNullOrEmpty(config.getAttribute("bcc"))) \
    and (config.hasAttribute("userName") and isNotNullOrEmpty(config.getAttribute("userName"))) \
    and (config.hasAttribute("password") and isNotNullOrEmpty(config.getAttribute("password"))):
        c=fetchreporting(config.getAttribute("type"),int(config.getAttribute("interval")),bool(config.getAttribute("enabled")),config.getAttribute("smtp"),int(config.getAttribute("smtpPort")),bool(config.getAttribute("tls")),config.getAttribute("recipients").split(","),config.getAttribute("cc").split(","),config.getAttribute("bcc").split(","),config.getAttribute("userName"),config.getAttribute("password"))
        REPORTING.append(c)    
#        print(c)           
    
    
   
def createStatsFromURLConfig(config):
    if (config.hasAttribute("url") and isNotNullOrEmpty(config.getAttribute("url"))) and (config.hasAttribute("interval") and isNotNullOrEmpty(config.getAttribute("interval"))) and (config.hasAttribute("latencyThreshold") and isNotNullOrEmpty(config.getAttribute("latencyThreshold"))):
        c=fetchurlstat(config.getAttribute("url"),int(config.getAttribute("interval")),int(config.getAttribute("latencyThreshold")))
        STATS.append(c)
        #print(c)
    
def createStats(filename):
        DOMTree = xml.dom.minidom.parse(filename)
        collection = DOMTree.documentElement
        urlconfig = collection.getElementsByTagName("URLMonitor")
        for config in urlconfig:
            createStatsFromURLConfig(config)
        return STATS

def updateStat(url,success,error,errormsg,latency):
    for stat in STATS:
        if stat.uri==url:
            if success==1:
                stat.pollcount=+1
                stat.successpollcount=+1
                stat.latency=+latency
            else:
                if error==1:
                    stat.pollcount=+1
                    stat.failurepollcount=+1
                    stat.lastfailurepoint=time.time()
                    stat.lasterrormessage=errormsg
                    stat.errorlogs.append(errormsg)
            
            if stat.latency>0 :
                stat.averagelatency=stat.latency/stat.successpollcount
            if stat.successpollcount>0 :
                stat.successpercentage=(float(stat.successpollcount)/float(stat.pollcount))*100
            if stat.failurepollcount>0 :
                stat.errorpercentage=(float(stat.failurepollcount)/float(stat.pollcount))*100
            break
        

        
        
        
def createURLMonitorThreads():
    thds=[]
    for i in range(0,len(CONFIGS)):
        #print(i,STATS[i])
        thd=url_monitor_thread(i)
        thd.start()
        thds.append(thd)
    return thds





     
# def renderSiteStatOnTemplate(stat,filename):
#     mytemplate = Template(readFileToString(filename))
#     return mytemplate.render({"stat":stat})
#     

    
# this is from util file                


#renderSiteStatsOnTemplate("page_templates\\site_stats.txt")
#    renderSiteStatsOnTemplate("page_templates\\email_site_stats.txt")
#    renderSiteStatOnTemplate(STATS[0],"page_templates\\error_email_notification.txt")
    