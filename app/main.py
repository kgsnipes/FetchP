'''
Created on 23-Jun-2014

@author: kaushik.ganguly
'''


import sys
import os
import threading
import time

CONFIGS=[]
STATS=[]
NOTIFIER=[]
REPORTING=[]
THD_LOCK = threading.Lock()


from fetchp.fetchutil import *
from fetchp.fetchclasses import *
from fetchp.fetchthread import *

def start_site_monitoring_app(arg):
    CONFIGS=read_url_config(arg[0])
    STATS=createStats(arg[0])
    NOTIFIER=read_notifier_config(arg[0])
    REPORTING=read_reporting_config(arg[0])
#    MAILREPORTING=Gmail(REPORTING[0].userName,REPORTING[0].password,REPORTING[0].smtpPort,REPORTING[0].smtpHost,REPORTING[0].recipient,REPORTING[0].cc,REPORTING[0].bcc)
#    MAILNOTIFIER=Gmail(NOTIFIER[0].userName,NOTIFIER[0].password,NOTIFIER[0].smtpPort,NOTIFIER[0].smtpHost,NOTIFIER[0].recipient,NOTIFIER[0].cc,NOTIFIER[0].bcc)
    thds=createURLMonitorThreads()
    for thd in thds:
        thd.join()
    
    
def main():
    sys.argv = input('config file path: ').split()
    start_site_monitoring_app(sys.argv)
   
    
    
def main_dev():
    start_site_monitoring_app(["D:\\Users\\kaushik.ganguly\\Documents\\GitHub\\FetchP\\SiteMonitorConfig.xml"])
    print("FetchP stopped")
    
if __name__ == '__main__':
    main_dev()