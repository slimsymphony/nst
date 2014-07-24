'''
************************************Description******************************************
GroupNo:

CaseNo:

Test case description:

Author:

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
from core.uitestcase import UITestCase

#========================================================================================

class ClassName(UITestCase):
    def __init__(self):
        self._grouNO = '0100'
        self._caseNO = '001'
        super(ClassName, self).__init__(self._grouNO, self._caseNO, InsertPackageNameIfNeeded)

    def setUp(self):
        super(ClassName, self).setUp()

        """ Insert brief description of the setup logic"""
        # Insert code to perform pre-condition steps

    def tearDown(self):
        """ Insert brief description of the teardown logic"""
        # Insert code to perform clean up operations

        super(ClassName, self).tearDown()

    def testMethod(self):
        self._logger.info("1. Test step description ...")
        '''
        Test step1
        '''

        self._logger.info("2. Test step description ...")
        '''
        Test step2
        '''

if __name__ == '__main__':
    testCase = ClassName()
    testCase.main()

