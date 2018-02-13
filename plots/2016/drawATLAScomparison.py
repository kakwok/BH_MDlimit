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


#f = TFile("StOpt_BHfull_plot.root")
f = TFile("../StOpt_Charybdis2016_plot.root")
f2 = TFile("../StOpt_Charybdis_newFormat_plot.root")
#f2 = TFile("StOpt_Charybdis_BH6_plot.root")
#f3 = TFile("StOpt_Charybdis_BH10_plot.root")
BH2_n2 = f.Get("BH2_n2")
BH2_n4 = f.Get("BH2_n4")
BH2_n6 = f.Get("BH2_n6")

BH2_n2_2015 = f2.Get("BH2_n2")
BH2_n4_2015 = f2.Get("BH2_n4")
BH2_n6_2015 = f2.Get("BH2_n6")

BH2_n2_ATLAS = TGraph() 
BH2_n4_ATLAS = TGraph() 
BH2_n6_ATLAS = TGraph() 

BH2_n2_ATLAS.SetName("BH_2_n2_ATLAS")
BH2_n4_ATLAS.SetName("BH_2_n4_ATLAS")
BH2_n6_ATLAS.SetName("BH_2_n6_ATLAS")

BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 2.0, 9.2)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 2.5, 9.1)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 3.0, 8.9)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 3.5, 8.65)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 4.0, 8.5)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 4.5, 8.37)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 5.0, 8.15)
BH2_n2_ATLAS.SetPoint(BH2_n2_ATLAS.GetN(), 5.5, 8.05)

BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 2.0, 9.6)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 2.5, 9.5)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 3.0, 9.2)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 3.5, 9.15)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 4.0, 9.0)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 4.5, 8.9)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 5.0, 8.7)
BH2_n4_ATLAS.SetPoint(BH2_n4_ATLAS.GetN(), 5.5, 8.6)

BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 2.0, 9.7)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 2.5, 9.65)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 3.0, 9.58)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 3.5, 9.38)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 4.0, 9.2)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 4.5, 9.17)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 5.0, 9.0)
BH2_n6_ATLAS.SetPoint(BH2_n6_ATLAS.GetN(), 5.5, 8.97)


BH2=[BH2_n2,BH2_n4,BH2_n6]
BH2_2015=[BH2_n2_2015,BH2_n4_2015,BH2_n6_2015]
BH2_ATLAS=[BH2_n2_ATLAS,BH2_n4_ATLAS,BH2_n6_ATLAS]

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

for g in BH2_ATLAS:
	g.SetLineColor(kRed)
	g.SetFillColor(kRed)
	g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(kRed)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(5)

for g in BH2_2015:
	g.SetLineColor(kGreen)
	g.SetFillColor(kGreen)
	g.SetMarkerStyle(kFullSquare)
	g.SetMarkerColor(kGreen)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(5)


mg = TMultiGraph()

mg.Add(BH2_n2)
mg.Add(BH2_n4)
mg.Add(BH2_n6)

mg.Add(BH2_n2_ATLAS)
mg.Add(BH2_n4_ATLAS)
mg.Add(BH2_n6_ATLAS)

#mg.Add(BH2_n2_2015)
#mg.Add(BH2_n4_2015)
#mg.Add(BH2_n6_2015)


mg.SetMinimum(6.3)
mg.SetMaximum(10.5)

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M_{D} (TeV)")
mg.GetXaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitle("Excluded M_{ BH}^{ min} (TeV)")
mg.GetYaxis().SetTitleOffset(1.2)
mg.SetTitle("")

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.05)
#latex.DrawLatex(0.5,0.4,"n=6")

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

leg= TLegend(0.15,0.15,0.92,0.3, "Charybdis2", "brNDC")
leg.SetNColumns(3)
leg.AddEntry(BH2_n2,"Rotating (C1) n=2","pl")
leg.AddEntry(BH2_n4,"Rotating (C1) n=4","pl")
leg.AddEntry(BH2_n6,"Rotating (C1) n=6","pl")
#leg.AddEntry(BH2_n2_2015,"Rotating (C1) 2015 n=2","pl")
#leg.AddEntry(BH2_n4_2015,"Rotating (C1) 2015 n=4","pl")
#leg.AddEntry(BH2_n6_2015,"Rotating (C1) 2015 n=6","pl")

leg.AddEntry(BH2_n2_ATLAS,"ATLAS Rotating n=2","pl")
leg.AddEntry(BH2_n4_ATLAS,"ATLAS Rotating n=4","pl")
leg.AddEntry(BH2_n6_ATLAS,"ATLAS Rotating n=6","pl")

leg.SetBorderSize(0)
leg.Draw()
leg.SetTextFont(42)
leg.SetTextSize(0.03)

#canvas.SaveAs("Charybdis_limit_CWR.pdf")
canvas.SaveAs("Charybdis2016_ATLAS.pdf")
