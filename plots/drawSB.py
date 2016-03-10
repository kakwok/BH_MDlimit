from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
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

f = TFile("StOpt_SBextra_v5_plot.root")
MD1640_xsec = f.Get("Xsec_SB_MD1640_n6")
MD1640_obs = f.Get("Observed_SB_MD1640_n6")
MD1640_exp = f.Get("Expected_SB_MD1640_n6")

MD1490_xsec = f.Get("Xsec_SB_MD1490_n6")
MD1490_obs  = f.Get("Observed_SB_MD1490_n6")
MD1490_exp  = f.Get("Expected_SB_MD1490_n6")

MD1640=[MD1640_xsec, MD1640_obs]
MD1490=[MD1490_xsec, MD1490_obs]

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

mg = TMultiGraph()

for g in MD1640:
	mg.Add(g)
for g in MD1490:
	mg.Add(g)

mg.SetMinimum(1)
mg.SetMaximum(1E3)

canvas.SetLogy()

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M^{min} (TeV)")
mg.GetYaxis().SetTitle("#sigma (fb)")
mg.SetTitle("")

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
latex.DrawLatex(0.363,0.87,"String ball(BlackMax)")
leg= TLegend(0.35,0.7,0.85,0.85, "Theoretical Cross Section", "brNDC")
leg.AddEntry(MD1640_xsec,"M_{D}=1.64 TeV, M_{S}=1.1 TeV, g_{S}=0.2","pl")
leg.AddEntry(MD1490_xsec,"M_{D}=1.49 TeV, M_{S}=1.1 TeV, g_{S}=0.3","pl")
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.Draw()

leg2= TLegend(0.35,0.55,0.85,0.69, "Observed Cross Section Limits", "brNDC")
leg2.AddEntry(MD1640_obs,"M_{D}=1.64 TeV, M_{S}=1.1 TeV, g_{S}=0.2","pl")
leg2.AddEntry(MD1490_obs,"M_{D}=1.49 TeV, M_{S}=1.1 TeV, g_{S}=0.3","pl")
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.045)
leg2.Draw()

canvas.SaveAs("SBlimit_final.pdf")
