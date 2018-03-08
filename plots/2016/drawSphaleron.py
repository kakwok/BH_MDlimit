from ROOT import *
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 0
#CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
iPeriod = 4

txt = open("../../StOpt_Sphaleron.txt")
g_spha  = TGraph()
g_spha_exp  = TGraph()
for line in txt:
    line = line.strip().split()
    if (line[0]=="SPHA"):
        E_spha  = float(line[1])
        StMin   = float(line[4])
        NMin    = float(line[5])
        exp_limit=float(line[6])
        limit   = float(line[11])
        if(E_spha==8.0):
            PEF =  limit/99.17
            PEF_exp =  exp_limit/99.17
        if(E_spha==9.0):
            PEF =  limit/7.1
            PEF_exp =  exp_limit/7.1
        if(E_spha==10.0):
            PEF =  limit/0.268
            PEF_exp =  exp_limit/0.268
        print "%s   xsec_limit = %.3f  PEF_limit=%.3f expected=%.3f"%(E_spha,limit, PEF,PEF_exp)
        g_spha.SetPoint(g_spha.GetN(),E_spha, PEF)
        g_spha_exp.SetPoint(g_spha_exp.GetN(),E_spha, PEF_exp)

g_spha_exp.SetLineColor(kBlack)
g_spha_exp.SetLineStyle(9)

g_spha.SetLineColor(kRed)
g_spha.SetFillColor(kRed)
g_spha.SetLineWidth(2002)
g_spha.SetFillStyle(3004)

leg = TLegend(0.2,0.71,0.6,0.91)
leg.AddEntry(g_spha,"Observed 95% exclusion","l")
leg.AddEntry(g_spha_exp,"Expected limit","l")
leg.SetTextSize(0.03)
g_spha.Draw("AC")
g_spha_exp.Draw("same")
g_spha.GetXaxis().SetTitle("E_{Sph} [TeV]")
g_spha.GetXaxis().SetLimits(8.0,10.0)
g_spha.GetYaxis().SetTitle("PEF")
g_spha.SetMinimum(1E-3)
g_spha.SetMaximum(1)

g_spha.GetXaxis().SetTitleSize(0.04)
g_spha.GetYaxis().SetTitleSize(0.04)
g_spha.GetXaxis().SetTitleOffset(1.2)
g_spha.GetYaxis().SetTitleOffset(1.25)
g_spha.GetXaxis().SetLabelSize(0.04)
g_spha.GetYaxis().SetLabelSize(0.04)
leg.Draw("same")
CMS_lumi.CMS_lumi(c1,iPeriod,iPos)
c1.SetLogy(1)
c1.SaveAs("PEF_limit.pdf")
