# This is a script to calculate the Zbi significance from the M.I. data card
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


IntLumi =  2263.5   	# Integrated Luminosity in pb^-1
eospath="/store/group/phys_exotica/BH_RunII/BlackMax_NTuple/"
#eospath="/store/group/phys_exotica/BH_RunII/SB_Ntuple_Final/"
XsecDB="BlackMax_xsection.txt"
#XsecDB="SB_xsection_extra.txt"
MILimit="MILimits.txt"
ModelClass="BM"			#or BM
NScanMin  = 7
NScanMax  = 10
SaveDump = True
##############################

eosHeader="root://eoscms.cern.ch/"
data  ="all2015C+D_NoMetCut+NewMETFilter.root"
DataRoot  =TFile("%s"%data)
DataDir   =DataRoot.Get("ST")

FitN2Root =TFile("fitfunctions_ex2.root","READ")
UncerRoot =TFile("background_shape_uncertainty.root","READ")
bestfitN2 = FitN2Root.Get("fit0")
Uncer     = UncerRoot.Get("shape_unc")

fitNormRanges = FitAndNormRange("FitNormRanges.txt")
#fitNormRanges.showFitRanges()
#fitNormRanges.showNormRanges()

Output   = open("%s"%argv[2],"w")
Output.write("Model  MD   n  MBH | STMin   Nmin      Zbi      Nsignal     Xsec(fb)    Acept   StLimit   xsec(fb): Obs -2sig -1sig Exp +1sig +2sig  \n")

if SaveDump:
	Dump = open("%s.log"%argv[2].replace(".txt",""),"w")

MasspointListInput = open("%s"%argv[1],"r")
Nfiles   =0

PlotFile = TFile.Open("%s.root"%argv[2].replace(".txt",""),"recreate")
PlotSTopt  = TGraph()
PlotSTopt.SetTitle("Optimal ST v.s MBH")
PlotSTopt.SetName("STopt")
PlotZbiOpt = TGraph()
PlotZbiOpt.SetTitle("Best Zbi v.s. MBH")
PlotZbiOpt.SetName("ZbiOpt")

ZbiBest2D=[]
iFile=0
gStyle.SetOptStat(0)
for line in MasspointListInput: 
	Masspoint=[]
	MIdata   =[]
	#raw   ="BlackMaxLHArecord_BH5_BM_MD4000_MBH8000_n6_FlatTuple.root"
	#raw   ="BlackMaxLHArecord_SB_MD1640_MBH5500_n6_FlatTuple.root"
	signal    = line.strip()
	raw = signal.replace("FlatTuple","NTuple")
	rawFile=eosHeader+eospath+"%s"%raw
	SignalOrgRoot=TFile.Open(rawFile)
	Ngen         =SignalOrgRoot.Get("bhana").Get("t").GetEntries()
	Masspoint    = getXsec(signal,XsecDB,ModelClass)
	#Masspoint =[Model  MD   MBH n  Xsec]
	MBH     = Masspoint[2]
	Xsec    = Masspoint[4]
	SignalFlatRoot=TFile("./SignalFlatTuple/%s"%signal)
	SignalDir =SignalFlatRoot.Get("ST")
	#nST = Best ST for a particular Nmin
	nST_list =[]
	nZbi_list =[]
	nYield_list =[]
	nMin_list =[]
	if (ModelClass=="SB" or ModelClass=="BM"):
		PlotTitle = signal.strip("BlackMaxLHArecord_").strip("_FlatTuple.root")
	ZbiBest2D.append( TH2F("%s"%PlotTitle,"%s"%PlotTitle,9,2,11,60,2000,8000))
	#print "Processing %s"%signal
	if SaveDump:
		Dump.write("Processing %s\n"%signal)
	for i in range(NScanMin,NScanMax+1):
		
		stExc_data=DataDir.Get("stExc02Hist")
		stInc_data=DataDir.Get("stInc%02iHist"%i)
		stInc_sig =SignalDir.Get("stInc%02iHist"%i)
		weight    = IntLumi*Xsec/ Ngen
		stInc_sig.Scale(weight)
		Totalsig  = stInc_sig.Integral()
		if SaveDump:
			Dump.write("Nmin=%i Scaled Signal=%s  Xsec=%s pb Weight=%s\n" %(i, Totalsig, Xsec , IntLumi*Xsec/ Ngen) )
	
		# Calculate normalization factor for fitting functions
		lowerNormBin = stInc_data.GetXaxis().FindBin(float(fitNormRanges.getLowerNormBound("inc%i"%i)))
		upperNormBin = stInc_data.GetXaxis().FindBin(float(fitNormRanges.getUpperNormBound("inc%i"%i)))
		lowerNormEdge = stInc_data.GetXaxis().GetBinLowEdge(lowerNormBin)
		upperNormEdge = stInc_data.GetXaxis().GetBinLowEdge(upperNormBin)
		normBinTotal = 0;
		normBinN2    = 0
		for normbin in range(lowerNormBin, upperNormBin):
			normBinTotal+=stInc_data.GetBinContent(normbin)
			normBinN2   +=stExc_data.GetBinContent(normbin)
		normfactor =  (normBinTotal/bestfitN2.Integral(lowerNormEdge, upperNormEdge))*stInc_data.GetXaxis().GetBinWidth(upperNormBin) # this assumes all the bins have the same width.
		normfactor2 =  (normBinTotal/normBinN2) # this assumes all the bins have the same width.
		#print "normfactor_fit=%.2f   normfactor_hist=%.2f   diff =%.3f" % ( normfactor, normfactor2, abs(normfactor-normfactor2)/normfactor) 
		bestfitN2_Normalized = bestfitN2.Clone()
		bestfitN2_Normalized.SetParameter(0, bestfitN2.GetParameter(0)*normfactor)
		if SaveDump:
			Dump.write("STmin | Sig   bkg  | n_on n_off tau | Zbi   Pbi |  S/Sqrt(B)  Accptance\n")
		# Scan through ST
		Zbi_list   =[]
		STMin_list =[]
		Yield_list =[]
		for stmin in range(20, 80):
			if (stmin*100<upperNormEdge):
				continue
			sig=0
			n_off=0
			startbin=stInc_sig.GetXaxis().FindBin(float(stmin*100))
			for stbin in range (startbin, stInc_sig.GetXaxis().GetNbins()):
				sig+=stInc_sig.GetBinContent(stbin)
			#	n_off+=stExc_data.GetBinContent(stbin)
			n_off=bestfitN2.Integral(stmin*100,9999999)/100
			bkg= bestfitN2_Normalized.Integral(stmin*100, 9999999)/100
			#tau = bkg/(deltaB**2)
			tau = 1/normfactor
			n_on =sig+bkg
			Zbi  = getZbi(n_on,n_off,tau)
			Pbi  = getPbi(n_on,n_off,tau)
			Zbi_list.append(Zbi)
			STMin_list.append(stmin*100)
			Yield_list.append(sig)
			if SaveDump:
				Dump.write("%s |%.4f %.3f  | %.5f %.5f %.5f %.3f| %.5f %.5f |%.3f %.3f \n" % (stmin*100, sig, bkg,  n_on, n_off, tau, n_off/tau, Zbi, Pbi, sig/math.sqrt(bkg), sig/(IntLumi*Xsec)))
			ZbiBest2D[iFile].Fill(i, stmin*100, getZbi(n_on,n_off,tau))
		nST_list.append( STMin_list[Zbi_list.index(max(Zbi_list))])
		nZbi_list.append(max(Zbi_list))
		nYield_list.append( Yield_list[ Zbi_list.index(max(Zbi_list))])
		nMin_list.append(i)
	MaxZbi= max(nZbi_list)
	STopt = nST_list[   nZbi_list.index(MaxZbi)]
	Yield = nYield_list[nZbi_list.index(MaxZbi)]
	Nopt  = nMin_list  [nZbi_list.index(MaxZbi)]
	Acceptance = Yield / (IntLumi*Xsec)
	MInorm     = (IntLumi/1000)*Acceptance
	MIdata     = getMI(STopt, Nopt, MILimit)
	Output.write("%s %.0f %i %.0f %s %s %.3f %.6f %f %.5f" % (Masspoint[0], Masspoint[1],Masspoint[3],Masspoint[2], STopt, Nopt,MaxZbi, Yield, Xsec*1000, Acceptance))
	Output.write(" %s %.3f %.3f %.3f %.3f %.3f %.3f \n"%(MIdata[0], MIdata[1]/MInorm, MIdata[2]/MInorm ,MIdata[3]/MInorm,MIdata[4]/MInorm,MIdata[5]/MInorm,MIdata[6]/MInorm))
	PlotSTopt.SetPoint(PlotSTopt.GetN(),MBH,STopt)
	PlotZbiOpt.SetPoint(PlotZbiOpt.GetN(),MBH,MaxZbi)
	PlotFile.cd()	
	ZbiBest2D[iFile].Write()
	iFile=iFile+1
PlotFile.cd()	
PlotSTopt.Write()
PlotZbiOpt.Write()
