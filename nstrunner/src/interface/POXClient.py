# -*- coding: utf-8 -*-
""" NST internal

Interface for the POX, 
    1.Start/Stop the POX JOB, Robot;
    2.Get the virtual phone number from robot; 
    3.Create/Answer/Release calls from robot;
     
"""

import time
import socket
import sys
import re

import logging

from java.util import HashMap



from com.nokia.nst.poxbackend import NSTPOXBackend, PoxConnectionException, PoxRobotException,InvalidPoxOperationException
from redstone.xmlrpc import XmlRpcClient

class POXClient():
    
    def __init__(self, phoneName='Reference', sim1NO='+8613703137613', deviceSN='emulator-5554'):
        '''
        Init the POXBackend, 
        '''
        self._phoneName = phoneName
        self._sim1NO = sim1NO
        
        config = HashMap()
        
        config.put("deviceSN", deviceSN)
        config.put("deviceSIM1Number", sim1NO)
        
        nstPoxBackend = NSTPOXBackend(config)
        
        self._nstPoxBackend = nstPoxBackend
        
         #Get the logger
        self._logger = logging.getLogger('')
        
    def startJob(self):
        '''
        start or check the pox job
        '''
        if self._nstPoxBackend:
            self._logger.debug("Begin to start the POX backend.")
            try:
                self._nstPoxBackend.startOrCheckPoxJob()
            except PoxConnectionException, ex:
                debug.err(str(ex.Message))
                self._logger.error(str(ex.getMessage()))

            self._logger.debug("Finish starting the POX backend.")
    
    def getRobotPhone(self, phoneName='Reference'):
        '''
        Get the robot phone information according to phoneName;
        '''
        #self._phoneName = phoneName
        
        if self._nstPoxBackend:
            
            self._logger.debug("Start to get robot phone for the :"+phoneName)
            
            try:
                phoneNO = self._nstPoxBackend.getRobotPhone(phoneName).PhoneNumber

                if(phoneName=='Reference'):
                    self._ReferenceNO = phoneNO
            
                self._logger.debug("Finish getting robot phone for the :" + phoneName + ", with the robot phone Number:" + phoneNO)    
                
                return phoneNO
            
            except PoxConnectionException, ex:

                raise BackendConnectionException(str(ex.getMessage()))
            except PoxRobotException, ex:

                raise POXRobotException(str(ex.getMessage()))
        else:
            raise RuntimeError('Unable to create call via POX. Backend not available!')
        
    
    def createCall(self, phoneNumber, phoneName='Reference'):      
        '''
        Create a call on POX robot
        '''
        
        #self._phoneName = phoneName
        
        if self._nstPoxBackend:
            self._logger.debug("Start to create call the from:"+phoneName +" to Number:"+phoneNumber)
            
            try:
                self._nstPoxBackend.createCall(phoneNumber, phoneName)

                self._logger.debug("Finish creating call the from:"+phoneName +" to Number:"+phoneNumber)
            except PoxConnectionException, ex:

                raise RuntimeError(str(ex.getMessage()))
            except PoxRobotException, ex:

                raise RuntimeError(str(ex.getMessage()))
        else:
            raise RuntimeError('Unable to create call via POX. Backend not available!')
    
    def answerCall(self,phoneName='Reference'):
        '''
        Answer a call on POX robot
        '''
        if self._nstPoxBackend and phoneName:
            
            self._logger.debug("Start answer call the from:"+phoneName)
            
            try:
                self._nstPoxBackend.answerCall(self._phoneName)

            except PoxConnectionException, ex:
                raise RuntimeError(str(ex.getMessage()))
            except PoxRobotException, ex:
                raise RuntimeError(str(ex.getMessage()))
        else:
            raise RuntimeError('Unable to answer call via POX. Backend not available!')
    
    def releaseCall(self,phoneName='Reference'): 
        '''
        Release the call
        If no POX job has been started, this method call can be ignored.
        '''
    
        if self._nstPoxBackend and phoneName:
            
            if self._nstPoxBackend and self._nstPoxBackend.GetJobID() < 0:
                return

            self._logger.debug("Start to release the phone call from:"+phoneName)
            
            # Release a call on POX robot
            try:
                self._nstPoxBackend.releaseCall(phoneName)
                
            except PoxConnectionException, ex:
                raise BackendConnectionException(str(ex.Message))
            except PoxRobotException, ex:
                raise POXRobotException(str(ex.Message))
        else:
            raise RuntimeError('Unable to release call via POX. Backend not available!')
    
    def close(self):
        '''
        close the pox job
        '''
        if self._nstPoxBackend:
            self._logger.debug("Start to close the POX backend with Job ID:"+str(self._nstPoxBackend.GetJobID()))
            try:
                self._nstPoxBackend.close()
            except PoxConnectionException, ex:
                debug.err(str(ex.Message))
                self._logger.error(str(ex.getMessage()))

            self._logger.debug("Finish closing the POX backend.")
        