'''
Cut-cross lib, including logging, exception etc;
'''
import re
import sys
import subprocess
import os
import datetime
import logging
import logging.config

class CutCross:
    
    def __init__(self, loggingFolder, logFileNamePre):
        self._loggingFolder = loggingFolder
        self._logFileNamePre = logFileNamePre
        
        if not os.path.exists(loggingFolder):
            os.makedirs(loggingFolder)
    
    def initLogConfig(self):
        
        #For further handling
        logFileName = self._logFileNamePre +"_"+ datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S") + ".log"
        #logFileName = "nstRunner.log"
        
        fullLogFileName = os.path.join(self._loggingFolder , logFileName)
        
        dumpLogFileName = "dumpcount.log"
        fulldumpLogFileName = os.path.join(self._loggingFolder , dumpLogFileName)
        
        # set up logging to file
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s %(name)-2s %(levelname)s: %(message)s',
                            datefmt='%m-%d %H:%M:%S',
                            filemode='w',
                            filename=fullLogFileName)
        
        # define a Handler which writes ERROR messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        # set a format which is simpler for console use
        #formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        
        formatter = logging.Formatter(fmt='%(asctime)s %(name)-2s %(levelname)s: %(message)s',
                            datefmt='%m-%d %H:%M:%S')

        # tell the handler to use this format
        #console.setFormatter(formatter)
        
        # define a Handler to the sys.stdout
        outputInfo = logging.StreamHandler(sys.stdout)
        outputInfo.setLevel(logging.DEBUG)
        outputInfo.setFormatter(formatter)
        
        #init the dump stats info log file
        dumpOutputInfo = logging.FileHandler(fulldumpLogFileName, mode='a')
        dumpOutputInfo.setLevel(logging.DEBUG)
        dumpOutputInfo.setFormatter(formatter)
        
        
        # add the handler to the root logger
        #logging.getLogger('').addHandler(console)
        logging.getLogger('').addHandler(outputInfo)
        
        logging.getLogger('DUMPStats').addHandler(dumpOutputInfo)
        
        
        
        logging.info("_______________Log Init___________________")
        
        logging.info("[LOGFILE]:%s" % (logFileName))
        
