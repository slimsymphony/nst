# This Python file uses the following encoding: utf-8
# version=0.8.1.14205

import re
import sys
import subprocess
import platform
import java
import os
import time
import logging
import org.python.modules.sre.PatternObject


try:
    NST_HOME = os.environ['NST_HOME']
except KeyError:
    print >> sys.stderr, "%s: ERROR: NST_HOME not set in environment" % __file__
    sys.exit(1)
sys.path.append(NST_HOME + '/nstrunner/src')

NST_JARS = NST_HOME + '/nstrunner/jars/'

sys.path.append(NST_JARS + 'NSTViewMngt.jar')
sys.path.append(NST_JARS + 'NSTResultGen.jar')
sys.path.append(NST_JARS + 'ADBExecutor.jar')
sys.path.append(NST_JARS + 'NSTPOXBackend.jar')

from com.nokia.nst.viewMgnt import ViewParser, View

from core.view import DeviceViewInterface, DeviceView, ViewInterfaceFactory
from core.deviceManager import DeviceManager
from interface.sViewClient import sViewClient

from com.nokia.adbexecutor import IADBExecutor, ADBExecutor

DEBUG = False

class Phone:
    
    #key number pad dict to mapping with MoneyDevice
    keyNumDict = None
    
    def __init__(self, deviceStr):
        
        #Get the logger
        self._logger = logging.getLogger('')
        
        # the connection string from adb devices
        self._deviceStr = deviceStr
        
        #self._exectorWrapper = new ADBExecutor(deviceStr)
        
        #get the configuration dictionary
        self._deviceConfig = DeviceManager.getDevicesConfiguration(deviceStr)
        
        self._logger.info("Case will use configuration: %s ." % self._deviceConfig)
        
        localPort = self.getConfigItem('localviewserverport')        
        
        self._localport = None
        
        if localPort is not None:
            self._localport = int(localPort)
            
        
        
    # ============================================================================
    #   1   Phone CONNECTION and STATUS MANAGEMENT 
    # ----------------------------------------------------------------------------
    
    # connect the device through adb
    def connect(self):
        '''
        Provide the following tasks:
        (1)Connect to the device through sn and get the basic configuration of the device;
        (2)Instance the view client for device view structure dump and parse;
        (3)Connect to the view server;
        '''
        try:
            self._logger.info("_______________Device with SN String  has been connected._______1________")
            
            #deviceManager = DeviceManager()
            self._device =  ADBExecutor(self._deviceStr)
            
            '''
            if self._device is not None:
                self._device.wake()
            '''
            self._logger.info("_______________Device with SN String %s has been connected._______________" % (self._deviceStr))
            
        except Exception , e:
            self._logger.critical("CRITICAL ERROR: Device with SN String %s can not be connected! Details: (%s)." % (self._deviceStr, e))
        except:
            self._logger.critical("CRITICAL ERROR: Device with SN String %s can not be connected! Details: Unknown Issue!" % (self._deviceStr))
        
        
        try: 
            # self._viewclient = ViewClient(self._device, self._deviceStr)   
            self._viewclient = ViewInterfaceFactory.factory(self.getConfigItem('viewdumpmode'), self, self._deviceStr)
            
            
            self.viewSelector = ViewSelector(self)
            self.multiViewSelector = ViewSelectors(self)
            
        except:
            self._logger.error("ERROR: The viewclient of Device with SN String %s can not be initialized!" % (self._deviceStr))
        
        try:
            self.initDeviceProperty()
        except:
            self._logger.error("ERROR: The Internal properties of Device with SN String %s can not be obtained!" % (self._deviceStr))
        
        try:
            
            self._sViewClient = None
            if self._localport is not None:
                self.startSViewServer()
                self._sViewClient = sViewClient(localport= self._localport)
                
        except:
            self._logger.error("ERROR: The standard viewclient of Device with SN String %s can not be initialized!" % (self._deviceStr))
    
    def initDeviceProperty(self):
        '''
        init the dievice property
        '''
        self._displaySize = self.getDisplaySize()
    
    def getConfigItem(self, itemName):
        '''
        Get the item value from configuration file; 
        '''
        
        itemValue = None
        
        try:

            itemValue = self._deviceConfig[itemName] 
        except KeyError, ke:
            self._logger.error("ERROR: Occurs at getConfigItem from Phone, no key with %s found ; Details: %s;" % (itemName, ke))
        
        return itemValue
                
#     def disConnect(self):
#         self._device.ShellExecute('adb shell ')
    
    # ============================================================================
    #   2   PHONE BEHAVIOR, including PRESS, TOUCH, MOVE,NAVIGATE etc
    # ----------------------------------------------------------------------------
    
    # navigate to the activity
    
    def getDisplaySize(self):
        '''
        Get the system display size
        '''

        width = -1
        height = -1
        
        if self._device is not None:
            width = self._device.GetDisplayWidth()
            height = self._device.GetDisplayHeight() 
        
        return (width, height)
    
    
    def setPowerSaveMode(self, status=1):
        '''
        Set the power save mode;
        '''
        self._device.PowserSave(status)
    
    def backToStartWindow(self):
        """
        From the helper method;
        """
        type = self.getConfigItem('duttype').upper()
        packageName = ""
        
        if type in ['AOL', 'AOL2']:
            packageName = 'com.nokia.homescreen'
            self._logger.debug("Press Home Key to back to Home Screen ...")
            self.pressKey('KEYCODE_HOME')
            self.sleep(1)
            self.pressKey('KEYCODE_HOME')
            self.sleep(1)
            self.swipeFromRightToLeft()
            self.sleep(0.5)
        if type in ['AOL15', 'AOL3']:
            packageName = 'com.nokia.homescreen'
            self._logger.debug("Swipe to back to Home Screen ...")
            self.pressKey('KEYCODE_HOME')
            self.sleep(1)
            self.swipeFromLeftToRight()
            self.sleep(1)
            self.swipeFromRightToLeft()
            self.sleep(1)
            self.swipeFromRightToLeft()
            self.sleep(0.5)
        else:
            """
            For N1, N2
            """
            packageName = 'com.proto.launcher'
            self._logger.debug("Send ADB command to start Launcher Activity ...")
            self.executeShell("am start -a android.intent.action.MAIN -c android.intent.category.HOME -n com.proto.launcher/.LauncherActivity")
            self.waitForUpdateOrSleep(5)
            self.sleep(2)

            self._viewclient.dump()
            self.sleep(2)
            if self._viewclient.findViewByClassAndIndex('android.widget.ListView', 1).isExist():
                self._logger.debug("In Fastlane now ...")
                if self._viewclient.findViewWithAttribute( value = 'Edit Fastlane').isExist():
                    self._logger.debug("In Fastlane editing mode ...")
                    self.pressKey('KEYCODE_BACK')
                    self.sleep(2)
                self.pressKey('KEYCODE_BACK')

        found = False
        self._viewclient.dump()
        if self._viewclient.findViewWithAttributes({'package':packageName, 'text': 'Search'}).isExist():
            found = True

        if found:
            self._logger.debug("Reach application list ...")
        else:
            raise Exception("Phone: backToStartWindow: Cannot back to application list ...")


    def pureBack(self, needCheckCrash=True, delegatedExceptionHandlerMap={}):
        """
        From the helper method;
        """
        self._logger.debug("Press Back Key until back to Home Screen ...")
        counter = 30
    
        while counter > 0:
            if needCheckCrash:
                # it dumps the screen in checkCrash function
                if self.checkCrash():
                    self.sleep(1)
                    self._viewclient.dump()
            else:
                self._viewclient.dump()
                
            for packageName in delegatedExceptionHandlerMap.keys():
                if self._viewclient.findViewWithAttribute(attr = 'package', value = packageName).isExist():
                    delegatedExceptionHandlerMap[packageName]()
                    self.sleep(2)
                    self._viewclient.dump()
                    break
    
            if self._viewclient.findViewWithAttribute(attr = 'package', value = 'com.proto.launcher').isExist():
                break
            if self._viewclient.findViewWithAttribute(attr = 'package', value = 'com.nokia.homescreen').isExist():
                break
    
            self.pressKey('KEYCODE_BACK')
            self.sleep(1)
    
            counter -= 1
    
    
    def checkCrash(self):
        """
        From the helper method;
        """
        self._viewclient.dump()
        foundCrash = False
        if self._viewclient.findViewWithTextContained("has stopped").isExist():
    
            self._viewclient.findViewWithTextContained("OK").touch()
            self._logger.debug("Application Crash Detected!")
            foundCrash = True
        elif self._viewclient.findViewWithTextContained("isn't responding").isExist():
    
            self._viewclient.findViewWithTextContained("OK").touch()
            self._logger.debug("Application ANR Detected!")
            foundCrash = True
            
        return foundCrash


    def forceStopAppWithPackageName(self, package_name):
        self._viewclient.dump()
        if self._viewclient.findViewWithAttribute(attr = 'package', value = 'com.proto.launcher').isExist():
            return True
        elif self._viewclient.findViewWithAttribute(attr = 'package', value = 'com.nokia.homescreen').isExist():
            return True
        else:
            self._logger.debug("Phone: forceStopAppWithPackageName: Force stop application '%s'" % package_name)
            self._device.ShellExecute("am force-stop %s" % package_name)
            return False


    def startActivity(self, type, packageName, activityName):
        runComponent = packageName + '/' + activityName
        self._device.StartActivity(packageName, activityName)
    
    # Judge if the current view contain specific text;
    def exitTextInView(self, isNeedDump=True, txt='OK'):
        # Dump the view
        if(isNeedDump):
            self._viewclient.dump()
        # find the text in view
        view = self._viewclient.findViewWithText(txt)

        if(view._viewObject is None):
            
            self._logger.info("Expect:False")
            
            return False
        else:
            return True
    
    def expectText(self, isNeedDump=True, expectText='OK'):
        '''
        check if there is a expectText in the View
        '''
        
        
        
        isExitText = self.exitTextInView(isNeedDump=isNeedDump, txt=expectText)

        if(isExitText):
            pass
        else:
            raise ValueNotFoundException(expectText)
    
    def expect(self, patternMap, referencePatternMap, isRefresh, referenceLevel=2):
        """
        based on the selector, will return the result;
        """
        patternStr = "".join(' %s=%s' % (key, value) for (key, value) in patternMap.iteritems())
        
        try:
            targetView = self.viewSelector.findViewInCurrentWindow(patternMap=patternMap, referencePatternMap=referencePatternMap, referenceLevel=referenceLevel)
            
            if targetView and targetView.isExist():
                pass
            else:
                raise ValueNotFoundException( patternStr)
        
        except ViewNotFoundException, ve:
            
            raise ValueNotFoundException( patternStr)

    
    def notExpect(self, patternMap, referencePatternMap, isRefresh):
        """
        
        """
        
        patternStr = "".join(' %s=%s' % (key, value) for (key, value) in patternMap.iteritems())
        
        try:
            targetView = self.viewSelector.findViewInCurrentWindow(patternMap=patternMap, referencePatternMap=referencePatternMap)
            
            if targetView and targetView.isExist():
                raise ValueNotFoundException(patternStr, False)
            else:
                pass
                
        
        except ViewNotFoundException, ve:
            pass
        
            
            
        
    
    # Judge if the current view contain specific attribute value;
    def exitAttributeValueInView(self, isNeedDump=True, attr='content-desc', value='OK'):
        # Dump the view
        if(isNeedDump):
            self._viewclient.dump()
        # find the text in view
        view = self._viewclient.findViewWithAttribute(attr, value)
        
        if(view._viewObject is None):
            return False
        else:
            return True
    
    def expectAttrValue(self, isNeedDump=True, expectAttr='content-desc', expectValue='OK'):
        '''
        check if there is a expectAttribute with exepecValue in the View
        '''
        
        #print expectAttr
        #print expectValue
        
        isExitText = self.exitAttributeValueInView(isNeedDump, expectAttr, expectValue)
        
        if(isExitText):
            pass
        else:
            raise ValueNotFoundException(expectAttr + " with value: " + expectValue)
    
    
    
    # ============================================================================
    #   Gestures and action
    # ----------------------------------------------------------------------------
    # Input some text on the touched textbox
    def input(self, text):
        
        self._device.Input(text)
        
        """
        for c in text:
            if c != ' ':
                self._device.type(c)
            else:
                self._device.press('KEYCODE_SPACE', MonkeyDevice.DOWN_AND_UP)
        """
    
    
    def clear(self, count=1):
        """
        use chimpchat IDevice interface to do:
        http://stackoverflow.com/questions/9474877/android-chimpchat-pressing-backspace
        """
        for i in range(0,count):
            #self._device.getManager().keyDown("KEYCODE_DEL")
            #self._device.press('KEYCODE_DEL', MonkeyDevice.DOWN_AND_UP)
            self._device.Delete()
    
    
    def back(self, count=1, duration=0.05):
        '''
        default duration is 50ms;
        '''
        self.pressKey('KEYCODE_BACK', count, duration)
        #self._device.PressBack()
    
    
    def volumeUp(self, count=1):
        '''
        '''
        self.pressKey('KEYCODE_VOLUME_UP', count=count)
    
    def volumeDown(self, count=1):
        '''
        '''
        self.pressKey('KEYCODE_VOLUME_DOWN', count=count)
    
    def pressKey(self,keyCode, count=1, duration=0.05):
        
        for i in range(0,count):
            self._device.Press(keyCode,'DOWN')
            self.sleep(1)
    
    def touch(self, x, y,duration=0.05,wait = 0.05,  count=1, isShell=False):
        
        '''
        touch method, support the shell input mode;
        support duration for whole touch event, and wait after touch, and multi touch(count);
        
        Attention: the duration is not supported in the shell execution mode;
        '''
        
        for i in range(0,count):
        
            #wait before each action
            time.sleep(wait)
        
            if isShell:
                self.shellTouchExecute(x, y)
            else:
                self._device.Touch(x, y, int(duration*1000))
                
                
    
    def drag(self, (x1, y1), (x2,y2), duration=1.0, steps=10):
        '''
        currently, we just use MR drag to simulate the swipe;
        '''
        self._device.Drag(x1, y1,x2, y2,steps)        
    
    def swipe(self, (x1, y1), (x2,y2), duration=0.2, steps=10):
        '''
        currently, we just use MR drag to simulate the swipe;
        '''
        self._device.Swipe(x1, y1,x2, y2,steps)
    
    def swipeFromLeftToRight(self, isShell=False):
        '''
        swith from the left side to the right side        
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        hCenter = height / 2
        if isShell:
            self.shellSwipeExecute((1,hCenter),(width-1, hCenter))
        else:
            self.swipe((1,hCenter),(width-1, hCenter), 1,10)
    
    
    def swipeFromRightToLeft(self, isShell=False):
        '''
        swith from the right side to the left side        
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        hCenter = height / 2
        if isShell:
            self.shellSwipeExecute((width-1,hCenter),(1, hCenter))
        else:    
            self.swipe((width-1,hCenter),(1, hCenter), 1,10)
    
    def swipeFromUpToDown(self,isShell=False):
        '''
        swith from the up side to the down side        
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        vCenter = width / 2
        if isShell:
            self.shellSwipeExecute((vCenter,1),(vCenter, height-1))
        else: 
            self.swipe((vCenter,1),(vCenter, height-1), 1,10)
    
    def swipeFromDownToUp(self,isShell=False):
        '''
        swith from the down side to the up side        
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        vCenter = width / 2
        if isShell:
            self.shellSwipeExecute((vCenter,height-1),(vCenter, 1))
        else:
            self.swipe((vCenter,height-1),(vCenter, 1), 1,10)
    
    def swipeFromCenterToDown(self,isShell=False):
        '''
        swith from the up side to the down side        
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        hCenter = width / 2
        
        vCenter = height / 2
        if isShell:
            self.shellSwipeExecute((hCenter,vCenter),(hCenter, height-1))
        else:
            self.swipe((hCenter,vCenter),(hCenter, height-1), 1,10)
    
    def swipeFromCenterToUp(self,isShell=False):
        '''
        swith from the down side to the up side        
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        hCenter = width / 2
        
        vCenter = height / 2
        
        if isShell:
            self.shellSwipeExecute((hCenter,vCenter),(hCenter, 1))
        else:
            self.swipe((hCenter,vCenter),(hCenter, 1), 1,10)
    
    
    def zoomOut(self,pct=0.3):
        '''
        perform a zoom-out action at the center screen,
        due to the limitation of mr, this is an alternative way to zoomOut. 
        '''
        
        (width, height) = self.getScreenSize()
        
        
        """
        self._device.touch(hCenter, vCenter,  MonkeyDevice.DOWN_AND_UP)
        self._device.touch(hCenter, vCenter,  'DOWN')
        self._device.drag((int(hCenter*(1+pct)), int(vCenter*(1+pct))),(hCenter, vCenter) ,0.2,10)
        self._device.touch(hCenter, vCenter,  'UP')
        """
        self._device.PerformTwoPointerGesture(100, int(height/5),width-10, height-10, 
                                               int(100+width*pct), int(100+height*pct), 
                                               int((width-10)*(1-pct)), int((height-10)*(1-pct)),
                                               30)

    
    def zoomIn(self,pct=0.3):
        '''
        perform a zoom-in action at the center screen,
        due to the limitation of mr, this is an alternative way to zoomIn.
        '''
        
        (width, height) = self.getScreenSize()
        
        hCenter = width / 2
        
        vCenter = height / 2
        
        """
        self._device.touch(hCenter, vCenter,  MonkeyDevice.DOWN_AND_UP)
        self._device.touch(hCenter, vCenter,  'DOWN')
        self._device.drag((hCenter, vCenter), (int(hCenter*(1+pct)), int(vCenter*(1+pct))),0.2,10)
        self._device.touch(int(hCenter*(1+pct)), int(vCenter*(1+pct)),  'UP')
        """
        
        self._device.PerformTwoPointerGesture(hCenter-10, vCenter-10,hCenter+10, vCenter+10, 
                                               int((hCenter-10)*(1-pct)), int((vCenter-10)*(1-pct)),
                                               int((hCenter+10)*(1+pct)), int((vCenter+10)*(1+pct)),
                                               30)

    
    def getScreenSize(self):
        '''
        '''
        width = self.getDisplaySize()[0]
        height = self.getDisplaySize()[1]
        
        return (width, height)
    
    def shellSwipeExecute(self, (x1, y1), (x2, y2)):
        '''
        shell swipe method 
        '''
        self.executeShell("input swipe %d %d %d %d" % (x1, y1, x2, y2))
    
    def shellTouchExecute(self,x,y):
        '''
        shell tap method
        '''
        self.executeShell("input tap %d %d" % (x,y))
    
    
    @staticmethod
    def initKeyNumPadDic():
        Phone.keyNumDict = {
                      '0': 'KEYCODE_NUMPAD_0', 
                      '1': 'KEYCODE_NUMPAD_1',
                      '2': 'KEYCODE_NUMPAD_2',
                      '3': 'KEYCODE_NUMPAD_3',
                      '4': 'KEYCODE_NUMPAD_4',
                      '5': 'KEYCODE_NUMPAD_5',
                      '6': 'KEYCODE_NUMPAD_6',
                      '7': 'KEYCODE_NUMPAD_7',
                      '8': 'KEYCODE_NUMPAD_8',
                      '9': 'KEYCODE_NUMPAD_9',
                      'ENTER':'KEYCODE_NUMPAD_ENTER'
                      }
        
    
    def dialNumber(self, number='10086', sleepSec=0.01):
        '''
        Dial the number
        '''
        
        if Phone.keyNumDict is None:
            Phone.initKeyNumPadDic()
        
        for c in number:
            self.pressKey(Phone.keyNumDict[c])            
            time.sleep(sleepSec)
    #
    
    def sleep(self, sleepSec):
        time.sleep(sleepSec)
    
    def waitForUpdateOrSleep(self, sleepSec):
        if self._sViewClient is not None:
            try:
                if self._sViewClient.getVersion() is None:                
                    '''
                    Restart the server if no response
                    '''
                    self.stopSViewServer()
                    self.startSViewServer()
                    
                self._sViewClient.waitForUpdate()
                
            except:
                self._logger.error("ERROR: Error occurs when wait for update from view server, will use the sleep way.")
                time.sleep(sleepSec)
            
        else:
            time.sleep(sleepSec)
    
    # ============================================================================
    #   3   APP Test CODE
    # ----------------------------------------------------------------------------
    
    # appFullName, including the path;
    def installAPP(self, apkFullName):
        #self._device.installPackage(apkFullName)
        pass
        
    # run the test of the specific apk;
    def runRobotiumTest(self, apkFullName):
        pass
    
    
    # ============================================================================
    #   4   Utilities
    # ----------------------------------------------------------------------------    
    
    # clear the log in logcat cache
    def clearLog(self):
        self.executeShell('logcat -c')
    
    # dump the log to the server/computer file sys
    def dumpLog(self, filePath):
        proc = subprocess.Popen("adb logcat", shell=True, stdout=subprocess.PIPE)

        while True:
            line = proc.stdout.readline()
            if line != '':
                # the real code does filtering here
                print "test:", line.rstrip()
            else:
                break
        
        '''
        #cmd = 'adb shell logcat -d > '+filePath
        cmd = 'adb shell logcat -d > /dev/tty'
        
        print cmd

        #pipe = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE)           
        #print pipe.stdout.readlines()
        #subprocess.call("exit 1", shell=True)
        p = subprocess.Popen([self._viewclient.adb, '-s', self._deviceStr,'logcat', '-d', '>', filePath], shell=True, stdout=subprocess.PIPE)
        
        print p.stdout.readlines()
        
        #subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        #os.system(cmd)
        #subprocess.Popen(cmd, shell=True)
        #os.p('adb logcat -d > '+filePath)
               
        #self.executeShell('logcat -d > '+filePath)
        '''
   
    def convertCoordinate(self,x, y, toLandscape=True):
        '''
        
        ''' 
        (width, height) = self.getDisplaySize()
        
        if toLandscape:
            return (y,width-x)
        else:
            return (width-y,x)
            
        
   
    def executeShell(self, command):
        return self._device.ShellExecute(command)
    
    
    def startSViewServer(self):
        '''
        Connect to the standard view server
        '''        
        #Check the status of viewserver, then start it;
        if not self.serviceResponse(self.executeShell('service call window 3')):
            try:
                
                #self._logger.info('service call window 1 i32 %d' % self._localport)
                self.serviceResponse(self.executeShell('service call window 1 i32 4939'))
            except:
                msg = 'Cannot start View server.\n' \
                        'This only works on emulator and devices running developer versions.\n' \
                        'Does hierarchyviewer work on your device?'  
                raise Exception(msg)        
        #forward the port
        adb = Phone.obtainAdbPath()
                
        subprocess.check_call([adb, '-s', self._deviceStr, 'forward', 'tcp:%d' % self._localport, 'tcp:4939'])
      
        
    def stopSViewServer(self):
        '''
        Stop the view server
        '''
        try:
            self.serviceResponse(self.executeShell('service call window 2 i32 4939'))
        except:
            msg = 'Cannot stop View server.\n' \
                    'This only works on emulator and devices running developer versions.\n' \
                    'Does hierarchyviewer work on your device?'  
            raise Exception(msg)
    
    def killProcess(self, processName):
        '''
        kill the specific process by name
        '''
        
        adb = Phone.obtainAdbPath()

        p = subprocess.Popen([adb, '-s', self._deviceStr, 'shell', 'ps' ], stdout=subprocess.PIPE)
        
        out, err = p.communicate()
        
        for line in out.splitlines():
            
            if processName in line:
                pid = int(line.split(None)[1])
                
                subprocess.check_call([adb, '-s', self._deviceStr, 'shell', 'kill', '-9', str(pid) ])
                
                self._logger.info("Process %s with PID: %d is killed!" %(processName, pid))
        
    def serviceResponse(self, response):
        '''
        Checks the response received from the I{ViewServer}.

        @return: C{True} if the response received matches L{PARCEL_TRUE}, C{False} otherwise
        '''
        
        #self._logger.info(response)

        PARCEL_TRUE = "Result: Parcel(00000000 00000001   '........')\r\n"
        ''' The TRUE response parcel '''
        return response == PARCEL_TRUE
    
    def dumpImageToFile(self, filename, format="PNG"):
        '''
        Write the View image to the specified filename in the specified format.
        
        @type filename: str
        @param filename: Absolute path and optional filename receiving the image. If this points to
                         a directory, then the filename is determined by the serialno of the device and
                         format extension.
        @type format: str
        @param format: Image format (default format is PNG)
        '''
        
        if not os.path.isabs(filename):
            raise ValueError("writeImageToFile expects an absolute path")
        if os.path.isdir(filename):
            filename = os.path.join(self._deviceStr + '.', filename + format.lower())

        try:
            self._device.TakeScreenshot(filename)
            self._logger.debug("writeImageToFile: saving image to '%s' in %s format" % (filename, format))
        except Exception, e:
            self._logger.error("ERROR: DumpImageToFile Failed! Details: %s." % (e))       
    
    @staticmethod
    def obtainAdbPath():
        '''
        Obtains the ADB path attempting know locations for different OSs
        '''

        #osName = platform.system()
        osName = java.lang.System.getProperty('os.name')
        
               
        isWindows = False
        if osName.startswith('Windows'):
            adb = 'adb.exe'
            isWindows = True
        else:
            adb = 'adb'

        ANDROID_HOME = os.environ['ANDROID_HOME'] if os.environ.has_key('ANDROID_HOME') else '/opt/android-sdk'
        HOME = os.environ['HOME'] if os.environ.has_key('HOME') else ''

        possibleChoices = [ os.path.join(ANDROID_HOME, 'platform-tools', adb),
                           os.path.join(HOME,  "android", 'platform-tools', adb),
                           os.path.join(HOME,  "android-sdk", 'platform-tools', adb),
                           adb,
                           ]

        if osName.startswith('Windows'):
            possibleChoices.append(os.path.join("""C:\Program Files\Android\android-sdk\platform-tools""", adb))
            possibleChoices.append(os.path.join("""C:\Program Files (x86)\Android\android-sdk\platform-tools""", adb))
        elif osName.startswith('Linux'):
            possibleChoices.append(os.path.join("opt", "android-sdk-linux",  'platform-tools', adb))
            possibleChoices.append(os.path.join(HOME,  "opt", "android-sdk-linux",  'platform-tools', adb))
            possibleChoices.append(os.path.join(HOME,  "android-sdk-linux",  'platform-tools', adb))
        elif osName.startswith('Mac'):
            possibleChoices.append(os.path.join("opt", "android-sdk-mac_x86",  'platform-tools', adb))
            possibleChoices.append(os.path.join(HOME,  "opt", "android-sdk-mac", 'platform-tools', adb))
            possibleChoices.append(os.path.join(HOME,  "android-sdk-mac", 'platform-tools', adb))
            possibleChoices.append(os.path.join(HOME,  "opt", "android-sdk-mac_x86",  'platform-tools', adb))
            possibleChoices.append(os.path.join(HOME,  "android-sdk-mac_x86",  'platform-tools', adb))
        else:
            # Unsupported OS
            pass

        for exeFile in possibleChoices:

            if os.access(exeFile, os.X_OK):
                return exeFile

        for path in os.environ["PATH"].split(os.pathsep):
            exeFile = os.path.join(path, adb)
            if exeFile != None and os.access(exeFile, os.X_OK if not isWindows else os.F_OK):
                return exeFile

        raise Exception('adb="%s" is not executable. Did you forget to set ANDROID_HOME in the environment?' % adb)

class ViewSelectors(object):
    '''
    return the views that match the pattern in the current screen;
    '''
    def __init__(self,phone):
        self.phone=phone
        #Get the logger
        self._logger = logging.getLogger('')
    
    def __call__(self, patternMap):
        self.phone._viewclient.dump()
        return self.phone._viewclient.findViewsWithAttributes(patternMap)
        
        
        
class ViewSelector(object):
    '''
    contain the xpath selection of view;
    '''
    def __init__(self,phone):
        self.phone=phone
        #Get the logger
        self._logger = logging.getLogger('')
    
    
    def __call__(self, patternMap,timeout=60,referencePatternMap=None,referenceLevel=2, searchDir='vertical', isRefresh=True):
        '''
        Find the view according to the pattern;
        If 'referencePattern' and Level is provided, it will find the refer object and find under the upper referenceLevel;
        
        Mainly used for 2 scenario for the 'hard view finding':
            (1)Find the view which hide in the 'List', it will automatically scroll the window to find the target view;
            (2)Find the view which hard to determine, but there is a reference view easy to find; 
                e.g., the checkbox next to the text 'Show layout bounds', which is typically exist the settings;
        
        
        If no view or reference view found, will throw the ViewNotFoundException;
        
        
        Parameters:
            patternMap, attribute map of view to be found;
            timeout, N/A, to be updated;
            referencePatternMap, attribute map of the reference view;
            referenceLevel, the parent/upper level which target view and reference view shared;
            searchDir, the scroll direction for search; 
        '''
        return self.__findView(patternMap, timeout, referencePatternMap, referenceLevel, searchDir,isRefresh)
    
    
    
    def findViewInCurrentWindow(self,patternMap, referencePatternMap=None, referenceLevel=2, searchDir='vertical'):
        '''
        Find the target view that exits only in current window;
        '''
        
        
        self.phone._viewclient.dump()
        
        
        preReceived = self.phone._viewclient.received
        
        findPatternMap = patternMap
        
        if referencePatternMap:
            findPatternMap = referencePatternMap
        
        viewFirst = self.phone._viewclient.findViewWithAttributes(findPatternMap)
        
        if not viewFirst.isExist():
            raise ViewNotFoundException(str(patternMap))
        
        if referencePatternMap:
            '''
            If not the target view, found the target view from the upper level;
            '''
            targetParent = viewFirst
            # self._logger.debug(targetParent.getCenter())
            for pLoop in range(0, referenceLevel):
                targetParent = DeviceView(self.phone._device, targetParent._viewObject.getParentView())
                
            
            self.phone._viewclient.setRootView(targetParent)
            
            return self.phone._viewclient.findViewWithAttributes(patternMap)

        else:
            return viewFirst
    
    def __findView(self, patternMap, timeout=60, referencePatternMap=None, referenceLevel=2, searchDir='vertical', isRefresh=True):
        
        firstDirectionDumpCounter = 0
        secondDirectionDumpCounter = 0
        directionTurnCounter = 0
        
        if isRefresh:
            self.phone._viewclient.dump() 
        
        preReceived = self.phone._viewclient.received
        
        findPatternMap = patternMap
        
        if referencePatternMap:
            findPatternMap = referencePatternMap
        
        '''
        scroll until the view is find
        '''
        viewFirst = self.phone._viewclient.findViewWithAttributes(findPatternMap)
        
        swipeBack = False
        
        # beginning time
        begin = time.time()
        
        while(True):
            
            '''
            break if timeout
            '''
            if time.time() - begin > timeout:
                raise ViewNotFoundException(str(patternMap) + " in %d seconds." % timeout)
            
            '''
            break until the targetView is found;
            '''
            if viewFirst.isExist():
                break
            
            if searchDir=='vertical':
                if swipeBack:
                    self.phone.swipeFromCenterToDown()
                else:
                    self.phone.swipeFromCenterToUp()
            else:
                if swipeBack:
                    self.phone.swipeFromLeftToRight()
                else:
                    self.phone.swipeFromRightToLeft()
            
            self.phone._viewclient.dump()
            
            if swipeBack:
                secondDirectionDumpCounter = secondDirectionDumpCounter+1
            else:
                firstDirectionDumpCounter =firstDirectionDumpCounter+1
                
            
            received = self.phone._viewclient.received
            viewFirst = self.phone._viewclient.findViewWithAttributes(findPatternMap)
            
            #break when the target view is found;
            if viewFirst.isExist():
                break
            
            if preReceived == received:
                swipeBack = not swipeBack                
                directionTurnCounter = directionTurnCounter+1
                
            
            
            if directionTurnCounter>=2:
                #self._logger.debug(directionTurnCounter)
                raise ViewNotFoundException(str(patternMap))
            
            if swipeBack:
                '''
                ignore the dump due there is no view found at the first Direction Search
                '''
                for i in range(1,firstDirectionDumpCounter-1):
                    if searchDir=='vertical':
                        self.phone.swipeFromCenterToDown()
                    else:
                        self.phone.swipeFromLeftToRight()
                    
                firstDirectionDumpCounter = 0
                
            preReceived = received

        '''
        scorll to the center
        '''
        self.__scrollToCenter(viewFirst, searchDir)
        '''
        search again
        '''
        self.phone._viewclient.dump()
        viewFirst = self.phone._viewclient.findViewWithAttributes(findPatternMap)
        
        if referencePatternMap:
            '''
            If not the target view, found the target view from the upper level;
            '''
            targetParent = viewFirst
            #self._logger.debug(targetParent.getCenter())
            for pLoop in range(0, referenceLevel):
                targetParent = DeviceView(self.phone._device, targetParent._viewObject.getParentView())
                
            
            self.phone._viewclient.setRootView(targetParent)
            
            return self.phone._viewclient.findViewWithAttributes(patternMap)

        else:
            return viewFirst
        
    def __scrollToCenter(self, view, searchDir='vertical'):
        '''
        scroll the view to the center or the 'delta' scroll, avoid the 'hidden view'
        '''
        return
        
        if not view:
            raise ViewNotFoundException(str(view)) 
        
        vX, vY = view.getCenter()
        
        pW, pH = self.phone.getScreenSize()
        
        if searchDir=='vertical':
            self.phone.swipe((vX,vY),(vX, pH/2), 1,10)
            
        else:
            self.phone.swipe((vX,vY),(pW/2, vY), 1,10)
            
        
        
class ValueNotFoundException(Exception):
    '''
    TextNotFoundException is raised when a text/content-desc is not found.
    '''
       
    def __init__(self, value, isValueExpect = True):
        
        if isValueExpect:
            msg = "Couldn't find the %s in the view!" % (value)
        else:
            msg = "Find the %s in the view that unexpected!" % (value)
            
        super(Exception, self).__init__(msg)    
        
class ViewNotFoundException(Exception):
    '''
    ViewNotFoundException is raised when a text/content-desc is not found.
    '''
       
    def __init__(self, value):
        msg = "Couldn't find the view, details:%s" % (value)
        super(Exception, self).__init__(msg)    






