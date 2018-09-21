from ROOT import *
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 0
CMS_lumi.lumiTextSize     = 0.65
#CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
iPeriod = 4

#txt = open("../../StOpt_Sphaleron.txt")
txt = open("../../StOpt_Sphaleron_CT10.txt")
#txt = open("../../StOpt_test.txt")
g_spha  = TGraph()
g_spha_exp  = TGraph()
g_spha_OneSig  = TGraphAsymmErrors()
g_spha_TwoSig  = TGraphAsymmErrors()
#CT10 xsec
xsec = {8.0:121.127,9.0:10.0507,10.0:0.505661}
#CT14nnlo xsec
#xSec = {8.0:99.17  ,9.0:7.3    ,10.0:0.268}
for line in txt:
    line = line.strip().split()
    if ("SPHA" in line[0]):
        E_spha  = float(line[1])
        StMin   = float(line[4])
        NMin    = float(line[5])
        exp_limit=float(line[6])
        exp_TwoSigDown=float(line[12])
        exp_OneSigDown=float(line[13])
        limit         =float(line[11])
        exp_OneSigUp  =float(line[15])
        exp_TwoSigUp  =float(line[16])
        PEF =  limit/xsec[E_spha]
        PEF_exp =  exp_limit/xsec[E_spha]
        PEF_exp_TwoSigDown =  exp_TwoSigDown/xsec[E_spha]
        PEF_exp_OneSigDown =  exp_OneSigDown/xsec[E_spha]
        PEF_exp_TwoSigUp =  exp_TwoSigUp/xsec[E_spha]
        PEF_exp_OneSigUp =  exp_OneSigUp/xsec[E_spha]


        print "%s   xsec_limit = %.3f  PEF_limit=%.3f expected= [%.4f, %.4f, %.4f, %.4f, %.4f] "%(E_spha,limit, PEF,PEF_exp_TwoSigDown, PEF_exp_OneSigDown, PEF_exp,PEF_exp_OneSigUp,PEF_exp_TwoSigUp)
        g_spha.SetPoint(g_spha.GetN(),E_spha, PEF)
        g_spha_exp.SetPoint(g_spha_exp.GetN(),E_spha, PEF_exp)

        g_spha_OneSig.SetPoint(     g_spha_OneSig.GetN(),E_spha, PEF_exp)
        g_spha_OneSig.SetPointError(g_spha_OneSig.GetN()-1,0,0, PEF_exp-PEF_exp_OneSigDown, PEF_exp_OneSigUp - PEF_exp)

        g_spha_TwoSig.SetPoint(     g_spha_TwoSig.GetN(),E_spha, PEF_exp)
        g_spha_TwoSig.SetPointError(g_spha_TwoSig.GetN()-1,0,0, PEF_exp-PEF_exp_TwoSigDown, PEF_exp_TwoSigUp - PEF_exp)
        #print "1sig %.3f %.3f %.6f %.6f "%(E_spha,PEF_exp, float(PEF_exp-PEF_exp_OneSigDown), float(PEF_exp_OneSigUp - PEF_exp))
        #print "2sig %.3f %.3f %.6f %.6f "%(E_spha,PEF_exp, float(PEF_exp-PEF_exp_TwoSigDown), float(PEF_exp_TwoSigUp - PEF_exp))

g_spha_exp.SetLineColor(kBlack)
g_spha_exp.SetLineStyle(2)
g_spha_exp.SetMarkerSize(0)
g_spha_exp.SetMarkerStyle(0)

g_spha_OneSig.SetLineColor(kBlack)
g_spha_OneSig.SetFillColor(kGreen+1)
g_spha_OneSig.SetLineStyle(2)
g_spha_OneSig.SetLineWidth(2)
g_spha_OneSig.SetMarkerStyle(0)
g_spha_TwoSig.SetLineColor(kBlack)
g_spha_TwoSig.SetFillColor(kOrange)
g_spha_TwoSig.SetLineStyle(2)
g_spha_TwoSig.SetLineWidth(2)
g_spha_TwoSig.SetMarkerStyle(0)


g_spha.SetLineColor(kBlack)
g_spha.SetMarkerColor(kBlack)
g_spha.SetMarkerStyle(20)
g_spha.SetMarkerSize(0.7)
#g_spha.SetFillColor(kRed)
#g_spha.SetLineWidth(2002)
#g_spha.SetFillStyle(3004)

mg = TMultiGraph()
mg.Add(g_spha_TwoSig)
mg.Add(g_spha_OneSig)
mg.Add(g_spha)
mg.Add(g_spha_exp)

leg = TLegend(0.3,0.71,0.7,0.91)
leg.AddEntry(g_spha,"Observed","pl")
#leg.AddEntry(g_spha_exp,"Expected limit","pl")
leg.AddEntry(g_spha_OneSig,"68% expected","lf")
leg.AddEntry(g_spha_TwoSig,"95% expected","lf")
leg.SetTextSize(0.03)

mg.Draw("ALP E3")
mg.GetXaxis().SetTitleSize(0.04)
mg.GetYaxis().SetTitleSize(0.04)
mg.GetXaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitleOffset(1.25)
mg.GetXaxis().SetLabelSize(0.04)
mg.GetYaxis().SetLabelSize(0.04)
mg.GetXaxis().SetTitle("E_{sph} [TeV]")
mg.GetXaxis().SetLimits(8.0,10.0)
mg.GetYaxis().SetTitle("PEF")
mg.SetMinimum(1E-3)
mg.SetMaximum(1)

leg.Draw("same")
CMS_lumi.CMS_lumi(c1,iPeriod,iPos)
c1.RedrawAxis()
c1.SetLogy(1)
c1.SaveAs("PEF_limit.pdf")
