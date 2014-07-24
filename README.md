# NST

> NST is an test automation tool for AoL,.

[![NPM version](https://badge.fury.io/js/NST.png)](https://npmjs.org/package/NST)
[![Build Status](https://api.travis-ci.org/NST/NST.png?branch=master)](https://travis-ci.org/NST/NST)

## Supported Platforms

* Android

## Why NST?

1. You don't have to recompile your app or modify it in any way, due
   to use of standard automation APIs on all platforms.
2. You can write tests with your favorite dev tools using any [WebDriver](https://code.google.com/p/selenium/wiki/JsonWireProtocol)-compatible
   language such as Java, [Objective-C](https://github.com/NST/selenium-objective-c),
   JavaScript with Node.js (in both [callback](https://github.com/admc/wd) and [yield-based](https://github.com/jlipps/yiewd) flavours),
   PHP, Python, [Ruby](https://github.com/NST/ruby_lib), C#, Clojure, or Perl
   with the Selenium WebDriver API and language-specific client libraries.
3. You can use any testing framework.

Investing in [WebDriver](https://code.google.com/p/selenium/wiki/JsonWireProtocol) means you are betting
on a single, free and open protocol for testing that has become a defacto standard. Don't lock yourself into a proprietary stack.

If you use Apple's UIAutomation library without NST you can only write tests
using JavaScript and you can only run tests through the Instruments application.
Similarly, with Google's UiAutomator you can only write tests in Java. NST
opens up the possibility of true cross-platform native mobile automation. Finally!

## Requirements

Your environment needs to be setup for the particular mobile platforms that you
want to run tests on. See below for particular platform requirements.

If you want to run NST via an `npm install`, hack with or contribute to NST, you will need
[node.js and npm](http://nodejs.org) 0.8 or greater (`brew install node`).

To verify that all of NST's dependencies are met you can use `NST-doctor`.
Run `NST-doctor` and supply the `--ios` or `--android` flags to verify that all
of the dependencies are set up correctly. If running from source, you may have to use
`bin/NST-doctor.js` or `node bin/NST-doctor.js`.

### Android Requirements

* [Android SDK](http://developer.android.com) API &gt;= 17 (Additional features require 18)
  * Add the path to "platform-tools" and "tools" to environment parameter "PATH". Make sure you can get device ID for each DUT using "adb devices"
  * Create new environment parameter "ANDROID_HOME" and set it to the path of "SDK"
* Install [Jython](http://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.5.3/jython-installer-2.5.3.jar) using "java -jar jython-installer-2.5.3.jar"
  * Create new environment parameter "JYTHON_HOME" and set it to the path of "Jython"
* Get the latest NST package from GIT or the [link](https://source.nokia.com/projects/6199-nst/repositories/28161)
  * Create new environment parameter "NST_HOME" and set it to the path of "NSTRunner"
* Set each device ID(DUT & RefPhone) into configuration file:
Open the config file named "deviceConfiguration.ini" under "$NST_HOME/config/". 
Add each device connected to the testing server into the configuration file following the format below:(You can get all of the information from Script Team)

        [4bb249b3]                       #Device ID
        ViewDumpMode=Standard            #UI dump mode, default "Standard"
        SIM1Number=13703131234           #SIM card number for slot 1
        SIM2Number=10086                 #SIM card number for slot 2 (DS only)
        NeedUnlock=1                     #Auto Unlock screen
        PreloadPath=/home/nst/preload    #Storage location for preload data
        DUTType=N2                       #DUT type, e.g. N1, N2, AOL2, AOL3, or etc.
        ServiceNo=8888                   #POX number
        TestMail=testmail@163.com        #Email address for testing
        Password=1234567                 #Password for test mail





## Quick Start
There are two ways to run a test:
### Using Jython

`$ jython /root/NST2/NSTRunner/cases/test/MTBF59001406_SearchForWLANNetworks.py -d c2a4261 -r 995b62c5`

* -d for DUT; -r for RefPhone

### Using the App
Kick up an NST server, and then run a test written in jython script!

* Set the "TestPlan.xml" under “$NST_HOME"
* Run it!

`$ java -jar nta-0.0.6-snapshot.jar TestPlan.xml`

## Multiple DUTs
 1. Set second device ID(DUT & RefPhone) into configuration file
 2. Set the "TestPlan.xml" under "$NST_HOME". Add second line of "target-device" for DUT & RefPhone

Run it!

`$ java -jar nta-0.0.6-snapshot.jar TestPlan.xml`  

## Multiple Tasks
NST can run more than two tasks at the same time!

 1. Set second device ID(DUT & RefPhone) into configuration file
 2. Create a new "TestPlan_2.xml" under "$NST_HOME"
 3. Check the folder "Device" under "$NST_HOME". Delete the files with the name with second device ID(DUT & RefPhone)

Run it!

`$ java -jar nta-0.0.6-snapshot.jar TestPlan_2.xml`  


## Writing Tests for NST

The main guide for getting started writing and running tests is [the running tests](https://github.com/NST/NST/blob/master/docs/running-tests.md) doc, which includes explanations for iOS, Android, and Android older devices.

Essentially, we support a subset of the [Selenium WebDriver JSON Wire Protocol](https://code.google.com/p/selenium/wiki/JsonWireProtocol), and extend it so that you can specify mobile-targeted [desired capabilities](https://github.com/NST/NST/blob/master/docs/caps.md) to run your test through NST.

You find elements by using a subset of WebDriver's element-finding strategies.
See [finding elements](https://github.com/NST/NST/blob/master/docs/finding-elements.md) for detailed information. We also have several extensions to the JSON Wire Protocol for [automating
mobile gestures](https://github.com/NST/NST/blob/master/docs/gestures.md)
like tap, flick, and swipe.

You can also automate web views in hybrid apps! See the [hybrid app
guide](https://github.com/NST/NST/blob/master/docs/hybrid.md)

This repository contains [many examples of tests in a variety of different languages](https://github.com/NST/NST/tree/master/sample-code/examples)!

For the full list of NST doc pages, visit [this directory](https://github.com/NST/NST/blob/master/docs/).

## How It Works

NST drives various native automation frameworks.

NST uses the UiAutomator framework for newer platforms and
[Selendroid](http://github.com/DominikDary/selendroid) and UiAutomator for older Android platforms.

## Contributing

Please take a look at our [contribution documentation](https://source.nokia.com/projects/6723-nst-dev/repositories/31460/entry/master/AUTHORS)
for instructions on how to build, test and run NST from source.


## Mailing List

Announcements and debates often take place on the [Discussion Group](https://source.nokia.com/projects/6723-nst-dev/repositories/31460/entry/master/AUTHORS), be sure to sign up!

## Troubleshooting

We put together a [troubleshooting guide](https://github.com/NST/NST/blob/master/docs/troubleshooting.md).
Please have a look here first if you run into any problems. It contains instructions for checking a lot
of common errors and how to get in touch with the community if you're stumped.

