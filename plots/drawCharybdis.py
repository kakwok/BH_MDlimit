from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
#CMS_lumi.extraText = "Preliminary"
CMS_lumi.extraText = ""
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
f = TFile("StOpt_Charybdis_plot.root")
f2 = TFile("StOpt_Charybdis_BH6_plot.root")
f3 = TFile("StOpt_Charybdis_BH10_plot.root")
BH2_n2 = f.Get("BH2_n2")
BH2_n4 = f.Get("BH2_n4")
BH2_n6 = f.Get("BH2_n6")
BH4_n2 = f.Get("BH4_n2")
BH4_n4 = f.Get("BH4_n4")
BH4_n6 = f.Get("BH4_n6")
BH6_n2 = f2.Get("BH6_n2")
BH6_n4 = f2.Get("BH6_n4")
BH6_n6 = f2.Get("BH6_n6")
BH8_n2 = f.Get("BH8_n2")
BH8_n4 = f.Get("BH8_n4")
BH8_n6 = f.Get("BH8_n6")
BH10_n2 = f3.Get("BH10_n2")
BH10_n4 = f3.Get("BH10_n4")
BH10_n6 = f3.Get("BH10_n6")

BH2=[BH2_n2,BH2_n4,BH2_n6]
BH4=[BH4_n2,BH4_n4,BH4_n6]
BH6=[BH6_n2,BH6_n4,BH6_n6]
BH8=[BH8_n2,BH8_n4,BH8_n6]
BH10=[BH10_n2,BH10_n4,BH10_n6]
for g in BH8:
	g.SetLineColor(kMagenta)
	g.SetFillColor(kMagenta)
	g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(kMagenta)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(9)

for g in BH2:
	g.SetLineColor(kBlue)
	g.SetFillColor(kBlue)
	g.SetMarkerStyle(kFullSquare)
	g.SetMarkerColor(kBlue)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(9)

for g in BH4:
	g.SetLineColor(kOrange)
	g.SetFillColor(kOrange)
	g.SetMarkerStyle(kFullTriangleUp)
	g.SetMarkerColor(kOrange)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(9)

for g in BH6:
	g.SetLineColor(kRed)
	g.SetFillColor(kRed)
	g.SetMarkerStyle(kFullTriangleDown)
	g.SetMarkerColor(kRed)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(9)

for g in BH10:
	g.SetLineColor(kGreen)
	g.SetFillColor(kGreen)
	g.SetMarkerStyle(kFullCross)
	g.SetMarkerColor(kGreen)
	g.SetLineWidth(2)
	if "n4" in g.GetName():
		g.SetLineStyle(2)
	if "n2" in g.GetName():
		g.SetLineStyle(9)


mg = TMultiGraph()

mg.Add(BH8_n2)
mg.Add(BH8_n4)
mg.Add(BH8_n6)
mg.Add(BH2_n2)
mg.Add(BH2_n4)
mg.Add(BH2_n6)
mg.Add(BH4_n2)
mg.Add(BH4_n4)
mg.Add(BH4_n6)
mg.Add(BH6_n2)
mg.Add(BH6_n4)
mg.Add(BH6_n6)
mg.Add(BH10_n2)
mg.Add(BH10_n4)
mg.Add(BH10_n6)


mg.SetMinimum(6.3)
mg.SetMaximum(9.5)

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M_{D} (TeV)")
mg.GetXaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitle("Excluded M_{ BH}^{ min} (TeV)")
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

n6 = TGraph()
n6.SetLineWidth(2)
n4 = TGraph()
n4.SetLineWidth(2)
n4.SetLineStyle(2)
n2 = TGraph()
n2.SetLineWidth(2)
n2.SetLineStyle(9)


leg= TLegend(0.15,0.15,0.9,0.3, "Charybdis", "brNDC")
leg.SetNColumns(3)
leg.AddEntry(BH2_n6,"Rotating (C1)","p")
leg.AddEntry(BH4_n6,"Nonrotating (C2)","p")
leg.AddEntry(n6,"n = 6","l")
leg.AddEntry(BH8_n6,"Rotating, evaporation model (C3)","p")
leg.AddEntry(BH6_n6,"Rotating, YR model (C4)","p")
leg.AddEntry(n4,"n = 4","l")
leg.AddEntry(BH10_n6,"Rotating, stable remnant (C5)","p")
leg.AddEntry(0, "", "");
leg.AddEntry(n2,"n = 2","l")
leg.SetBorderSize(0)
leg.Draw()
leg.SetTextFont(42)
leg.SetTextSize(0.03)

canvas.SaveAs("Charybdis_limit_CWR.pdf")
