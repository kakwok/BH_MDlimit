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

def getZbi(n_on, n_off, tau):
	P_Bi = TMath.BetaIncomplete(1./(1.+tau),n_on,n_off+1)
	Z_Bi = TMath.Sqrt(2)*TMath.ErfInverse(1-2*P_Bi)
	return (Z_Bi)
def getXsec(signal , lookupfiles):
	if(os.path.exists("./SignalFlatTuple/%s"%signal)and os.path.exists(lookupfiles)):
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
			print "Cannot find matching model"
	else:
		print "Signal files /look up file missing"
		return;

#### Main program ####


signal="BlackMaxLHArecord_BH5_BM_MD4000_MBH5000_n6_FlatTuple.root"
raw   =signal.replace("FlatTuple","NTuple")
data  ="all2015C+D_NoMetCut+NewMETFilter.root"

XsecDB="BlackMax_xsection.txt"
Xsec    = getXsec(signal,XsecDB)
IntLumi = 2.3   	# Integrated Luminosity in pb^-1

SignalOrgRoot=TFile.Open("root://eoscms.cern.ch//store/group/phys_exotica/BH_RunII/BlackMax_NTuple/%s"%raw)
Ngen         =SignalOrgRoot.Get("bhana").Get("t").GetEntries()

SignalFlatRoot=TFile("./SignalFlatTuple/%s"%signal)
SignalDir =SignalFlatRoot.Get("ST")
DataRoot  =TFile("%s"%data)
DataDir   =DataRoot.Get("ST")
FitN2Root =TFile("fitfunctions_ex2.root")
FitN3Root =TFile("fitfunctions_ex3.root")
UncerRoot =TFile("background_shape_uncertainty.root")
bestfitN2 = FitN2Root.Get("fit0")
bestfitN3 = FitN3Root.Get("fit0")
Uncer     = UncerRoot.Get("shape_unc")

fitNormRanges = FitAndNormRange("FitNormRanges.txt")
fitNormRanges.showFitRanges()
fitNormRanges.showNormRanges()

Output   = open("StOpt.txt","w")
Output.write("N_min    STMin(optimized)    Zbi     Acceptance    xsection \n")

for i in range(2,11):
	stInc_data=DataDir.Get("stInc%02iHist"%i)
	stInc_sig =SignalDir.Get("stInc%02iHist"%i)
	print i 
	weight    = IntLumi*Xsec/ Ngen
	stInc_sig.Scale(weight)
	Totalsig  = stInc_sig.Integral()
	print "%s %s %s" %( Totalsig, Xsec , IntLumi*Xsec/ Ngen) 

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
	Zbi_list = []
	STMin_list=[]
	for stmin in range(30, 80):
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
		print "%s    %.3f   %.3f   %.3f   %.3f  %.2f" % (stmin*100, sig, bkg, deltaB, getZbi(n_on,n_off,tau), sig/Totalsig)
	#print "%s %.3f %.3f" % ( i, STMin_list[Zbi_list.index(max(Zbi_list))], max(Zbi_list))	



