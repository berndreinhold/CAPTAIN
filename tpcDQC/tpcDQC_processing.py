#/usr/bin/python

#call from /home/reinhold/AmC_processing.sh
import os
import subprocess
import re
import sys
import math
#from ROOT import TFile, TTree, TSQLServer, TSQLResult, TSQLRow


class RunProcessing:
    def __init__(self):
        self.excluded_runs = [] #exclude runs from processing with tpcDQC
        self.input_dir = "/global/project/projectdirs/captain/data/2016/"
	self.out_dir = self.input_dir + "tpcDQC/"
        self.input_dir += "TPC/Feb/" #input to SLAD 

        self.lAvailableRuns=[]
	self.lProcessedRuns=[]
	self.lRuns2HTML=[]

    def available_for_processing(self):
        """
        check for ubdaq.gz file - more sophisticated checks could be implemented later.
        """
        for file in os.listdir(self.input_dir):
            match = re.findall(r'mCAPTAIN_EXT-([0-9]{4})-0.ubdaq.gz', file)
            if match: self.lAvailableRuns[len(self.lAvailableRuns):]=[int(match[0])]
        self.lAvailableRuns.sort()
        
	print self.lAvailableRuns
	print "number of available runs in input_dir(%s): %d" % (self.input_dir, len(self.lAvailableRuns))

    def processed_runs(self):
	for file in os.listdir(self.out_dir):
	    match = re.findall(r'tpcDQC_([0-9]{4}).root', file)
	    #print file, match	
	    if match: self.lProcessedRuns[len(self.lProcessedRuns):]=[int(match[0])]
	self.lProcessedRuns.sort()
	print self.lProcessedRuns
	print "number of processed runs in out_dir(%s): %d" % (self.out_dir, len(self.lProcessedRuns))

    def loop(self):

	start_dir = os.getcwd()
	os.chdir("/global/homes/r/reinhol1/work/captain/software/work-area/runArea/fake-devel/tpcDataQuality/")
        #os.chdir("/global/project/projectdirs/captain/users/ysun/software3/work-area/tpcDataQuality/Linux-Scientific-6.4-x86_64")
        #subprocess.call(["/bin/bash `capt-setup`"], shell=True)
	os.chdir("Linux-Scientific-6.4-x86_64/")
        
	print(os.getcwd())
    
	self.processed_runs()
        self.available_for_processing()

        sProcessedRuns = set(self.lProcessedRuns)
        sAvailableRuns = set(self.lAvailableRuns)
        sNewRuns = sAvailableRuns - sProcessedRuns
        print("new runs available for processing:")
        print(sNewRuns)

	for run in sNewRuns:
            if run in self.excluded_runs: continue 
            try:
                #./TPCDATAQUALITY.exe -tubdaq /global/project/projectdirs/captain/data/2016/TPC/Feb/mCAPTAIN_EXT-5213-0.ubdaq.gz -o tpcDQC_5213.root 
                argument_list = ["./TPCDATAQUALITY.exe", "-tubdaq", "%s/mCAPTAIN_EXT-%d-0.ubdaq.gz" % (self.input_dir, run), "-o %stpcDQC_%d.root" % (self.out_dir, run)]
                print(argument_list)
                p1 = subprocess.call(argument_list)
                if p1 < 0: print >>sys.stderr, "p1 was terminated by signal", -retcode
                    #p2 = subprocess.call(["./WriteMasasXY", "/home/reinhold/totransfer/Run%06d.root" % run, "0"])
                    #if p2 < 0: print >>sys.stderr, "p2 was terminated by signal", -retcode
                    #p3 = subprocess.call(["./WriteJasonsXY", "/home/reinhold/totransfer/Run%06d.root" % run, "0"])
                    #if p3 < 0: print >>sys.stderr, "p3 was terminated by signal", -retcode
            except OSError as e:
                print >>sys.stderr, "Execution failed:", e

                #            if os.path.isfile("/home/reinhold/totransfer/Run%06d.root" % run) and not os.path.isfile("%s/Run%06d.root" % (self.out_dir,run)):
                #try:
                #    #p4 = subprocess.call(["scp", "-r", "/home/reinhold/totransfer/Run%06d*.root" % run, "reinhol1@ds50srv01.fnal.gov:/scratch/darkside/reinhol1/SLAD/AmC/"]) #this typically won't work, since the kerberos authentification is not active.
                #    #if p4 < 0: print >>sys.stderr, "p4 was terminated by signal", -retcode	
                #    p5 = os.system("mv /home/reinhold/totransfer/Run%06d*.root %s" % (run, self.out_dir)) 
                #    if p5 < 0: print >>sys.stderr, "p5 was terminated by signal", -retcode
                #except OSError as e:
                #    print >>sys.stderr, "Execution failed:", e
            #if os.path.isfile("%s/Run%06d.root" % (self.out_dir,run)):
            #    self.check_TreeEntries(run)

        os.chdir(start_dir)



def main():
    rp = RunProcessing()
    rp.loop()
    #check_TreeEntries(14468)


if __name__ == "__main__":
	main()
