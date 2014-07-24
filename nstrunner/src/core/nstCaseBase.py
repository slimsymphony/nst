# ============================================================================
#                              NSTCase module
#                           -----------------------
# ----------------------------------------------------------------------------

# ============================================================================
#   1   ABSTRACT
#
#   1.1 Module type
#
#       Basic case handling module, including common behaviors
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

import sys
import os
import datetime
import logging
import string
import re
from optparse import OptionParser

# this must be imported before MonkeyRunner and MonkeyDevice,
# otherwise the import fails
try:
    NST_HOME = os.environ['NST_HOME']
    # ANDROID_VIEW_CLIENT_HOME = os.environ['ANDROID_VIEW_CLIENT_HOME']
except KeyError:
    print >> sys.stderr, "%s: ERROR: NST_HOME not set in environment" % __file__
    sys.exit(1)

sys.path.append(NST_HOME + '/nstrunner/src')
sys.path.append(NST_HOME + '/nstrunner/cases')

from core.phone import Phone,ViewSelector, ValueNotFoundException


from interface.POXClient import POXClient
from com.nokia.nst.poxbackend import *
from redstone.xmlrpc import *

from com.nokia.nst.tools import ResultTransform

from core.cutcross import CutCross

class NSTCaseBase(object):
    
    '''
    Init the paras from command line
    '''
    def __init__(self, groupNO='0000', caseNO='0000'):
        
        self._groupNO = groupNO
        self._caseNO = caseNO
        
        # process the args
        self.__processCaseParameters()

        
        # init the direcotry for the test result storage
        self.__initDirectory(groupNO, caseNO)
        
        #init log setting
        self.__initLogConfig()
        
        #Get the logger
        self._logger = logging.getLogger('')
        self._logger.info("_______________Group %s Case %s Begin Init..._______________" % (groupNO, caseNO))
            
        # init the test result
        self._excutionInfo = NSTCaseExecution(groupNO, caseNO) 
        
    # setup the environment for the case running    
    def setUp(self):
        
        try:
            self._logger.info("_______________Group %s Case %s Begin Setup..._______________" % (self._groupNO, self._caseNO))        
    
            #init the device configuration

            # connect the phone
            self.__connectDevices()
        except Exception , err:
                '''
                Catch the exception at each loop, so the case execution can be continue;
                '''
                self._logger.error("ERROR: Case setup occurs; Details: %s ." % (str(err)))
            
    def __processCaseParameters(self):
        '''
        Process the input args, 
        which control the running behavior of the case running;
        '''     
        
        # parse the args
        parser = OptionParser()
        # parse the deviceid to run
        parser.add_option('-d', '--device', dest='deviceid',
                          help='device serial id in adb device list')
        '''
        parser.add_option("-f", "--file", dest="filename",
                          help="write report to FILE", metavar="FILE")
        parser.add_option("-q", "--quiet",
                          action="store_false", dest="verbose", default=True,
                          help="don't print status messages to stdout")
        '''
        parser.add_option('-r', '--refdevice', dest='refdeviceid',
                          help='reference device serial id in adb device list')

        '''
        Use 'o' to parse, since 'p', 's', 'v' is used by monkeyrunner
        '''
        parser.add_option('-o', '--poxdevice', dest='poxenabled',
                          help='pox client used for referencephone')
        
        (options, args) = parser.parse_args()
        
        
        #self._logger.debug(options)
        
        # use the command line args, if not provided use the default monitor
        if options.deviceid is not None:
            self._deviceId = options.deviceid
            
        else:
            self._deviceId = 'emulator-5554'
        
        self._deviceId2  = self._deviceId.replace(":", "-")
        
        if options.refdeviceid is not None:
            self._refDeviceid = options.refdeviceid
        else:
            self._refDeviceid = None
    
        
        if options.poxenabled is not None:
             
            self._poxenabled = options.poxenabled
        else:
            self._poxenabled = None
    
    def __initLogConfig(self):
        '''
        Init the log config, create the logger by case;
        The logger folder and file name under the following convention:
            (1)The folder will be under log/nstRunner/deviceSN
            (2)The file name will be [group+case]_[timestampe].log
        '''
        
        logLoc = "" 
        
        if self.__getTestPlanName() is None:
            logLoc = os.path.join(self._nstHome,"testresult", self._deviceId2,"nstrunner.log")
        else:
            logLoc = os.path.join(self._nstHome,"testresult", self.__getTestPlanName(), self._deviceId2,"nstrunner.log")
        
        self._cutCross = CutCross(logLoc, self._groupNO + self._caseNO)
        self._cutCross.initLogConfig()
    
    def __initDirectory(self, groupNO='0000', caseNO='0000'):
        
        nstHome = os.getenv("NST_HOME")
        
        self._nstHome = nstHome

        timeStr = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        
        resultLoc = "" 
        
        if self.__getTestPlanName() is None:
            resultLoc = os.path.join(self._nstHome, "testresult", self._deviceId2 , "nstrunner.testresult",self._groupNO + self._caseNO+timeStr)
        else:
            resultLoc = os.path.join(self._nstHome, "testresult", self.__getTestPlanName(), self._deviceId2, "nstrunner.testresult", self._groupNO + self._caseNO+timeStr)
        
        if not os.path.exists(resultLoc):
            os.makedirs(resultLoc)

        self._resultLoc = resultLoc
        self._resultLocTS = timeStr
    
    def __connectDevices(self):
        self.testAttr = 'testAttr'
        self.phone = Phone(self._deviceId)
        self.phone.connect()
        
        if self._refDeviceid is not None:
               
            self.refPhone = Phone(self._refDeviceid)
            self.refPhone.connect()
        else:
            self._logger.warn("WARN: No reference phone provided!")
         
        '''
            If using pox tag, create the POX client;
        '''

        if self._poxenabled=='1':
            
            self.refPhone_Pox = POXClient(phoneName="Reference", sim1NO=self.phone.getConfigItem('sim1number') ,deviceSN=self._deviceId )
            
            self.refPhone_Pox.startJob()
            self.refPhoneNumber_Pox = self.refPhone_Pox.getRobotPhone()
            
    def __getTestPlanName(self):
        '''
        Find the test plan name by device id in the specific folder;
        '''
        
        
        plannameLoc = os.path.join(self._nstHome, "rtdata")
        
        for file in os.listdir(plannameLoc):
            if self._deviceId in file:
                if re.search('[0-9]{14}$',file):
                    return file.split(".")[1]
        
        return None
        
        
    
    def expectText(self, expectText="OK"):
        '''
        1. Judge whether there is text in the current view
        2. Save the exeuction result; 
        '''
        result = NSTCaseResult(msg='Success!', isSuc=True)
        
        try:
            self.phone.expectText(isNeedDump=True, expectText=expectText)
        except ValueNotFoundException, e:
            setattr(result, '_msg', 'Failed!')
            setattr(result, '_isSuc', False)
            self._logger.info("_______________Group %s Case %s Expecting Text %s Failed!_______________" % (self._groupNO , self._caseNO, expectText))
        
        ts = datetime.datetime.now() 
        tss = datetime.datetime.strftime(ts, "%Y%m%d%H%M%S")
        
        imageName = tss + ".png"
        
        filename = os.path.join(self._resultLoc, imageName)
        
        self.phone.dumpImageToFile(filename) 
        setattr(result, '_imageLoc', filename)        
        setattr(result, '_finishTime', ts)
        setattr(result, '_expectStr', expectText)
        
        #log the result
        self._logger.info("[EXPECTRESULT]:%s"%str(result._isSuc))
        self._logger.info("[RESULTIMGLOC]:%s"%str(filename))
        
        self._excutionInfo._results.append(result)

    
    def expectAttribute(self, expectAttr="content-desc", expectValue="OK"):
        '''
        1. Judge whether there is text in the current view
        2. Save the exeuction result; 
        '''
        result = NSTCaseResult(msg='Success!', isSuc=True)
        
        try:
            self.phone.expectAttrValue(expectAttr=expectAttr, expectValue=expectValue)
        except ValueNotFoundException, e:
            setattr(result, '_msg', 'Failed!')
            setattr(result, '_isSuc', False)
            self._logger.info("_______________Group %s Case %s Expecting Attribute %s with value %s Failed!_______________" % (self._groupNO, self._caseNO, expectAttr,expectValue))
        
        ts = datetime.datetime.now() 
        tss = datetime.datetime.strftime(ts, "%Y%m%d%H%M%S")
        
        imageName = tss + ".png"
        
        filename = os.path.join(self._resultLoc, imageName)
        
        #print filename
        
        self.phone.dumpImageToFile(filename) 
        setattr(result, '_imageLoc', filename)
        setattr(result, '_finishTime', ts)
        
        #log the result
        self._logger.info("[EXPECTRESULT]:%s"%str(result._isSuc))
        self._logger.info("[RESULTIMGLOC]:%s"%str(filename))
        
        self._excutionInfo._results.append(result)
        
    def saveResult(self, result):
        '''
        Will store the result, please specify the result parameter with attributes:
            isSuc=False, 
            expectStr=''
            msg=''
        '''
        
        if result is None:
            return
    
        ts = datetime.datetime.now() 
        tss = datetime.datetime.strftime(ts, "%Y%m%d%H%M%S")
        
        imageName = tss + ".png"
        
        filename = os.path.join(self._resultLoc, imageName)
        
        #print filename
        
        self.phone.dumpImageToFile(filename) 
        setattr(result, '_imageLoc', filename)
        setattr(result, '_finishTime', ts)
        
        #log the result
        self._logger.info("[EXPECTRESULT]:%s"%str(result._isSuc))
        self._logger.info("[RESULTIMGLOC]:%s"%str(filename))
        
        self._excutionInfo._results.append(result)
        
    
    # tear down the environment for this case
    def tearDown(self):
        
        try:
            self._logger.info("_______________Group %s Case %s Begin to TearDown..._______________" % (self._groupNO, self._caseNO))
            
            '''
            Close the pox job;
            '''
            if hasattr(self, "refPhone_Pox"):
                if self.refPhone_Pox:
                    self.refPhone_Pox.close()
        except Exception , err:
            '''
            Catch the exception at each loop, so the case execution can be continue;
            '''
            self._logger.error("ERROR: Exception occurs when pox backend closing in teardown ; Details: %s ." % (str(err)))
            
        try:  
            self._excutionInfo._endTime = datetime.datetime.now()
            
            runtimeSec = self._excutionInfo._endTime - self._excutionInfo._startTime 
            
            self._logger.info("_______________Group %s Case %s, total runtime: %s ._______________" % (self._groupNO, self._caseNO, runtimeSec))
            
            '''
            Save the result to the folder with the fileName;
            '''
            
            self._logger.info("_______________Start to generate test result for Group %s Case %s ._______________" % (self._groupNO, self._caseNO))
            
            xmlResult = self._excutionInfo.toXMLStr()
            
            timeStr = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
            
            fileName = "r_" + timeStr + ".res"
            
            fileFullName = os.path.join(self._resultLoc, fileName)
            
            resFile = open(fileFullName, 'w+')
            
            resFile.write(xmlResult)
            
            resFile.close()
                        
            self._logger.info("[RESULTID]:%s" % (self._groupNO + self._caseNO+self._resultLocTS))
            self._logger.info("[CASERESULT]:%s" % str(self._excutionInfo.getCaseResult()))
            
            finalResFile = os.path.join(self._resultLoc,self._resultLocTS+'.html')
            
            self._logger.info("[RESULTFILE]:_______________Result file is generated at: %s ___________________" % (finalResFile))
            #Generate the result file
            resultGen = ResultTransform()
            
            inputXSLT = os.path.join(self._nstHome, "nstrunner","res","ResultTransform.xslt")
            
            
            
            resultGen.genTestResult(self._resultLoc, inputXSLT, finalResFile)
            
            self._logger.info("_______________Group %s Case %s Finish TearDown..._______________" % (self._groupNO, self._caseNO))
    
        except Exception , err:
            
            self._logger.error("ERROR: Exception occurs when case teardown; Details: %s ." % (str(err)))
            
            
class NSTCaseExecution:
    '''
    Case execution object.
    '''
    def __init__(self, groupNO='0000', caseNO='0000', startTime=datetime.datetime.now(), endTime=datetime.datetime.now()):
        self.attrDict = {}
        
        self._groupNO = groupNO
        self._caseNO = caseNO
        self._startTime = startTime
        self._endTime = endTime
        
        self.attrDict['groupNO'] = groupNO
        self.attrDict['caseNO'] = caseNO
        self.attrDict['startTime'] = startTime
        self.attrDict['endTime'] = endTime 
        
        self._results = []
    
    def getCaseResult(self):
        '''
        Get the case level result
        '''
        
        #if the result is none return false;
        if not self._results:
            return False
        
        for res in self._results:
            '''
            If any of the step is false, return False;
            '''
            if  not res._isSuc:
                return False
        
        return True
    
    def toXMLStr(self):
        '''
        XML Serialization for this object.
        '''
        childStr = ""  # XML string of children
        
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'groupNO', 'a':self._groupNO }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'caseNO', 'a':self._caseNO }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'startTime', 'a':self._startTime }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'endTime', 'a':self._endTime }
        
        '''
        append the result string
        '''
        resStr = ""        
        for res in self._results:
            resStr += res.toXMLStr()
        
        resultsStr = '<results>%s</results>' % resStr
        
        return '<executionInfo>%s%s</executionInfo>' % (childStr, resultsStr)
        
        
class NSTCaseResult:
    '''
    Case execution result
    '''
    
    def __init__(self, finishTime=datetime.datetime.now(), msg='', imageLoc='', isSuc=False, expectStr=''):
        self.attrDict = {}
        
        self._finishTime = finishTime
        self._msg = msg
        self._imageLoc = imageLoc
        self._isSuc = isSuc
        self._expectStr = expectStr
        
        self.attrDict['finishTime'] = finishTime
        self.attrDict['msg'] = msg
        self.attrDict['imageLoc'] = imageLoc
        self.attrDict['isSuc'] = isSuc
        self.attrDict['expectStr'] = expectStr
        
        
    def toXMLStr(self):
        '''
        XML Serialization for this object.
        '''
        
        
        childStr = ""  # XML string of children
        
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'finishTime', 'a':self._finishTime }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'msg', 'a':self._msg }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'imageLoc', 'a':self._imageLoc }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'isSuc', 'a':self._isSuc }
        childStr += "<%(n)s>%(a)s</%(n)s>" % { 'n':'expectStr', 'a':self._expectStr }
        
        serilizedStr = '<result>%s</result>' % childStr
        
        return serilizedStr
        
