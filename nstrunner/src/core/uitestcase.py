'''
************************************Description******************************************

    Base class to be used in UI test cases.

*****************************************************************************************
'''

#========================================================================================
import os
import sys

try:
    NST_HOME = os.environ['NST_HOME']
except KeyError:
    print >>sys.stderr, "%s: ERROR: NST_HOME not set in environment" % __file__
    sys.exit(1)

sys.path.append(NST_HOME + '/nstrunner/src')
sys.path.append(NST_HOME + '/nstrunner/cases')
sys.path.append(NST_HOME + '/nstrunner/cases/util')

from core.phone import Phone
from core.phone import ValueNotFoundException
from core.nstCaseBase import NSTCaseBase
from core.nstCaseBase import NSTCaseResult
import Helper

#========================================================================================

class UITestCase(NSTCaseBase):
    def __init__(self, groupNO='0000', caseNO='0000', forceStopPackage=None):
        self._grouNO = groupNO
        self._caseNO = caseNO
        self._forceStopPackage = forceStopPackage
        super(UITestCase, self).__init__(self._grouNO, self._caseNO)

    def basicSetup(self):
        super(UITestCase, self).setUp()

    def setUp(self):
        self._logger.info("_______________UI TestCase setUp_______________")
        '''
        Unlock the device
        '''
        self.phone._viewclient.dump()
        if(self.phone.getConfigItem('needunlock') =='1'):
            Helper.unlockDevice(self.phone)
            self.phone.sleep(2)

    def tearDown(self):
        self._logger.info("_______________UI TestCase tearDown_______________")
        self.phone.pureBack(delegatedExceptionHandlerMap={'com.android.keyguard': self._tearDownForKeyguard, \
            'com.nokia.glancescreen': self._tearDownForKeyguard})
        if self._forceStopPackage is not None:
            if not self.phone.forceStopAppWithPackageName(self._forceStopPackage):
                self._logger.info("UI TestCase: (%s), force stop Package: (%s)." % ((self._grouNO + self._caseNO), self._forceStopPackage))

    def basicTeardown(self):
        super(UITestCase, self).tearDown()

    def testMethod(self):
        pass

    def main(self):
        '''
            setUp
        '''
        try:
            self.basicSetup()
        except RuntimeError, rte:
            self._logger.warning("RuntimeError occurs in basicSetup, Details: %s ." % (str(rte)))
        except Exception, err:
            self._logger.warning("Exception occurs in basicSetup, Details: %s ." % (str(err)))

        try:
            # Compatible with previous version
            self.setUp()
        except RuntimeError, rte:
            self._logger.warning("RuntimeError occurs in setUp, Details: %s ." % (str(rte)))
        except Exception, err:
            self._logger.warning("Exception occurs in setUp, Details: %s ." % (str(err)))

        isBackOperationFail = False
        try:
            self._logger.info("UITestCase: setUp: Make sure phone is in Apps list")
            self.phone.backToStartWindow()
        except RuntimeError, rte:
            isBackOperationFail = True
            self._logger.warning("RuntimeError occurs in backToStartWindow, Details: %s ." % (str(rte)))
        except Exception, err:
            isBackOperationFail = True
            self._logger.warning("Exception occurs in backToStartWindow, Details: %s ." % (str(err)))

        if isBackOperationFail:
            try:
                self._logger.warning("UITestCase: setUp: Press back until it returns to homescreen")
                self.phone.pureBack(delegatedExceptionHandlerMap={'com.android.keyguard': self._tearDownForKeyguard, \
                    'com.nokia.glancescreen': self._tearDownForKeyguard})
            except RuntimeError, rte:
                self._logger.warning("RuntimeError occurs in pureBack, Details: %s ." % (str(rte)))
            except Exception, err:
                self._logger.warning("Exception occurs in pureBack, Details: %s ." % (str(err)))

            try:
                self._logger.warning("UITestCase: setUp: Make sure phone is in Apps list again!")
                self.phone.backToStartWindow()
            except RuntimeError, rte:
                self._logger.warning("RuntimeError occurs in backToStartWindow, Details: %s ." % (str(rte)))
            except Exception, err:
                self._logger.warning("Exception occurs in backToStartWindow, Details: %s ." % (str(err)))

        '''
            test Method
        '''
        try:
            self.testMethod()
        except RuntimeError, rte:
            self._logger.error("RuntimeError occurs in runTest, Details: %s ." % (str(rte)))
            result = NSTCaseResult(msg = 'Failed!', isSuc = False)
            self.saveResult(result)
        except Exception, err:
            self._logger.error("Exception occurs in runTest, Details: %s ." % (str(err)))
            result = NSTCaseResult(msg = 'Failed!', isSuc = False)
            self.saveResult(result)
        else:
            result = NSTCaseResult(msg = 'Successful!', isSuc = True)
            self.saveResult(result)

        '''
            tearDown
        '''
        # Save testing result
        try:
            self.basicTeardown()
        except RuntimeError, rte:
            self._logger.warning("RuntimeError occurs in basicTeardown, Details: %s ." % (str(rte)))
        except Exception, err:
            self._logger.warning("Exception occurs in basicTeardown, Details: %s ." % (str(err)))

        try:
            self.tearDown()
        except RuntimeError, rte:
            self._logger.warning("RuntimeError occurs in tearDown, Details: %s ." % (str(rte)))
        except Exception, err:
            self._logger.warning("Exception occurs in tearDown, Details: %s ." % (str(err)))

    def _tearDownForKeyguard(self):
        self.phone._logger.info("UITestCase: _tearDownForKeyguard: Deal with keyguard state")
        Helper.unlockDevice(self.phone)
