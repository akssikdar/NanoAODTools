#!/usr/bin/env python
import os, time, socket, sys, argparse

def PrCom(str):
    print str
    os.system(str)

BaseCMSDir = os.environ["CMSSW_BASE"]+"/src"
BaseHOME   = os.environ["HOME"]

parser = argparse.ArgumentParser(description="NanoAOD producer in CONDOR")
parser.add_argument('--NanoAOD','-nano',type=str,
                    help='Dataset to be processed.')
parser.add_argument('--Year', '-y', type=str, default="2018",
                    help='Data period')
parser.add_argument('--DataSet', '-ds', type=str, default="mc",
                    choices=["mc","top","mujets","ejets","mumu","ee","mue"],
                    help='DataSet to be processed')
parser.add_argument('--Time', '-t', type=int, default=18,
                    help='Time to schedule the job. Default 18 hours.')

args = parser.parse_args()

# RefTag = "TEST"
RefTag      = time.strftime('%Hh%Mm%Ss')
RunFileName = "ToCondorHisto_" + RefTag
LstFileName = "FListTemporal_" + RefTag
shFileName  = "shSubTemporal_" + RefTag

# LXPLUS machine
TimeFlavour = args.Time # Runtime in hours
CERNmachine = "lxplus" in socket.gethostname() 

# Copy proxy to available lxplus location
print "\n-------------------------------------------------"
user = str(os.getuid())
print "user " + os.getlogin() + ": " + user
FileProxy = "x509up_u" + user
print "looking for PROXY in /tmp/" + FileProxy

if os.path.isfile("/tmp/" + FileProxy):
    print "File /tmp/" + FileProxy + " found!"
else:
    print "/tmp/" + FileProxy + " file not found. You must first create your credentials by: \n\nvoms-proxy-init -voms cms\n"
    quit()
print "-------------------------------------------------"

# Create list of files 
print "Requiring dataset files by:"
PrCom( 'das_client -query="file dataset=' + args.NanoAOD + '" > ' + LstFileName)

flist = open(LstFileName, "r")
ListOfSamples = flist.readlines()
print "Sample with " + str(len(ListOfSamples)) + " files."
if len(ListOfSamples) == 0:
    print "[ERROR] There are no available files!"
    exit

print "-------------------------------------------------"
print "creating executable " + shFileName
fsh = open(shFileName, "w")
print>>fsh, '#!/bin/bash'
if CERNmachine:
    print>>fsh, '''
export X509_USER_PROXY=$2
voms-proxy-info -all
voms-proxy-info -all -file $2
    '''
else:
    print>>fsh, 'source $VO_CMS_SW_DIR/cmsset_default.sh'
print>>fsh, 'RunConfig=$1'
print>>fsh, 'cd ' + BaseCMSDir + '/PhysicsTools/NanoAODTools/python/postprocessing/UserCode'
print>>fsh, 'scram build ProjectRename'
print>>fsh, 'eval `scram runtime -sh`'
print>>fsh, 'python postprocNanoAODCIEMAT.py $RunConfig'


fsh = None
os.chmod(shFileName,0744)
print "-------------------------------------------------"

headfile = "root://cms-xrd-global.cern.ch//"
#headfile = "root://xrootd-cms.infn.it//"
SubArg = ""

fout = open(RunFileName, "w")
print>>fout, '\n######################\n'
print>>fout, 'executable = ' + shFileName
print>>fout, 'universe   = vanilla'
print>>fout, 'use_x509userproxy = True'
print>>fout, 'should_transfer_files   = YES\n'
print>>fout, '\n######################\n'
print>>fout, 'log    = job_Loc_$(ClusterId)_$(ProcId).log'
print>>fout, 'output = job_Loc_$(ClusterId)_$(ProcId).info'
print>>fout, 'error  = job_Loc_$(ClusterId)_$(ProcId).err'
print>>fout, '\n######################\n'

if CERNmachine:
    print>>fout, '# Setting the runtime manually: '     
    print>>fout, '+MaxRuntime = ' + str(int(TimeFlavour*60.*60.)) # Runtime in seconds 
    print>>fout, '''
# It can be done also as:
# +JobFlavour = "FlavName"
# Where the available flavours are:
# espresso     = 20 minutes
# microcentury = 1 hour
# longlunch    = 2 hours
# workday      = 8 hours
# tomorrow     = 1 day
# testmatch    = 3 days
# nextweek     = 1 week
    '''
    print>>fout, '\n######################\n'
    PrCom ( 'cp /tmp/' + FileProxy + ' ' + BaseHOME + '/private/')
    print>>fout, 'Proxy_path = ' + BaseHOME + '/private/' + FileProxy
    SubArg = " $(Proxy_path)"
    print>>fout, '\n######################\n'


for NanoFile in ListOfSamples:
    print>>fout, 'arguments = "\'--Year=' + args.Year + ' --DataSet=' + args.DataSet + ' --NanoInput=' + headfile+NanoFile.rstrip() + '\' ' + SubArg + '"'
    print>>fout, 'queue'
    print>>fout, '\n######################\n'

fout = None
os.chmod(RunFileName,0744)

if CERNmachine:
    command = 'condor_submit ' + RunFileName
else:
    #command = 'condor_submit -remote condorsc1.ciemat.es ' + RunFileName
    print 'Use lxplus to submit condor '

print 'Submitting job with command: '
PrCom( str(command) )
# print ( str(command) )
print ("Deleting temporal files....")
PrCom( "rm " + RunFileName )
PrCom( "rm " + LstFileName )
PrCom( "rm " + shFileName )
# print( "rm " + RunFileName )
# print( "rm " + LstFileName )
# print( "rm " + shFileName )
