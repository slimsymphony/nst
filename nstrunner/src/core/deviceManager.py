# ============================================================================
#                              Device Management module
#                           -----------------------
# ----------------------------------------------------------------------------

# ============================================================================
#   1   ABSTRACT
#
#   1.1 Module type
#
#       Manage the device connections, status, etc
#
#   1.2 Description
#
#       This module implements a common ISI message helper class. The class
#       and its subclasses (implemented elsewhere) take care of packing and
#       unpacking of ISI messages' fields. Errors in (un)packing raise an
#       ISIMessageException.
#
#   1.3 Notes
#
#       Current plan:
#           - Implement subclass of ISIMessage for each non MM'ed ISI IF
#           - Implement PMDMessage class for Message Macros (PMD wrapper)
#
#       The latest documentation for the struct module is here:
#           http://www.python.org/doc/current/lib/module-struct.html
#
#       Code indentation rule: 4 spaces for one indentation level, no tabs!
#       Recommended maximum line length is 79 characters.
#       (see more from: http://www.python.org/doc/essays/styleguide.html)
# ----------------------------------------------------------------------------

# ============================================================================
#   2   CONTENT
#
#       1   ABSTRACT
#       1.1 Module type
#       1.2 Description
#       1.3 Notes
#
#       2   CONTENT
#
#       3   MODULE CODE
#       3.1 DeviceManager class
#       3.n Self test
# ----------------------------------------------------------------------------

""" NST internal

"""

# ============================================================================
#   3   MODULE CODE
# ----------------------------------------------------------------------------

# Python library module imports
import os
import ConfigParser
import time
import logging

# ============================================================================
#   3.1     DeviceManager class
# ----------------------------------------------------------------------------
class DeviceManager:
    
    #static member
    deviceConfig = None
    nstHome = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def getDevicesConfiguration(deviceSN):
        '''
        return the dict of deviceSN section
        '''
        if DeviceManager.deviceConfig is None:
            DeviceManager.initDevicesConfiguration()
        
        #the default collection is list, so convert to dict;
        return dict(DeviceManager.deviceConfig.items(deviceSN)) 
    
    @staticmethod    
    def initDevicesConfiguration():
        '''
        Get the devices configuration for the controlling of behavior including: 
            (1)method of view dump client
            (2)basic information of device, SIM Number...
        '''
        '''
        1.Judge whether the config file exit; %NST_HOME%/config/devicesConfiguration.ini is the default file;
        2.Init the config and set the Class member;
        '''
        DeviceManager.nstHome = os.getenv("NST_HOME")        
        
        configFile = os.path.join(DeviceManager.nstHome, "config", "devicesConfiguration.ini")
        
        if not os.path.exists(configFile):
            raise RuntimeError('''ERROR: No configuration file is found, please provide it at %NST_HOME%/config/devicesConfiguration.ini !''') 
        
        config = ConfigParser.ConfigParser()
        config.readfp(open(configFile))
        
        DeviceManager.deviceConfig = config
    
    
    def lsDevices(self):
        self._deviceList = list
        self._deviceList.append("1")
        self._deviceList.append("2")

    def initDevices(self):
        self._deviceDict = dict
        
        # iterate the device name list and construct the key-value pair of device;
        for element in self._deviceList:  
            self._deviceDict[element] = self.connectDevice(self, element)
        
    
    def connectDevice(self, deviceStr, timeOut=10, connTime=5):
        #device = MonkeyDevice
        #self._logFMT = {'deviceId':deviceStr}
        
        for i in range(connTime):
            device = MonkeyRunner.waitForConnection(timeOut, deviceStr)
            if device is not None:              
                # logging.info("Device Connected;", extra=self._logFMT)                
                #print "Device found..."
                break;
        
        return device
    
     

# ============================================================================
#   3.n     Self test
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    print 'running'
