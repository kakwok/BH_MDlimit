# This is a script to calculate the Zbi significance from the M.I. data card
#
# In v5, MI limit is minimized. No Zbi is used.
#
# Data card is the txt output from fitSThists.py
# Usage        : python ZbiCalculator_v3.py Masspointlist.txt Output.txt
# Output files : STMin_optimized.txt STmin_optimized.root
# Input files  : Data.root_InclusiveX.txt 
# Martin Kwok 1/28/2016

from ROOT import *
from ROOT import TMath
from fitAndNormRanges import *
from sys import argv
import os
import math
import re
from GetXsec import * 
from GetMI import * 

def getPbi(n_on, n_off, tau):
	P_Bi = TMath.BetaIncomplete(1./(1.+tau),n_on,n_off+1)
	return (P_Bi)
def getZbi(n_on, n_off, tau):
	P_Bi = TMath.BetaIncomplete(1./(1.+tau),n_on,n_off+1)
	Z_Bi = TMath.Sqrt(2)*TMath.ErfInverse(1-2*P_Bi)
	return (Z_Bi)
#### Main program ####

#Input constants :


#IntLumi =  2263.5   	# Integrated Luminosity in pb^-1 for 2015
IntLumi =  36500.0   	# Integrated Luminosity in pb^-1


#eospath="/store/group/phys_exotica/BH_RunII/QBH_RS1_NTuple/"
#eospath="/store/group/phys_exotica/BH_RunII/QBH_ADD_NTuple/"
#eospath="/store/group/phys_exotica/BH_RunII/SB_Ntuple_Final/"
#eospath="/store/group/phys_exotica/BH_RunII/BlackMax_NTuple/"
eospath="" 				#Use empty path for newer FlatTuple with Ngen information
#XsecDB="QBH_RS1_xsection.txt"
#XsecDB="QBH_ADD_xsection.txt"
#XsecDB="SB_xsection_extra.txt"
#XsecDB="BlackMax_xsection.txt"
#XsecDB="Charybdis_xsection_2016.txt"
#XsecDB="Charybdis_BH10_xsection.txt"
#XsecDB="Sphaleron_xsection.txt"
XsecDB="Charybdis_SB_xsection_newMD.txt"
MILimit="MILimit_2016.txt"

ModelClass="SB"				#or BM, BM_full, SB, QBH_ADD, QBH_RS1, CYBD, Sphaleron
NScanMin  = 3
NScanMax  = 11
SaveDump = True
##############################

eosHeader="/eos/cms"
#data  ="/afs/cern.ch/user/k/kakwok/work/public/Blackhole/BH2016/flatTuple/BHflatTuple_2016BtoH_CleanTail_70GeV.root"
#data  ="all2015C+D_NoMetCut+NewMETFilter.root"
data  ="./mBH_Exc9/70GeV/BHflatTuple_2016BtoH_preApprove_70GeV.root"
DataRoot  =TFile("%s"%data)
DataDir   =DataRoot.Get("ST")

fitNormRanges = FitAndNormRange("FitNormRanges_2016.txt")
#fitNormRanges = FitAndNormRange("FitNormRanges.txt")

Output   = open("%s"%argv[2],"w")
Output.write("Model  MD   n  MBH | STMin   Nmin  | ExpLimit     Nsignal    Acept   StLimit  Xsec(fb) |  xsec(fb): Obs -2sig -1sig Exp +1sig +2sig  \n")

if SaveDump:
	Dump = open("%s.log"%argv[2].replace(".txt",""),"w")

MasspointListInput = open("%s"%argv[1],"r")
Nfiles   =0

PlotFile = TFile.Open("%s.root"%argv[2].replace(".txt",""),"recreate")

LimitBest2D=[]
iFile=0
iMissing=0
MissingPoints=[]
gStyle.SetOptStat(0)
for PathAndFile in MasspointListInput:
	if PathAndFile[0]=="#":
		print "Skipping %s"%PathAndFile
		continue 
	Masspoint=[]
	MIdata   =[]
	#raw   ="BlackMaxLHArecord_BH5_BM_MD4000_MBH8000_n6_FlatTuple.root"
	#raw   ="BlackMaxLHArecord_SB_MD1640_MBH5500_n6_FlatTuple.root"
	PathAndFile      = PathAndFile.strip()
	signal    = PathAndFile.split("/")[2]
	raw       = signal.replace("FlatTuple","NTuple")
	rawFile   = eosHeader + eospath + "%s"%raw
	SignalFlatRoot  = TFile.Open("./%s"%PathAndFile)
	SignalDir       = SignalFlatRoot.Get("ST")
	#print " Opening FlatTuple file: %s" % PathAndFile
	#print " Opening RawTuple file: %s" % rawFile
	if(os.path.exists(rawFile)):
		SignalOrgRoot=TFile.Open(rawFile)
		Ngen         =SignalOrgRoot.Get("bhana").Get("t").GetEntries()
	elif "Ngen" == SignalFlatRoot.Get("Ngen").GetName():
		Ngen         = SignalFlatRoot.Get("Ngen").GetBinContent(1)
	else:
		print "Cannot find Ngen in original NTuple in eos Or Ngen histogram in SignalFlatTuple."
	Masspoint    = getXsec(PathAndFile,XsecDB,ModelClass)
	#Masspoint =[Model  MD   MBH n  Xsec]
	#print Masspoint
	MBH     = Masspoint[2]
	Xsec    = Masspoint[4]
	#nST = Best ST for a particular Nmin
	nST_list =[]
	nExpLimit_list =[]
	nYield_list =[]
	nMin_list =[]
	PlotTitle = "%s_%s_%s_%s" %(Masspoint[0],Masspoint[1],Masspoint[2],Masspoint[3])
	LimitBest2D.append( TH2F("%s"%PlotTitle,"%s"%PlotTitle,9,2,11,60,2000,8000))
	#print "Processing %s"%signal
	if SaveDump:
		Dump.write("Processing %s\n"%signal)
	for i in range(NScanMin,NScanMax+1):
		
		stInc_data=DataDir.Get("stInc%02iHist"%i)
		stInc_sig =SignalDir.Get("stInc%02iHist"%i)
		weight    = IntLumi*Xsec/ Ngen
		stInc_sig.Scale(weight)
		Totalsig  = stInc_sig.Integral()
		if SaveDump:
			Dump.write("Nmin=%i Scaled Signal=%s  Xsec=%s pb Weight=%s\n" %(i, Totalsig, Xsec , IntLumi*Xsec/ Ngen) )
		lowerNormBin = stInc_data.GetXaxis().FindBin(float(fitNormRanges.getLowerNormBound("inc%i"%i)))
		upperNormBin = stInc_data.GetXaxis().FindBin(float(fitNormRanges.getUpperNormBound("inc%i"%i)))
		lowerNormEdge = stInc_data.GetXaxis().GetBinLowEdge(lowerNormBin)
		upperNormEdge = stInc_data.GetXaxis().GetBinLowEdge(upperNormBin)

		# Calculate normalization factor for fitting functions
		if SaveDump:
			Dump.write("Nmin STmin | Sig   Accptance | Expected limit \n")
		# Scan through ST
		ExpLimit_list   =[]
		Zbi_list   =[]
		STMin_list =[]
		Yield_list =[]
		for stmin in range(20, 80):
			if (stmin*100<=upperNormEdge):
				continue
			sig=0.0
			startbin=stInc_sig.GetXaxis().FindBin(float(stmin*100))
			for stbin in range (startbin, stInc_sig.GetXaxis().GetNbins()):
				sig+=stInc_sig.GetBinContent(stbin)
			if sig==0.0:
				continue
			Acc        = float(sig / (IntLumi*Xsec))
			minorm     = float((IntLumi/1000.)*Acc)
			midata     = getMI(stmin*100, i , MILimit)

			#print "%s %.3f %.3f %.3f" % (stmin*100, sig, Acc, minorm)
			#ObsLimit = midata[1]/minorm
			ExpLimit = midata[4]/minorm
			ExpLimit_list.append(ExpLimit)
			STMin_list.append(stmin*100)
			Yield_list.append(sig)
			if SaveDump:
				Dump.write("%i %s %.3f %.3f %.3f \n" % (i, stmin*100, sig, Acc , ExpLimit))
			LimitBest2D[iFile].Fill(i, stmin*100, ExpLimit)
		if not ExpLimit_list:
			continue
		nExpLimit_list.append( min(ExpLimit_list) )
		nST_list.append( STMin_list[ExpLimit_list.index(min(ExpLimit_list))])
		nYield_list.append( Yield_list[ ExpLimit_list.index(min(ExpLimit_list))])
		nMin_list.append(i)
	if not nExpLimit_list:
		continue
	MinLimit= min(nExpLimit_list)
	STopt = nST_list[   nExpLimit_list.index(MinLimit)]
	Yield = nYield_list[nExpLimit_list.index(MinLimit)]
	Nopt  = nMin_list  [nExpLimit_list.index(MinLimit)]

	if SaveDump:
		Dump.write("For signal=%s: \n"   % signal)
		Dump.write("nSTlist = %s: \n"    % nST_list)
		Dump.write("nMinlist = %s: \n"   % nMin_list)
		Dump.write("nMinlist = %s: \n"   % nExpLimit_list)

	Acceptance = Yield / (IntLumi*Xsec)
	MInorm     = (IntLumi/1000)*Acceptance
	MIdata = getMI(STopt,Nopt,MILimit)
	if MIdata[1]==0:
		iMissing=iMissing+1
		MissingPoints.append("%s %.0f %i %.0f %s %s "%(Masspoint[0], Masspoint[1],Masspoint[3],Masspoint[2], STopt, Nopt))
	Output.write("%s %.0f %i %.0f    %s %s    %.3f %.3f %s %.5f %f" % (Masspoint[0], Masspoint[1],Masspoint[3],Masspoint[2], STopt, Nopt, MinLimit, Yield, MIdata[0],Acceptance,Xsec*1000))
	Output.write("      %.3f %.3f %.3f %.3f %.3f %.3f \n"%( MIdata[1]/MInorm, MIdata[2]/MInorm ,MIdata[3]/MInorm,MIdata[4]/MInorm,MIdata[5]/MInorm,MIdata[6]/MInorm))
	PlotFile.cd()	
	LimitBest2D[iFile].Write()
	iFile=iFile+1
print " Missing %s points in MI limit. Printing as follows:"%iMissing
Dump.write(" Missing %s points in MI limit. Printing as follows:\n"%iMissing)
for line in MissingPoints:
	print line
	Dump.write("%s\n"%line)
