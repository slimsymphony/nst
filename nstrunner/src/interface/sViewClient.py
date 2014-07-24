#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
""" NST internal

Interface for the verserver, functions include:
    1.Start/Stop the viewserver
    2.Get the view status of the view
     

"""
import time
import socket
import sys
import re

VIEW_SERVER_HOST = 'localhost'

class sViewClient():
    '''
    used as a client for the viewserver
    '''
    def __init__(self, localport=4939):
        self._localport = localport
        
    def getFocus(self):
        '''
        Get the focused items from viewserver
        '''
        
        s = self.__getSockeConnection()
                
        s.send('GET_FOCUS\r\n')
        received = s.recv(1024)
        s.close()
        
        return received
    
    def waitForUpdate(self):
        '''
        Wait until the update finish
        '''

        #print >> sys.stderr, 'AUTOLIST'
        
        s = self.__getSockeConnection()
        
        try:
            
            s.send('AUTOLIST\r\n')
            
            retData = self.recv_timeout(the_socket=s, timeout=1)
            
            #print >> sys.stderr, retData
            
            #print >> sys.stderr, retData
        except:
            print >> sys.stderr, 'send or receive error when sent AUTOLIST command'
            s.close()
            
        s.close()
        
        
    def getVersion(self):

        try:
            s = self.__getSockeConnection()
            
            s.send('SERVER\r\n')            
            
            received = s.recv(1024)
            
        except:
            print >> sys.stderr, 'send or receive error when sent SERVER command'
            s.close()
            return None
        
        s.close()
        
        return received
        
    def recv_timeout(self, the_socket,timeout=2):
        #make socket non blocking
        the_socket.setblocking(0)
         
        #total data partwise in an array
        total_data=[];
        data='';
         
        #beginning time
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
             
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
             
            #recv something
            try:
                data = the_socket.recv(1024)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
                
            except:
                pass
         
        #join all parts to make final string
        return ''.join(total_data)
        
    def __getSockeConnection(self):
        '''
        Get the socket connection;
        '''
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((VIEW_SERVER_HOST,self._localport))
        except socket.error, ex:
                raise RuntimeError("ERROR: Connecting to %s:%d: %s" % (VIEW_SERVER_HOST, self._localport, ex))
        
        return s
    
if __name__ == '__main__':
    print 'running'
    
    sc = sViewClient(localport=4950)
    print sc.getVersion()
    
    sc.waitForUpdate()
