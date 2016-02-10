# This is a script to calculate the Zbi significance from the M.I. data card
# Data card is the txt output from fitSThists.py
# Usage        : python ZbiCalculator.py Data.root STMin_optimized.txt
# Output files : STMin_optimized.txt
# Input files  : Data.root_InclusiveX.txt 
# Martin Kwok 1/28/2016

from ROOT import *
from ROOT import TMath
from fitAndNormRanges import *
from sys import argv
import os
import math
import re 
def getPbi(n_on, n_off, tau):
	P_Bi = TMath.BetaIncomplete(1./(1.+tau),n_on,n_off+1)
	return (P_Bi)
def getZbi(n_on, n_off, tau):
	P_Bi = TMath.BetaIncomplete(1./(1.+tau),n_on,n_off+1)
	Z_Bi = TMath.Sqrt(2)*TMath.ErfInverse(1-2*P_Bi)
	return (Z_Bi)
def getXsec(signal , lookupfiles, modelClass):
	if(os.path.exists("./SignalFlatTuple/%s"%signal)and os.path.exists(lookupfiles)):
		if(modelClass=="BM"):
			Model=signal.split("_")[1]
			MD = signal.split("_")[3]
			MBH= signal.split("_")[4]
			n  = signal.split("_")[5]
			Found = False
			print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
			File = open(lookupfiles,"r")
			for line in File:
				path = line.split("\t")[0]
				xsec  = line.split("\t")[1]
				key = path.split("/")[9]
				if (key.split("_")[2]==MD and key.split("_")[3]==MBH and key.split("_")[4]==n and key.split("_")[0]==Model):
			#		print float(xsec)
					return float(xsec);
			if(not Found):
				print "Cannot find matching mass point"
		if(modelClass=="SB"):
			Model=signal.split("_")[1]
			MD   =signal.split("_")[2]
			MBH  =signal.split("_")[3]
			n    =signal.split("_")[4]
			Found = False
                        print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
                        File = open(lookupfiles,"r")
			for line in File:
				key = line.split(" ")[0]
				xsec= line.split(" ")[1]
				if (key.split("_")[1]==MD and key.split("_")[2]==MBH and key.split("_")[5]==n ):
					return float(xsec);
			if(not Found):
				print "Cannot find matching mass point"
	else:
		print "Signal files /look up file missing"
		return;

#### Main program ####

#Input constants :


IntLumi =  2263.5   	# Integrated Luminosity in pb^-1
eospath="/store/group/phys_exotica/BH_RunII/SB_Ntuple_Final/"
#XsecDB="BlackMax_xsection.txt"
XsecDB="SB_xsection_extra.txt"
ModelClass="SB"			#or BM
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
fitNormRanges.showFitRanges()
fitNormRanges.showNormRanges()

Output   = open("StOpt.txt","w")
Output.write("Model                         STMin(optimized)   Nmin      Zbi       Nsignal     xsection \n")

Input    = open("MassPointList.txt","r")

PlotFile = TFile.Open("PlotOut.root","recreate")
Plot     = TH1F("BH5_BM_MD4000_MBX_n6","BH5_BM_MD4000_MBX_n6",4,6000,9000)
for line in Input: 
	#signal="BlackMaxLHArecord_BH5_BM_MD4000_MBH8000_n6_NTuple.root"
	raw    = line.strip()
	signal = raw.replace("NTuple","FlatTuple")
	rawFile=eosHeader+eospath+"%s"%raw
	SignalOrgRoot=TFile.Open(rawFile)
	Ngen         =SignalOrgRoot.Get("bhana").Get("t").GetEntries()
	Xsec    = getXsec(signal,XsecDB,ModelClass)
	SignalFlatRoot=TFile("./SignalFlatTuple/%s"%signal)
	SignalDir =SignalFlatRoot.Get("ST")
	#nST = Best ST for a particular Nmin
	nST_list =[]
	nZbi_list =[]
	nYield_list =[]
	nMin_list =[]

	for i in range(2,11):
		stInc_data=DataDir.Get("stInc%02iHist"%i)
		stInc_sig =SignalDir.Get("stInc%02iHist"%i)
		weight    = IntLumi*Xsec/ Ngen
		stInc_sig.Scale(weight)
		Totalsig  = stInc_sig.Integral()
		print "Scaled Signal=%s  Xsec=%s pb Weight=%s" %( Totalsig, Xsec , IntLumi*Xsec/ Ngen) 
	
		# Calculate normalization factor for fitting functions
		lowerNormBin = stInc_data.GetXaxis().FindBin(float(fitNormRanges.getLowerNormBound("inc%i"%i)))
		upperNormBin = stInc_data.GetXaxis().FindBin(float(fitNormRanges.getUpperNormBound("inc%i"%i)))
		lowerNormEdge = stInc_data.GetXaxis().GetBinLowEdge(lowerNormBin)
		upperNormEdge = stInc_data.GetXaxis().GetBinLowEdge(upperNormBin)
		normBinTotal = 0;
		for normbin in range(lowerNormBin, upperNormBin):
			normBinTotal+=stInc_data.GetBinContent(normbin)
		normfactor =  (normBinTotal/bestfitN2.Integral(lowerNormEdge, upperNormEdge))*stInc_data.GetXaxis().GetBinWidth(upperNormBin) # this assumes all the bins have the same width.
		bestfitN2_Normalized = bestfitN2.Clone()
		bestfitN2_Normalized.SetParameter(0, bestfitN2.GetParameter(0)*normfactor)
	
		# Scan through ST
		Zbi_list   =[]
		STMin_list =[]
		Yield_list =[]
		for stmin in range(20, 80):
			sig=0
			startbin=stInc_sig.GetXaxis().FindBin(float(stmin*100))
			for stbin in range (startbin, stInc_sig.GetXaxis().GetNbins()):
				sig+=stInc_sig.GetBinContent(stbin)
			bkg= bestfitN2_Normalized.Integral(stmin*100, 9999999)/100
			# Uncertianty is obtained by  (Integral of upper limit - Integral of lower limit)
			fUp = 0
			fLow= 0
			for st    in range (stmin*100, Uncer.GetNbinsX()):
				fUp  += bestfitN2_Normalized.Eval(st)+ ( bestfitN2_Normalized.Eval(st)*Uncer.GetBinContent(st) )
				fLow += bestfitN2_Normalized.Eval(st)- ( bestfitN2_Normalized.Eval(st)*Uncer.GetBinContent(st) )
			deltaB = ((fUp - fLow)/100)/2
			tau = bkg/(deltaB**2)
			n_off=tau*bkg
			n_on =sig+bkg
			Zbi_list.append(getZbi(n_on,n_off,tau))
			STMin_list.append(stmin*100)
			Yield_list.append(sig)
			print "%s    %.3f   %.3f   %.3f   %s  %s   %.3f" % (stmin*100, sig, bkg, deltaB, getZbi(n_on,n_off,tau), getPbi(n_on,n_off,tau), sig/math.sqrt(bkg))
		#print "%s %.3f %.3f" % ( i, STMin_list[Zbi_list.index(max(Zbi_list))], max(Zbi_list))	
		nST_list.append( STMin_list[Zbi_list.index(max(Zbi_list))])
		nZbi_list.append(max(Zbi_list))
		nYield_list.append( Yield_list[ Zbi_list.index(max(Zbi_list))])
		nMin_list.append(i)
	MaxZbi= max(nZbi_list)
	STopt = nST_list[   nZbi_list.index( MaxZbi)]
	Yield = nYield_list[nZbi_list.index(MaxZbi)]
	Nopt  = nMin_list  [nZbi_list.index(MaxZbi)]
	Output.write("%s %s %s %s %s %s\n" % (signal, STopt, Nopt,MaxZbi, Yield, Xsec))
	#Plot.Fill(MBH,STopt)
	SignalFlatRoot.Close()
	SignalOrgRoot.Close()	
Plot.Write()
