import os
import glob

#/mnt/hadoop/store/user/kakwok/QCD/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/BHnTuples_QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/170508_161813/0000/ntuple_output_100.root
Topdir = "/mnt/hadoop/users/mkwok/BH/QCD"
#dataSetNames =[]
#dataSetNames.append("QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8")
#dataSetNames.append("QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8")

dataSetNames = glob.glob("%s/*.root"%Topdir)
outputTag = "Moriond17_May11"

for dataSetName in dataSetNames:
	datasetTag = dataSetName.split("/")[-1].replace(".root","").replace("BHnTuple_","")
	cmd  = "root -l -q '../BHflatTuplizer.cc+(\"%s\",\"BHflatTuple_%s_%s_%sGeV.root\",\"../empty.txt\",false,%s)'"%(dataSetName,datasetTag,outputTag,70,70.0)
	cmd += ">> %s_flatuplize.log &"%dataSetName.split("/")[-1].replace(".root","") 
	print cmd
	#os.system(cmd)
