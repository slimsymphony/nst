# This Python file uses the following encoding: utf-8
""" NST internal

"""

import re
import sys
import subprocess
import os
import signal
import time
import datetime
import logging
import warnings
import org.python.modules.sre.PatternObject
import codecs
import java
import java.lang.Exception
from java.util import HashMap


from com.nokia.nst.viewMgnt import View, ViewParser

DEBUG = False
DEBUG_DEVICE = DEBUG and False
DEBUG_RECEIVED = DEBUG and False
DEBUG_TREE = DEBUG and False
DEBUG_GETATTR = DEBUG and False
DEBUG_CALL = DEBUG and False
DEBUG_COORDS = DEBUG and False  
DEBUG_TOUCH = DEBUG and False
DEBUG_STATUSBAR = DEBUG and False
DEBUG_WINDOWS = DEBUG and False
DEBUG_BOUNDS = DEBUG and False
DEBUG_DISTANCE = DEBUG and False

WARNINGS = False 

class DeviceViewInterface:
    '''
    Based on UIAutomator, ADB channel, communicate with device side; 
    
    Main functionalities:
        (1)Dump the view xml file;
        (2)Parse and return the view information;
    
    '''
    
    def __init__(self, device, deviceStr, autodump=False, ignoreuiautomatorkilled=False):
        '''
        Constructor
        
        @type device: Phone Object
        @param device: The device running the C{View server} to which this client will connect
        @type serialno: str
        @param serialno: the serial number of the device or emulator to connect to
        '''
        self._device = device
        self._deviceStr = deviceStr
        self._autodump = autodump
        self._viewParser = ViewParser(self._deviceStr)
        self._ignoreuiautomatorkilled = ignoreuiautomatorkilled
        
        self._logger = logging.getLogger('')
        
        self._dumplogger = logging.getLogger('DUMPStats')
        
#         self._logger.debug('adb -s %s shell /system/bin/uiautomator server' % self._deviceStr)
#         host_exec('adb -s %s shell /system/bin/uiautomator server' % self._deviceStr)
#         
#         
#         time.sleep(3)
        
        ## A workaround to alias utf8 encoding to cp65001(Microsoft's utf8)
        try:
            codecs.lookup('cp65001')
        except:
            def cp65001(name):
                if name.lower() == 'cp65001':
                    return codecs.lookup('utf-8')
            codecs.register(cp65001)
    
    def host_exec(self, cmd):
      p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      out, msg= p.communicate()
      return out
    
    def dump(self, sleep=1):
        '''
        Dumps the window content and return the root of parsed view.
        
        Sleep is useful to wait some time before obtaining the new content when something in the
        window has changed.
        
        @type sleep: int
        @param sleep: sleep in seconds before proceeding to dump the content
        
        @return: return the root value of the 
        '''
        if(sleep > 0):
            
            time.sleep(sleep)
        
        '''
        Using /dev/tty this works even on devices with no sdcard
        '''
        startTime = datetime.datetime.now()
        #creationflags = subprocess.CREATE_NEW_CONSOLE
        #received = subprocess.call('cmd /c adb shell /system/bin/uiautomator client /dev/tty', creationflags = subprocess.CREATE_NEW_CONSOLE)
        #received = subprocess.call('adb shell /system/bin/uiautomator client /dev/tty', shell=True)
        #received = self.host_exec('adb -s %s shell /system/bin/uiautomator client /dev/tty' % self._deviceStr)

        
        try:
            
            #received = subprocess.check_output([adb, '-s', self._deviceStr, 'shell uiautomator dump /dev/tty'])
            rawReceived = self._device.executeShell('uiautomator dump /dev/tty >/dev/null')
            #rawReceived = self.host_exec('adb -s %s shell uiautomator dump /dev/tty' % self._deviceStr)
                
            if rawReceived:
                received = rawReceived.replace('UI hierchary dumped to: /dev/tty', '')
            else:
                received = rawReceived
                    
            
            #received = self.host_exec('adb -s %s shell uiautomator dump /dev/tty' % self._deviceStr)
        
        except Exception, value:
            #raise RuntimeError("ERROR: /system/bin/uiautomator client error occurs, will dump again!")
            errMsg = "ERROR: uiautomator dump /dev/tty >/dev/null error occurs, will dump again!"
            self._logger.error(errMsg)
            time.sleep(3)
            #received = subprocess.check_output([adb, '-s', self._deviceStr, 'shell uiautomator dump /dev/tty'])
            received = self._device.executeShell('uiautomator dump /dev/tty >/dev/null')

        
        
        
        
        
        
        for i in range(1,3):
            '''
            Try another 2 times;
            '''
            if not received:      
                '''
                Retry the dump 
                '''
                time.sleep(2)
                self._logger.warn("Empty UIAutomator dump was received, will dump again, dump counter:(%d)!" % (i+1))
                
                rawReceived = self.host_exec('adb -s %s shell uiautomator dump /dev/tty' % self._deviceStr)
                
                if rawReceived:
                    received = rawReceived.replace('UI hierchary dumped to: /dev/tty', '')
            
            else:
                break
        
        #print received
        finishTime = datetime.datetime.now()
        
        timeDelta = finishTime - startTime
        #self._logger.debug(received)
        #self._logger.debug(timeDelta)
        
        self._dumplogger.debug("dump time:"+str(timeDelta))
        
        if not received:
                
                errMsg = 'ERROR: Empty UIAutomator dump was received after 3 dump action!'            
                self._logger.error(errMsg)
                raise RuntimeError(errMsg)
        

        '''received = received.encode('utf-8', 'ignore')'''
        self.received = received
        
        if DEBUG:
            self.received = received
            print >> sys.stdout, self.received
        if DEBUG_RECEIVED:
            print >> sys.stderr, "received %d chars" % len(received)
            print >> sys.stderr
            print >> sys.stderr, repr(received)
            print >> sys.stderr
        onlyKilledRE = re.compile('[\n\S]*Killed[\n\r\S]*', re.MULTILINE)
        if onlyKilledRE.search(received):
            raise RuntimeError('''ERROR: UiAutomator output contains no valid information. UiAutomator was killed, no reason given.''')
        '''
        In rare case, this maybe used;
        '''
        if self._ignoreuiautomatorkilled:
            if DEBUG_RECEIVED:
                print >> sys.stderr, "ignoring UiAutomator Killed"
            killedRE = re.compile('</hierarchy>[\n\S]*Killed', re.MULTILINE)
            if killedRE.search(received):
                received = re.sub(killedRE, '</hierarchy>', received)
            elif DEBUG_RECEIVED:
                print "UiAutomator Killed: NOT FOUND!"
            
            ''' 
            It seems that API18 uiautomator spits this message to stdout
            '''
            dumpedToDevTtyRE = re.compile('</hierarchy>[\n\S]*UI hierchary dumped to: /dev/tty.*', re.MULTILINE)
            if dumpedToDevTtyRE.search(received):
                received = re.sub(dumpedToDevTtyRE, '</hierarchy>', received)
            if DEBUG_RECEIVED:
                print >> sys.stderr, "received=", received
        
        if re.search('\[: not found', received):
            raise RuntimeError('''ERROR: Some emulator images (i.e. android 4.1.2 API 16 generic_x86) does not include the '[' command.
                                While UiAutomator back-end might be supported 'uiautomator' command fails.
                                You should force ViewServer back-end.''')

        
        self._rootViewNode = self._viewParser.ParseToViewByStr(received)
        
        
        
        #self._logger.info(self._rootViewNode)
        
        return self._rootViewNode
    

    def setRootView(self, rootView):
        '''
        set the root view of the current parser
        '''
        self._rootViewNode = rootView._viewObject
    
    def findViewWithText(self, viewText):
        '''
        Find the view according to the view text;
        Return the DeviceView instance;
        '''
        viewByText = self._viewParser.FindViewByText(self._rootViewNode, viewText)
        return DeviceView(self._device, viewByText)
    
    def findViewWithTextContained(self, viewText):
        '''
        Find the view according to the view text, where contains the viewText;
        Return the DeviceView instance;
        '''
        viewByTextC = self._viewParser.FindViewByTextContained(self._rootViewNode, viewText)
        return DeviceView(self._device, viewByTextC)
    
    def findViewByClassAndIndex(self, vClassName, vIndex):
        '''
        Find the view according to the class and index;
        '''
        
        viewRet = self._viewParser.FindViewByClassAndIndex(self._rootViewNode, vClassName, vIndex)
        
        return DeviceView(self._device, viewRet)
    
    def findViewByClassAndText(self, vClassName, vText):
        '''
        Find the view according to the class and index;
        '''
        viewRet = self._viewParser.FindViewByClassAndText(self._rootViewNode, vClassName, vText)
        return DeviceView(self._device, viewRet)
    
    def findViewWithAttribute(self, attr='content-desc', value='OK'):
        '''
        Find the view according to the attribute and value;
        Return the DeviceView instance;
        ***To be noticed, other means not implemented yet;***
        '''
        
        if attr == 'content-desc':
            viewByCont = self._viewParser.FindViewByContDesc(self._rootViewNode, value)
            return DeviceView(self._device, viewByCont)
            
        else:
            #viewOjbect = self._viewParser.FindViewByTextContained(self._rootViewNode, value)
            
            attrsMap = {attr:value}
            viewOjbect = self.findViewWithAttributes(attrsMap)
            return viewOjbect
    
    def findViewWithAttributes(self, attrMap = {"content-desc":"OK"}):
        '''
        Find the view by attribute:value pair;
        '''
        attrHashMap = HashMap()
    
        for key in attrMap.keys():
            attrHashMap.put(key, attrMap[key])
    
        viewRet = self._viewParser.FindViewByAttibutes(self._rootViewNode, attrHashMap)
    
        return DeviceView(self._device, viewRet)
    
    def findViewsWithAttributes(self, attrMap = {"content-desc":"OK"}):
        '''
        Find all the views by attribute:value pair;
        Support the regex pattern for the text search;
        
        return the matched view list;
        
        '''
        attrHashMap = HashMap()
    
        for key in attrMap.keys():
            attrHashMap.put(key, attrMap[key])
    
        viewRets = self._viewParser.FindViewsByAttibutes(self._rootViewNode, attrHashMap)
    
        dViewRets = []
        
        for v in viewRets:
            dViewRets.append(DeviceView(self._device, v))
        
        return dViewRets
    
    def main(self):
        '''
        For test purpose only
        '''    
        self.dump() 
        
        #attrsMap = {"text":"Gallery","class":"android.widget.TextView", "index":2, "password":False}
        attrsMap = {"text":"Gallery"}
        
        #galleryView = self.findViewWithAttributes(attrMap = attrsMap)
        galleryView = self.findViewWithText("Gallery")
        
        print galleryView.getText()
        
        print galleryView.getStartX()
        print galleryView.getStartY()
        
        print galleryView.getWidth()
        print galleryView.getHeight()
        
        print self._rootViewNode.getStartX()
        
class NDeviceViewInterface(DeviceViewInterface):
    '''
    Tailored for NDevice View Dump
    '''
    def __init__(self, device, deviceStr, autodump=False, ignoreuiautomatorkilled=False):
        DeviceViewInterface.__init__(self, device, deviceStr,autodump, ignoreuiautomatorkilled)
    
    def dump(self, sleep=1):
        '''
        Dumps the window content.
        
        Sleep is useful to wait some time before obtaining the new content when something in the
        window has changed.
        
        @type sleep: int
        @param sleep: sleep in seconds before proceeding to dump the content
        
        @return: return the root value of the 
        '''
        if(sleep > 0):
            time.sleep(sleep)
        
        '''
        Using /dev/tty this works even on devices with no sdcard
        '''
        startTime = datetime.datetime.now()
        
        try:
            received = self._device.executeShell('/system/bin/uiautomator client')
        except:
            raise RuntimeError("ERROR: /system/bin/uiautomator client error occurs!")

        
        finishTime = datetime.datetime.now()
        
        timeDelta = finishTime - startTime
        
        self._logger.debug(timeDelta)
        
        if not received:            
            errMsg = 'ERROR: Empty UIAutomator dump was received'            
            self._logger.error(errMsg)
            raise RuntimeError(errMsg)
        

        '''received = received.encode('utf-8', 'ignore')'''
        
        if DEBUG:
            self.received = received
            print >> sys.stdout, self.received
        if DEBUG_RECEIVED:
            print >> sys.stderr, "received %d chars" % len(received)
            print >> sys.stderr
            print >> sys.stderr, repr(received)
            print >> sys.stderr
        onlyKilledRE = re.compile('[\n\S]*Killed[\n\r\S]*', re.MULTILINE)
        if onlyKilledRE.search(received):
            raise RuntimeError('''ERROR: UiAutomator output contains no valid information. UiAutomator was killed, no reason given.''')

        
        self._rootViewNode = self._viewParser.ParseToViewByStr(received)
        
        self._logger.info(self._rootViewNode)
        
        return self._rootViewNode

class ViewInterfaceFactory:
    
    @staticmethod
    def factory(ViewDumpMode,device, deviceStr):
        if ViewDumpMode == 'NType':
            return NDeviceViewInterface(device, deviceStr)
        else:
            return DeviceViewInterface(device, deviceStr)

class DeviceView:
    '''
    Device view to be operated;
    '''
    def __init__(self, device,viewObject):
        self._device = device
        self._viewObject = viewObject
        
    
    def touch(self,duration=0.05):
        '''
        Touches the center of this View
        '''
        
        (x, y) = self.getCenter()
        if DEBUG_TOUCH:
            print >>sys.stderr, "should touch @ (%d, %d)" % (x, y)
        
        
        self._device.touch(x, y, duration=duration, wait=0)
        """
        if type == MonkeyDevice.DOWN_AND_UP:
            if WARNINGS:
                print >> sys.stderr, "DeviceView: touch workaround enabled"
            self._device.touch(x, y, MonkeyDevice.DOWN)
            time.sleep(50/1000.0)
            self._device.touch(x+10, y+10, MonkeyDevice.UP)
        else:
            self._device.touch(x, y, type)
        """

    def drag(self, (destX, destY), duration=1.0, steps=10):
        '''
        Simulates a drag gesture (touch, hold, and move) on this view item;
        '''
        (x, y) = self.getCenter()
        

        #self._device.touch(x, y,  'DOWN')
        self._device.drag((x, y), (destX, destY),duration,steps)
        #self._device.touch(destX, destY,  'UP')

    def getCenter(self):
        '''
        Gets the center coords of the View
        '''
        x = self._viewObject.getStartX()
        y = self._viewObject.getStartY()
        width = self._viewObject.getWidth()
        height = self._viewObject.getHeight()
        
        centerX = x + width / 2
        centerY = y + height / 2
        return (centerX, centerY)
    
    def swipeToUpperBoundary(self):
        '''
        swipe from center to upper boundary
        '''
        (x, y) = self.getCenter()
        y2 = self._viewObject.getStartY()

        self._device.swipe((x,y),(x, 0), 1,10)
        
    def swipeToDownBoundary(self):
        '''
        swipe from center to down boundary
        '''
        (x, y) = self.getCenter()
        
        deviceHeight = int(self._device.getProperty('display.height')) 

        self._device.swipe((x,y),(x, deviceHeight), 1,10)

    def swipeToLeft(self):
        '''
        swipe from right to left within the boundary of this view
        '''
        (x, y) = self.getCenter()
        x2 = self._viewObject.getStartX()
        width = self._viewObject.getWidth()
                
        self._device.swipe((x2+width-1,y),(x2+1, y), 1,10)

    
    def swipeToRight(self):
        '''
        swipe from left to right within the boundary of this view
        '''
        (x, y) = self.getCenter()
        x2 = self._viewObject.getStartX()
        width = self._viewObject.getWidth()
                
        self._device.swipe((x2+1,y),(x2+width-1, y), 1,10)
    
    def getSubViews(self):
        '''
        return the subviews contained
        '''    
        subViews = []
        
        subViewOjbects = self._viewObject.getChildrenViews()
        
        
        for element in subViewOjbects:  
            viewEle = DeviceView(self._device, element)
            subViews.append(viewEle)
        
        return subViews
    
    def isExist(self):
        return self._viewObject is not None
        
        
'''
Execution Tips: 
monkeyrunner -plugin C:\nst\NSTViewMngt\build\lib\NSTViewMngt.jar C:\nst\NSTRunner\src\core\view.py
monkeyrunner C:\nst\NSTRunner\src\core\view.py
'''
if __name__ == '__main__':
    print 'running'
    
    #device = MonkeyRunner.waitForConnection(10, "87366c33")
    
    #device.wake()
    
    #dv = DeviceViewInterface(device, "87366c33")
    #dv.main()
    
    '''
    dv.dump()
    
    relView = dv.findViewByClassAndIndex('android.widget.RelativeLayout', 0)
    print '____'
    print len(relView.getSubViews())
    '''
    
    ''' for subview tesing
    dv.dump()

    listView = dv.findViewByClassAndIndex('android.widget.LinearLayout', 1)
    
    
    subViews = listView.getSubViews()
    mmsRegion = subViews[1]
    
    print mmsRegion._viewObject.getStartX()
    print mmsRegion._viewObject.getStartY()
    
    mmsSubViews = mmsRegion.getSubViews()
    
    print mmsSubViews
    
    print mmsSubViews[1]._viewObject.getStartX()
    print mmsSubViews[1]._viewObject.getStartY()
    mmsSubViews[1].getSubViews()[0].touch()
    '''
    #view = dv.findViewWithTextContained("Phone")
    #view.touch()
