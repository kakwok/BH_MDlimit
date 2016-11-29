from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 33
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


#f = TFile("StOpt_BHtest2_plot.root")
f = TFile("StOpt_BHfull_plot.root")
BH1_n2 = f.Get("BH1_n2")
BH1_n4 = f.Get("BH1_n4")
BH1_n6 = f.Get("BH1_n6")
BH2_n2 = f.Get("BH2_n2")
BH2_n4 = f.Get("BH2_n4")
BH2_n6 = f.Get("BH2_n6")
BH5_n2 = f.Get("BH5_n2")
BH5_n4 = f.Get("BH5_n4")
BH5_n6 = f.Get("BH5_n6")
BH5_n2_exp = f.Get("BH5_n2_exp")
BH5_n4_exp = f.Get("BH5_n4_exp")
BH5_n6_exp = f.Get("BH5_n6_exp")


BH1=[BH1_n2,BH1_n4,BH1_n6]
BH2=[BH2_n2,BH2_n4,BH2_n6]
BH5=[BH5_n2,BH5_n4,BH5_n6]
BH5_exp=[BH5_n2_exp,BH5_n4_exp,BH5_n6_exp]
for g in BH1:
	g.SetLineColor(12)
	g.SetFillColor(12)
	g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(12)
	g.SetLineWidth(2)
for g in BH2:
	g.SetLineColor(kBlue)
	g.SetFillColor(kBlue)
	g.SetMarkerStyle(kFullSquare)
	g.SetMarkerColor(kBlue)
	g.SetLineWidth(2)
for g in BH5:
	g.SetLineColor(kOrange)
	g.SetFillColor(kOrange)
	g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(kOrange)
	g.SetLineWidth(2)
for g in BH5_exp:
	g.SetLineColor(kOrange)
	g.SetFillColor(kOrange)
	g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(kOrange)
	g.SetLineWidth(2)
	g.SetLineStyle(2)


mg = TMultiGraph()

mg.Add(BH1_n2)
mg.Add(BH1_n4)
mg.Add(BH1_n6)
mg.Add(BH2_n2)
mg.Add(BH2_n4)
mg.Add(BH2_n6)
mg.Add(BH5_n2)
mg.Add(BH5_n4)
mg.Add(BH5_n6)
mg.Add(BH5_n2_exp)
mg.Add(BH5_n4_exp)
mg.Add(BH5_n6_exp)


mg.SetMinimum(5)
mg.SetMaximum(10)

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M_D (TeV)")
mg.GetYaxis().SetTitle("Excluded M_{BH}^{min} (TeV)")
mg.SetTitle("")

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.05)
latex.DrawLatex(0.8,0.63,"n6")
latex.DrawLatex(0.8,0.55,"n4")
latex.DrawLatex(0.8,0.4,"n2")

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

leg= TLegend(0.15,0.15,0.4,0.4, "BlackMax", "brNDC")
leg.AddEntry(BH1_n2,"Non-rotating,no gravition(BH1)","pl")
leg.AddEntry(BH2_n2,"Rotating(BH2)","pl")
leg.AddEntry(BH5_n2,"Rotating(BH5)","pl")
leg.AddEntry(BH5_n2_exp,"Rotating(BH5) Expected","pl")
leg.SetBorderSize(0)
leg.Draw()
leg.SetTextFont(42)
leg.SetTextSize(0.045)

#canvas.SaveAs("BHlimit_final.pdf")
canvas.SaveAs("BHlimit_fullsim_May31.pdf")
