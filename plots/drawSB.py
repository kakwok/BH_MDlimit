from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = False
#CMS_lumi.extraText = "Preliminary"
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

#f = TFile("StOpt_SBextra_v5_plot.root")
f = TFile("StOpt_SBextra_full_plot.root")
MD1640_xsec = f.Get("Xsec_SB_MD1640_n6")
MD1640_obs = f.Get("Observed_SB_MD1640_n6")
MD1640_exp = f.Get("Expected_SB_MD1640_n6")

MD1490_xsec = f.Get("Xsec_SB_MD1490_n6")
MD1490_obs  = f.Get("Observed_SB_MD1490_n6")
MD1490_exp  = f.Get("Expected_SB_MD1490_n6")

MD1890_xsec = f.Get("Xsec_SB_MD1890_n6")
MD1890_obs  = f.Get("Observed_SB_MD1890_n6")
MD1890_exp  = f.Get("Expected_SB_MD1890_n6")

MD2380_xsec = f.Get("Xsec_SB_MD2380_n6")
MD2380_obs  = f.Get("Observed_SB_MD2380_n6")
MD2380_exp  = f.Get("Expected_SB_MD2380_n6")



MD1640=[MD1640_xsec, MD1640_obs]
MD1490=[MD1490_xsec, MD1490_obs]
MD1890=[MD1890_xsec, MD1890_obs]
MD2380=[MD2380_xsec, MD2380_obs]

for g in MD1640:
	g.SetLineColor(12)
	g.SetFillColor(12)
	if not "Xsec" in g.GetName():
		g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(12)
	g.SetLineWidth(2)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)
	
for g in MD1490:
	g.SetLineColor(kBlue)
	g.SetFillColor(kBlue)
	g.SetMarkerColor(kBlue)
	g.SetLineWidth(2)
	g.SetMarkerStyle(kFullSquare)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)
for g in MD1890:
	g.SetLineColor(kRed)
	g.SetFillColor(kRed)
	g.SetMarkerColor(kRed)
	g.SetLineWidth(2)
	g.SetMarkerStyle(kOpenCircle)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)
for g in MD2380:
	g.SetLineColor(kGreen)
	g.SetFillColor(kGreen)
	g.SetMarkerColor(kGreen)
	g.SetLineWidth(2)
	g.SetMarkerStyle(kOpenSquare)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)



mg = TMultiGraph()

for g in MD1640:
	mg.Add(g)
for g in MD1490:
	mg.Add(g)
for g in MD1890:
	mg.Add(g)
for g in MD2380:
	mg.Add(g)

#mg.SetMinimum(1)
mg.SetMinimum(1E-3)
mg.SetMaximum(1E5)

canvas.SetLogy()

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M_{SB} (TeV)")
mg.GetXaxis().SetLimits(4.5,10.5)
mg.GetYaxis().SetTitle("#sigma (fb)")
mg.SetTitle("")
mg.Draw("ALP")

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
latex.DrawLatex(0.36,0.87,"String balls (BlackMax)")
leg= TLegend(0.35,0.65,0.75,0.85, "Cross Section", "brNDC")
leg.AddEntry(MD1640_xsec," ","pl")
leg.AddEntry(MD1490_xsec," ","pl")
leg.AddEntry(MD1890_xsec," ","pl")
leg.AddEntry(MD2380_xsec," ","pl")
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.Draw()

leg2= TLegend(0.49,0.65,0.85,0.85, "Observed Limits", "brNDC")
leg2.AddEntry(MD1640_obs,"M_{D}=1.64 TeV, M_{S}=1.1 TeV, g_{S}=0.2","pl")
leg2.AddEntry(MD1490_obs,"M_{D}=1.49 TeV, M_{S}=1.1 TeV, g_{S}=0.3","pl")
leg2.AddEntry(MD1890_obs,"M_{D}=1.89 TeV, M_{S}=1.5 TeV, g_{S}=0.4","pl")
leg2.AddEntry(MD2380_obs,"M_{D}=2.38 TeV, M_{S}=2.0 TeV, g_{S}=0.5","pl")
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.03)
leg2.Draw()

canvas.SaveAs("SBlimit_final.pdf")
