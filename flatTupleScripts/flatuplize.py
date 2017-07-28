import os
import glob
import time

#Topdir = "/eos/cms/store/user/kakwok/BH/NTuple/QCD/"
Topdir = "/eos/cms/store/user/bravo/bhSphAna/qcd/"

isFromCameron = True

#dataSetNames = glob.glob("%s/*.root"%Topdir)  # old style trees
ptBins = glob.glob("%s*"%Topdir)
dataSetNames  = []
for ptBin in ptBins:
    dataSetNames.append( ptBin + "/trees/*.root")
#    dataSetNames = /eos/cms/store/user/bravo/bhSphAna/qcd/pt120to170/trees/*.root
outputTag = "Moriond17_May11"
pTcuts    = [30,50,70,90] 

for pTcut in pTcuts:
    for dataSetName in dataSetNames:
        #datasetTag = dataSetName.split("/")[-1].replace(".root","").replace("BHnTuple_","")
        datasetTag =  dataSetName.split("/")[-4]+"_"+dataSetName.split("/")[-3]
        cmd  = "root -l -q '../BHflatTuplizer.cc+(\"%s\",\"./%sGeV/BHflatTuple_%s_%s_%sGeV.root\",\"../empty.txt\",false,%s)'"%(dataSetName,pTcut,datasetTag,outputTag,pTcut,float(pTcut))
        cmd += ">> %s_flatuplize.log &"%(datasetTag) 
        print cmd
        os.system(cmd)
        time.sleep(0.5)
    time.sleep(0.5)
    #os.system(cmd)
