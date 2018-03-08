from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

def mapMDtoMS(SBgraph):
    for i in range(0,SBgraph.GetN()):
        x,y = Double(0.0),Double(0.0)
        SBgraph.GetPoint(i, x, y)
        gs = 0
#        print x,y
        if   (x==9.174):    gs=0.4
        elif (x==9.858):    gs=0.3
        elif (x==10.910):   gs=0.2
        SBgraph.SetPoint(i, gs, y)
        
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = False
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

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

f = TFile("../StOpt_SB2016_gsScan_plot.root")
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

mg = TMultiGraph()
mg.Add(SB_n6_TwoSig)
mg.Add(SB_n6_OneSig)
mg.Add(SB_n6)
mg.Add(SB_n6_exp)

mg.SetMinimum(6)
mg.SetMaximum(10.5)

mg.Draw("ALP E3")
mg.GetXaxis().SetTitle("g_{s}")
mg.GetXaxis().SetTitleSize(0.048)
mg.GetXaxis().SetLimits(0.2,0.4)
mg.GetXaxis().SetLabelOffset(0.022)
mg.GetXaxis().SetTitleOffset(1.2)
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
#latex.DrawLatex(0.36,0.87,"g_{s} = 0.2")
#leg= TLegend(0.35,0.65,0.75,0.85, "Charybdis2", "brNDC")
#leg.AddEntry(SB_n6," ","pl")
#leg.SetBorderSize(0)
#leg.SetTextFont(42)
#leg.SetTextSize(0.03)
#leg.Draw()

leg2= TLegend(0.4,0.65,0.85,0.85, "String balls, M_{S} = 3.6 TeV (Charybdis2)", "brNDC")
leg2.AddEntry(SB_n6 ,"Observed ","pl")
leg2.AddEntry(SB_n6_exp,"Expected","pl")
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.045)
leg2.Draw()

canvas.SaveAs("SBlimit_gs_scan.pdf")
