'''
Created on 23-Jun-2014

@author: kaushik.ganguly
'''
import sys
import os
import threading
from fetchp.fetchutil import *


CONFIGS=[]
STATS=[]
NOTIFIER=[]
REPORTING=[]


THD_LOCK = threading.Lock()


def start_site_monitoring_app(arg):
    read_url_config(arg[0])
    createStats(arg[0])
    read_notifier_config(arg[0])
    read_reporting_config(arg[0])
#    thds=createURLMonitorThreads()
#    for thd in thds:
#        thd.join()
    renderSiteStatsOnTemplate("page_templates\\site_stats.txt")
    
def main():
    sys.argv = input('config file path: ').split()
    start_site_monitoring_app(sys.argv)
   
    
    
def main_dev():
    start_site_monitoring_app(["D:\\Users\\kaushik.ganguly\\Documents\\GitHub\\FetchP\\SiteMonitorConfig.xml"])
    print("FetchP stopped")
    
if __name__ == '__main__':
    main_dev()