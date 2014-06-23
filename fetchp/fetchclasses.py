'''
Created on 23-Jun-2014

@author: kaushik.ganguly
'''


class fetchurlconfig:
# the default interval is 60 seconds and default threshold is 30 seconds 
    def __init__(self,uri="",interval=60,threshold=30):
        self.uri=uri
        self.threshold=threshold
        self.interval=interval
        
    def __str__(self):
        return "URL CONFIG \n URI="+self.uri+"\nINTERVAL"+str(self.interval)+"\nTHRESHOLD"+str(self.threshold)
        
        
class fetchnotifier:

    def __init__(self,ty,enabled,smtpHost,smtpPort,tlsEnabled,recipient,cc,bcc,userName,password):
        self.ty=ty
        self.enabled=enabled
        self.smtpHost=smtpHost
        self.smtpPort=smtpPort
        self.tlsEnabled=tlsEnabled
        self.recipient=recipient
        self.cc=cc
        self.bcc=bcc
        self.userName=userName
        self.password=password
    
    def __str__(self):
        return "NOTIFIER \nTYPE="+self.ty+"\nENABLED="+str(self.enabled)\
            +"\nSMTP HOST="+self.smtpHost+"\nSMTP PORT="+self.smtpPort\
            +"\nTLS="+str(self.tlsEnabled)+"\nRECIPIENT="+str(self.recipient)\
            +"\nCC="+str(self.cc)+"\nBCC="+str(self.bcc)\
            +"\nUSERNAME="+self.userName+"\nPASSWORD="+self.password
    
        


class fetchreporting:

    def __init__(self,ty,interval,enabled,smtpHost,smtpPort,tlsEnabled,recipient,cc,bcc,userName,password):
        self.ty=ty
        self.interval=interval
        self.enabled=enabled
        self.smtpHost=smtpHost
        self.smtpPort=smtpPort
        self.tlsEnabled=tlsEnabled
        self.recipient=recipient
        self.cc=cc
        self.bcc=bcc
        self.userName=userName
        self.password=password
        
    def __str__(self):
        return "NOTIFIER \nTYPE="+self.ty+"\nINTERVAL="+self.interval+"\nENABLED="+str(self.enabled)\
            +"\nSMTP HOST="+self.smtpHost+"\nSMTP PORT="+self.smtpPort\
            +"\nTLS="+str(self.tlsEnabled)+"\nRECIPIENT="+str(self.recipient)\
            +"\nCC="+str(self.cc)+"\nBCC="+str(self.bcc)\
            +"\nUSERNAME="+self.userName+"\nPASSWORD="+self.password
        
class fetchurlstat:
    def __init__(self,uri,interval,threshold):
        self.uri=uri
        self.interval=interval
        self.threshold=threshold
        self.pollcount=0
        self.successpollcount=0
        self.failurepollcount=0
        self.lastfailurepoint=None
        self.errorpercentage=0.0
        self.successpercentage=0.0
        self.lasterrormessage=None
        self.averagelatency=0.0
        self.latency=0.0
        self.errorlogs=[]
        self.lasterrornotified=None
        
    def __str__(self):
        return "STATS\nURL="+self.uri+"\nINTERVAL="+str(self.interval)+"\nTHRESHOLD="+str(self.threshold)\
            +"\nPOLL COUNT="+str(self.pollcount)+"\nSUCCESS POLL="+str(self.successpollcount)+"\nSUCCESS PERCENTAGE="+str(self.successpercentage)\
            +"\nERROR POLL="+str(self.failurepollcount)+"\nERROR PERCENTAGE="+str(self.errorpercentage)+"\nLAST FAILURE POINT="+str(self.lastfailurepoint)\
            +"\nAVERAGE LATENCY="+str(self.averagelatency)
            
            