# -*- coding: utf-8 -*-
"""
Created in Oct 2018

@author: disha
"""

import os,sys,os.path
import string
import time
from datetime import datetime, timedelta

import madrigalWeb.madrigalWeb

def getNextYearMonthDay(year,month,day):
    s = str(year) + "-" + str(month) + "-" + str(day)
    date = datetime.strptime(s, "%Y-%m-%d")
    modified_date = date + timedelta(days=1)
    ret = datetime.strftime(modified_date, "%Y-%m-%d").split("-")
    return int(ret[0]),int(ret[1]),int(ret[2])

#constants
madrigalUrl = 'http://www.haystack.mit.edu/madrigal'
instrument = 'World-wide GPS Receiver Network'

user_fullname = 'Disha Sardana'
user_email = 'dishas9@vt.edu'
user_affiliation = 'Virginia Tech'

# create the main object to get all needed info from Madrigal
madrigalObj = madrigalWeb.madrigalWeb.MadrigalData(madrigalUrl)

# these next few lines convert instrument name to code
code = None
instList = madrigalObj.getAllInstruments()
for inst in instList:
    if inst.name.lower() == instrument.lower():
        code = inst.code
        print "Found instrument!"
        print code
        break

if code == None:
    raise ValueError, 'Unknown instrument %s' % (instrument)


config = open("runConfig_eclipse.txt")
path ="C:/Users/disha/Desktop/eclipse-data-sonification/Madrigal Data/"

for line in config:
    params = line.split(" ")
    year = int(params[0])
    month = int(params[1])
    day = int(params[2])
    nextYear, nextMonth, nextDay = getNextYearMonthDay(year,month,day)
    print "Now fetching file for:"
    print str(year) + "-" + str(month) + "-" + str(day)
    print str(nextYear) + "-" + str(nextMonth) + "-" + str(nextDay)
    expList = madrigalObj.getExperiments(code, year,month,day,0,0,0,nextYear,nextMonth,nextDay,0,0,0)
    for exp in expList:
        print exp.startday
        print exp.endday
        if (exp.startday==day and exp.endday==nextDay):
            print "Here's the experiment!"
            print (str(exp) + '\n')

            fileList = madrigalObj.getExperimentFiles(exp.id)
            for thisFile in fileList:
                if thisFile.category == 1:
                    print (str(thisFile.name) + '\n')
                    thisFilename = thisFile.name

                    onlyFileName = thisFilename.split("/")
                    f = open(path + onlyFileName[len(onlyFileName)-1],"w")
                    f.close()
                    print "Beginning download for:"
                    print str(year) + "-" + str(month) + "-" + str(day)
                    result = madrigalObj.downloadFile(thisFilename, path + onlyFileName[len(onlyFileName)-1], user_fullname, user_email, user_affiliation, "simple")
                    print "Completed download for:"
                    print str(year) + "-" + str(month) + "-" + str(day)