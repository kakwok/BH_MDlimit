from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

def mapMDtoMS(SBgraph):
    for i in range(0,SBgraph.GetN()):
        x,y = Double(0.0),Double(0.0)
        SBgraph.GetPoint(i, x, y)
        MS = 0
#        print x,y
        if   (x==3.031):    MS=1.0
        elif (x==4.546):    MS=1.5
        elif (x==6.061):    MS=2.0
        elif (x==7.576):    MS=2.5
        elif (x==9.092):    MS=3.0
        elif (x==10.607):   MS=3.5
        elif (x==12.122):   MS=4.0
        SBgraph.SetPoint(i, MS, y)
        
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = False
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
CMS_lumi.lumiTextSize     = 0.65

H_ref = 600;
W_ref = 800;
W = W_ref
H  = H_ref

iPeriod = 4

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

canvas = TCanvas("c2","c2",50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)
frame = canvas.GetFrame()

f = TFile("../StOpt_SB2016_plot.root")
SB_n6     = f.Get("SB_n6")
SB_n6_exp = f.Get("SB_n6_exp")
SB_n6_OneSig  = f.Get("SB_n6_OneSig")
SB_n6_TwoSig  = f.Get("SB_n6_TwoSig")

mapMDtoMS(SB_n6)
mapMDtoMS(SB_n6_exp)
mapMDtoMS(SB_n6_OneSig)
mapMDtoMS(SB_n6_TwoSig)
SB_n6.SetLineWidth(2)
SB_n6.SetLineColor(kBlack)
SB_n6.SetMarkerColor(kBlack)
SB_n6.SetMarkerStyle(kFullCircle)
SB_n6_exp.SetLineWidth(2)
SB_n6_exp.SetLineStyle(2)
SB_n6_exp.SetLineColor(kBlack)
SB_n6_exp.SetMarkerStyle(0)
SB_n6_OneSig.SetLineWidth(2)
SB_n6_OneSig.SetLineStyle(2)
SB_n6_OneSig.SetLineColor(kBlack)
SB_n6_OneSig.SetFillColor(kGreen+1)
SB_n6_TwoSig.SetLineWidth(2)
SB_n6_TwoSig.SetLineStyle(2)
SB_n6_TwoSig.SetLineColor(kBlack)


mg = TMultiGraph()
mg.Add(SB_n6_TwoSig)
mg.Add(SB_n6_OneSig)
mg.Add(SB_n6)
mg.Add(SB_n6_exp)

mg.SetMinimum(6.5)
mg.SetMaximum(11)

mg.Draw("ALP E3")
mg.GetXaxis().SetTitle("M_{S} [TeV]")
mg.GetXaxis().SetTitleSize(0.045)
mg.GetXaxis().SetLimits(1.0,3.5)
mg.GetXaxis().SetLabelOffset(0.015)
mg.GetXaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetLabelSize(0.045)

mg.GetYaxis().SetTitle("M_{SB} [TeV]")
mg.GetYaxis().SetTitleSize(0.045)
mg.GetYaxis().SetTitleOffset(1.1)
mg.GetYaxis().SetLabelSize(0.045)
mg.SetTitle("")
mg.Draw("ALP E3")

latex = TLatex()
latex.SetNDC()
latex.SetTextFont(42)
latex.SetTextSize(0.045)

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

blankline = 0

latex.DrawLatex(0.17,0.78, "String balls (Charybdis 2)")
latex.DrawLatex(0.17,0.73, "g_{s} = 0.2")

latex.DrawLatex(0.65,0.87,"Lower limits, 95% CL")
leg2= TLegend(0.65,0.65,0.85,0.85, "", "brNDC")
#latex.DrawLatex(0.415,0.87,"Lower limits, 95% CL")
#leg2= TLegend(0.4,0.65,0.85,0.85, "String balls, g_{s} = 0.2 (Charybdis 2)", "brNDC")
leg2.AddEntry(SB_n6 ,"Observed ","pl")
leg2.AddEntry(SB_n6_OneSig,"68% expected","lf")
leg2.AddEntry(SB_n6_TwoSig,"95% expected","lf")
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.045)
leg2.Draw()

canvas.SaveAs("SBlimit_MSscan.pdf")
#outputRoot = TFile("SBlimit_MSscan.root","RECREATE")
#outputRoot.cd()
#canvas.Write()
