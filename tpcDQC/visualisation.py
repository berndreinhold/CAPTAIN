"""
produce visualisations of a data frame
Author : Bernd
Date : Jan. 6, 2015
"""
#import numpy as np
#import matplotlib.pyplot as plt
import math
import sys
import os
import re
import time
#import seaborn as sns

import html_output as ho

#see the output ROOT file of tpcDataQuality.exe
array_variables = [('baseline',1), ('pedestalRMS',1), ('shutoff',2), ('pulseCheckPositive',2), ('pulseCheckNegative',2), ('eventTiming',2)] #list the variables with the second argument being the importance of the variable: 1 is most important, 2nd is less, 0 is disabled
array_ch = [('wire',1), ('ch',2), ('conn_ch',2), ('disc_ch',2)]
#the product of the number in array_variables and array_ch is then the importance factor

class fig_summary():
    def __init__(self):
        self.run = -1 #run number
        self.mean = -1
        self.RMS = -1
        self.xvar = ""
        self.yvar = ""
        self.label = ""
        self.comment = ""
        self.fig_path = "" #fig_path + fig_rel_path is where the figure is copied to physically
        self.fig_rel_path = "" #contains the relative path written to HTML and the name of the figure. It could be: figures/fig_name.png or just fig_name.png

class html_picture_summary_root(ho.html_picture_summary):
    #def __init__(self, of_name, CSS=[]):
    #    ho.html_picture_summary.__init__(self, of_name, CSS)

    def body_content(self, summary_struct, title, level=1, append=True, type="images"): #level=1:<h1>, level=2:<h2>, level=3:<h3>
        """
        summary_struct is essentially a list of images or a table of contents that are turned into valid HTML
        """
        l = []
        #l[len(l):] = ['<h%d id="%s" class="headers">%s<a href="#%s" class="permalink">&para;</a><a href="#bottom" class="topbottom">bottom</a><a href="#top" class="topbottom">top</a></h%d>' % (level, "_".join(title.split()), title, "_".join(title.split()),level)] #http://www.tedmontgomery.com/tutorial/HTMLchrc.html
        match = re.findall(r'run ([0-9]{4})', title)
        if match:
            l[len(l):] = ['<h%d id="%s" class="headers">%s (%s, <a href="tpcDQC_%s.html">all plots for %s</a>)<a href="#%s" class="permalink">&para;</a><a href="#top" class="topbottom">top</a></h%d>' % (level, "_".join(title.split()), title, "[date]", "_".join(title.split()), title, "_".join(title.split()),level)] #http://www.tedmontgomery.com/tutorial/HTMLchrc.html
        else:
            l[len(l):] = ['<h%d id="%s" class="headers">%s<a href="#%s" class="permalink">&para;</a></h%d>' % (level, "_".join(title.split()), title, "_".join(title.split()),level)] #http://www.tedmontgomery.com/tutorial/HTMLchrc.html

        if summary_struct:
            if type == "images":
                for s in summary_struct:
                    #l[len(l):] = ['<div class="Fig_BasicInfo">']
                    l[len(l):] = ['<div>']
                    #l[len(l):] = ["<h%d>%s</h%d>" % (level+2, str(s.label), level+2)]
                    l[len(l):] = ["<h%d>%s</h%d>" % (level+2, str(s.label), level+2)]
                    #l[len(l):] = ["<div>%s</div>" % str(s.fig_rel_path)]
                    l[len(l):] = ['<img src="%s" alt="[no figure]"/>' % str(s.fig_rel_path)] #html code
                    l[len(l):] = ["<div>%s</div>" % str(s.comment)]
                    l[len(l):] = ['</div>']
            elif type == "toc_runs":
                l[len(l):] = ['<ol>']
                for s in summary_struct:
                    l[len(l):] = ['<li><a href="#%s">%s</a> (%s, <a href="tpcDQC_%s.html">all plots for %s</a>)</li>' %("_".join(s[0].split()),s[0],s[1],"_".join(s[0].split()),s[0])] #s[0]: "run 5213", s[1]: [its creation date]
                l[len(l):] = ['</ol>']
            elif type == "toc_vars":
                l[len(l):] = [', '.join(['<a href="tpcDQC_%s.html">%s</a>' % (s,s) for s in summary_struct])] #s: "tpc_DQC_FebMar2016.html"

            elif type == "toc_plain":
                l[len(l):] = ['<ul>']
                for s in summary_struct:
                    l[len(l):] = ['<li><a href="%s">%s</a></li>' % (s,s)] #s: "tpc_DQC_FebMar2016.html"
                l[len(l):] = ['</ul>']
        if not append: self._body_content = ""
        self._body_content += "\n".join(l)

 
class plot_summary():
    """
    this class is very specifically adjusted to a certain analysis task (different for any dataset that needs to be shown)
    """

    def __init__(self, html_dir="./", rel_dir=""):
        if html_dir[-1]!="/": html_dir+="/"
        self._output_dir = html_dir #where the HTML file is being stored
        if len(rel_dir)>0 and rel_dir[-1]!="/": rel_dir+="/"
        self._rel_dir = rel_dir #the PNGs and the CSS are being stored in self._output_dir + self._rel_dir
        if not os.path.exists(self._output_dir + self._rel_dir): os.makedirs(self._output_dir + self._rel_dir)
        self.list_fig_summary = []
        self.run_list = []

    def perRun(self, run, varlist=[]):
        """for each variable get the variable path and store some text"""
        #print(self._df[var_name].dtype)
        var_name = "baseline_wire_run%d" % run

        for var in varlist:
                var_name = "%s_run%d" % (var,run)
                fs = fig_summary()   #fs.mean = average(df[var_name])
                fs.xvar = var_name
                fs.label = var_name
                
                print(fs.label)
                fs.fig_path = self._output_dir
                fs.fig_rel_path = self._rel_dir + var_name + ".png"
                
                self.list_fig_summary.append(fs)
                
                #plt.show()
                #print("figure made: ", fs.fig_path + fs.fig_rel_path)
                #plt.savefig(fs.fig_path + fs.fig_rel_path)


    def perRun_Priority(self, run, priority_thres):
        varlist = []
        for var, priority_var in array_variables:
            if var == "eventTiming":
                #varlist.append(var + ("_run%d" % run))
                priority = priority_var
                if priority> priority_thres: continue
                varlist.append(var)
                continue
            for ch, priority_ch in array_ch:
                priority = priority_var * priority_ch
                if priority> priority_thres: continue
                #varlist.append(var + "_" + ch + ("_run%d" % run))
                varlist.append(var + "_" + ch)
        if varlist: self.perRun(run, varlist)
        else: "varlist is empty, you might want to change the priority threshold (%d)" % priority_thres


    def perRun__xxx(self, run):
        """for each variable make a PNG and store some text"""
        #print(self._df[var_name].dtype)
        fs = fig_summary()   #fs.mean = average(df[var_name])
        fs.xvar = var_name
        fs.label = var_name

        buffer = []


        fs.xvar = var_name
        fs.label = var_name
        print(fs.label)
        fs.fig_path = self._output_dir
        fs.fig_rel_path = self._rel_dir + var_name + ".png"
        
        self.list_fig_summary.append(fs)

        #plt.show()
        print("figure made: ", fs.fig_path + fs.fig_rel_path)
        plt.savefig(fs.fig_path + fs.fig_rel_path)

    def listruns(self, dir_, bAppend=False):
        if len(self.run_list) and not bAppend:
            #self.run_list.clear()
            self.run_list[:] = [] 
        for dirname, dirnames, filenames in os.walk(dir_):
            for filename in filenames:
                match = re.findall(r'(tpcDQC_([0-9]{4}).root)', filename)
                print(filename, match)
                if match: self.run_list.append((int(match[0][1]),time.ctime(os.path.getctime(dirname + match[0][0]))))

        self.run_list.sort(key=lambda x: x[0])
        #print(self.run_list)

    def produceAllPlots(self, in_dir="/home/reinhold/data/CAPTAIN/", out_dir="html/figures/"):
        self.listruns(in_dir)

        for run, ctime_ in self.run_list:
            buffer = "root -q -b -l 'producePlots.C(%d, \"%s\", \"%s\")'" % (run, in_dir, out_dir)
            os.system(buffer)        #out_dir has to be a relative path, relative to input-dir, these are concatenated in producePlots.C

        #produce also list of creation dates from run list

    def __del__(self):
        print(self.list_fig_summary)


def SummaryWebsite(plot_sum):

    #output_filepath = "/home/reinhold/data/CAPTAIN/html/"
    output_filepath = "/global/project/projectdirs/captain/data/2016/tpcDQC/html/"
    output_filename = "tpcDQC_FebMar2016.html"
    os.system("cd %s; ln -s tpcDQC_FebMar2016.html index.html; cd %s;" % (output_filepath, os.getcwd()))
    html = html_picture_summary_root(output_filename, output_filepath, ["basic_style.css"])

    if 1:
        
        #plot_sum.listruns("/home/reinhold/data/CAPTAIN/")
        plot_sum.listruns("/global/project/projectdirs/captain/data/2016/tpcDQC/")
        
        runlist_ = [("run %d" % run[0], run[1]) for run in plot_sum.run_list]
        html.body_content([], "table of contents", 2, True)
        html.body_content(runlist_, "per run", 3, True, "toc_runs")
        #html.body_content(runlist_, "per variable", 3, True, "toc")

        varlist = []
        for var2, priority_var in array_variables:
            if var2 == "eventTiming":
                varlist.append(var2)
                continue
            for ch, priority_ch in array_ch:
                #ignore priority argument, produce all:
                varlist.append(var2 + "_" + ch)
        varlist.sort()
        print(varlist)
        html.body_content(varlist, "per variable", 3, True, "toc_vars")
        
        html.body_content([], "plots", 2, True) #produces just a header line
        for run in plot_sum.run_list:
            plot_sum.perRun_Priority(run[0], 1) #the latter argument is a priority threshold: the lower this threshold, the fewer plots are produced -> this allows to select only the most critical plots
            html.body_content(plot_sum.list_fig_summary, "run %d" % run[0], 3, True)
            #plot_sum.list_fig_summary.clear()
            plot_sum.list_fig_summary[:] = []

    html.loop("February/March 2016 - TPC Data Quality Control", "most critical plots for all runs are shown below. Program to produce these: TPCDATAQUALITY.exe to produce histograms from ubdaq raw data, a ROOT plot script to produce PNG and a python script to produce the HTML. This set of scripts is run with a cronjob on PDSF every 30 min. (Yujing Sun, Bernd Reinhold @ UHawaii, Feb. 2016)") #the second argument is a comment field printed at the top


def OneRunAllPlots(plot_sum, run):
    #output_filepath = "/home/reinhold/data/CAPTAIN/html/"
    output_filepath = "/global/project/projectdirs/captain/data/2016/tpcDQC/html/"
    output_filename = "tpcDQC_run_%d.html" % run
    html = html_picture_summary_root(output_filename, output_filepath, ["basic_style.css"])


    if 1:
        
        runlist_ = ["tpcDQC_run_%d.html" % x[0] for x in plot_sum.run_list]
        html.body_content(["tpcDQC_FebMar2016.html"], "table of contents", 2, True, "toc_plain")
        html.body_content(runlist_, "per run", 3, True, "toc_plain")
        #html.body_content(runlist_, "per variable", 3, True, "toc")
        varlist = []
        for var2, priority_var in array_variables:
            if var2 == "eventTiming":
                varlist.append(var2)
                continue
            for ch, priority_ch in array_ch:
                #ignore priority argument, produce all:
                varlist.append(var2 + "_" + ch)
        varlist.sort()
        html.body_content(varlist, "per variable", 3, True, "toc_vars")


        varlist = []
        for var, priority_var in array_variables:
            if var == "eventTiming":
                varlist.append(var)
                continue
            for ch, priority_ch in array_ch:
                #ignore priority argument, produce all:
                varlist.append(var + "_" + ch)
        varlist.sort()

        ###print(type(run))
        plot_sum.perRun(run, varlist)
        html.body_content(plot_sum.list_fig_summary, "plots", 2, True) #produces just a header line

        #html.body_content(plot_sum.list_fig_summary, "run %d" % run, 3, True)
        #plot_sum.list_fig_summary.clear()
        plot_sum.list_fig_summary[:] = []

    html.loop("Run %d - TPC Data Quality Control" %run, "all variables for run %d are shown below." %run) #the second argument is a comment field printed at the top

def OneVarAllRuns(plot_sum, var):

    #output_filepath = "/home/reinhold/data/CAPTAIN/html/"
    output_filepath = "/global/project/projectdirs/captain/data/2016/tpcDQC/html/"
    output_filename = "tpcDQC_%s.html" % var
    html = html_picture_summary_root(output_filename, output_filepath, ["basic_style.css"])

    if 1:
        
        #plot_sum.listruns("/home/reinhold/data/CAPTAIN/")
        plot_sum.listruns("/global/project/projectdirs/captain/data/2016/tpcDQC/")
        
        runlist = [("run %d" % run[0], run[1]) for run in plot_sum.run_list]
        html.body_content(["tpcDQC_FebMar2016.html"], "table of contents", 2, True, "toc_plain")
        html.body_content(runlist, "per run", 3, True, "toc_runs")

        varlist = []
        for var2, priority_var in array_variables:
            if var2 == "eventTiming":
                varlist.append(var2)
                continue
            for ch, priority_ch in array_ch:
                #ignore priority argument, produce all:
                varlist.append(var2 + "_" + ch)
        varlist.sort()
        html.body_content(varlist, "per variable", 3, True, "toc_vars")
        #html.body_content(runlist_, "per variable", 3, True, "toc")
        
        html.body_content([], "plots", 2, True) #produces just a header line
        for run in plot_sum.run_list:
            plot_sum.perRun(run[0], [var]) #the latter argument is a priority threshold: the lower this threshold, the fewer plots are produced
            html.body_content(plot_sum.list_fig_summary, "run %d" % run[0], 3, True)
            #plot_sum.list_fig_summary.clear()
            plot_sum.list_fig_summary[:] = []

    html.loop("%s - February/March 2016 - TPC Data Quality Control" % var, "%s for all runs are shown below" % var) #the second argument is a comment field printed at the top

    

def main():
    #output_filepath = "/home/reinhold/data/CAPTAIN/html/"
    output_filepath = "/global/project/projectdirs/captain/data/2016/tpcDQC/html/"
    plot_sum = plot_summary(output_filepath, "figures/")
    #plot_sum.produceAllPlots("/global/project/projectdirs/captain/data/2016/tpcDQC/")
    #SummaryWebsite(plot_sum)
    #plot_sum.listruns("/home/reinhold/data/CAPTAIN/")
    plot_sum.listruns("/global/project/projectdirs/captain/data/2016/tpcDQC/")
    for run, ctime_ in plot_sum.run_list:
        OneRunAllPlots(plot_sum, run)

    varlist = []
    for var, priority_var in array_variables:
        if var == "eventTiming":
            varlist.append(var)
            continue
        for ch, priority_ch in array_ch:
            #ignore priority argument, produce all:
            varlist.append(var + "_" + ch)
    varlist.sort()
    for var in varlist:
        OneVarAllRuns(plot_sum, var)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
