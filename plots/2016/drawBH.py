from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
#CMS_lumi.extraText = ""
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 33
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

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
f = TFile("../StOpt_BlackMax2016_plot.root")
BH1_n2 = f.Get("BH1_n2")
BH1_n4 = f.Get("BH1_n4")
BH1_n6 = f.Get("BH1_n6")
BH2_n2 = f.Get("BH2_n2")
BH2_n4 = f.Get("BH2_n4")
BH2_n6 = f.Get("BH2_n6")
BH5_n2 = f.Get("BH5_n2")
BH5_n4 = f.Get("BH5_n4")
BH5_n6 = f.Get("BH5_n6")
#BH5_n2_exp = f.Get("BH5_n2_exp")
#BH5_n4_exp = f.Get("BH5_n4_exp")
#BH5_n6_exp = f.Get("BH5_n6_exp")


BH1=[BH1_n2,BH1_n4,BH1_n6]
BH2=[BH2_n2,BH2_n4,BH2_n6]
BH5=[BH5_n2,BH5_n4,BH5_n6]
BH5_exp=[BH5_n2_exp,BH5_n4_exp,BH5_n6_exp]
for g in BH1:
	g.SetLineColor(kGreen)
	g.SetFillColor(kGreen)
	g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(kGreen)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(5)
for g in BH2:
	g.SetLineColor(kBlue)
	g.SetFillColor(kBlue)
	g.SetMarkerStyle(kFullSquare)
	g.SetMarkerColor(kBlue)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(5)

for g in BH5:
	g.SetLineColor(kRed)
	g.SetFillColor(kRed)
	g.SetMarkerStyle(kFullTriangleUp)
	g.SetMarkerColor(kRed)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(5)


#for g in BH5_exp:
#	g.SetLineColor(kRed)
#	g.SetFillColor(kRed)
#	g.SetMarkerStyle(kFullTriangleDown)
#	g.SetMarkerColor(kRed)
#	g.SetLineWidth(2)
#	if "n6" in g.GetName():
#		g.SetLineStyle(1)
#	if "n4" in g.GetName():
#		g.SetLineStyle(2)
#	if "n2" in g.GetName():
#		g.SetLineStyle(5)

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
#mg.Add(BH5_n2_exp)
#mg.Add(BH5_n4_exp)
#mg.Add(BH5_n6_exp)


mg.SetMinimum(5.8)
mg.SetMaximum(11)

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M_{D} (TeV)")
mg.GetXaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitle("Excluded M_{ BH}^{ min} (TeV)")
mg.SetTitle("")

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.05)
#latex.DrawLatex(0.8,0.63,"n6")
#latex.DrawLatex(0.8,0.55,"n4")
#latex.DrawLatex(0.8,0.4,"n2")

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

n6 = TGraph()
n6.SetLineWidth(2)
n4 = TGraph()
n4.SetLineWidth(2)
n4.SetLineStyle(2)
n2 = TGraph()
n2.SetLineWidth(2)
n2.SetLineStyle(5)

leg= TLegend(0.15,0.145,0.7,0.295, "BlackMax", "brNDC")
leg.SetNColumns(2)
leg.AddEntry(BH1_n6,"Nonrotating, no graviton emission (B1)","p")
leg.AddEntry(n6,"n = 6","l")
leg.AddEntry(BH2_n6,"Rotating, no graviton emission (B2)","p")
leg.AddEntry(n4,"n = 4","l")
leg.AddEntry(BH5_n6,"Rotating, energy/momentum loss (B3)","p")
leg.AddEntry(n2,"n = 2","l")
#leg.AddEntry(BH5_n6_exp,"Rotating, B3 (Expected)","p")
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.Draw()

canvas.SaveAs("BHlimit_BlackMax.pdf")
#canvas.SaveAs("BHlimit_CWR.pdf")
#canvas.SaveAs("BHlimit_fullsim_May31.pdf")
