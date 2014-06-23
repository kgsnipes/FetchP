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


class url_monitor_thread (threading.Thread):
    def __init__(self, conf,stat):
        threading.Thread.__init__(self)
        self.conf = conf
        self.stat = stat
        
    def run(self):
        while True:
            # Get lock to synchronize threads
            THD_LOCK.acquire()
            self.process_url()
            # Free lock to release next thread
            THD_LOCK.release()
            time.sleep(self.stat.interval)

    def process_url(self):
        print(self.conf.uri)
       
            
        
       

