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

f = TFile("StOpt_RS1_plot.root")
MD4000_xsec = f.Get("Xsec_QBH_RS1_MD4000_n1")
MD4000_obs =  f.Get("Observed_QBH_RS1_MD4000_n1")
MD4000_exp =  f.Get("Expected_QBH_RS1_MD4000_n1")

MD4000=[MD4000_xsec, MD4000_obs]

for g in MD4000:
	g.SetLineColor(kBlue)
	g.SetFillColor(kBlue)
	if not "Xsec" in g.GetName():
		g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(kBlue)
	g.SetLineWidth(2)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)

mg = TMultiGraph()

for g in MD4000:
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

latex.DrawLatex(0.363,0.87,"RS1")
leg= TLegend(0.35,0.7,0.85,0.85, "Theoretical Cross Section", "brNDC")
leg.AddEntry(MD4000_xsec,"M_{D}=4 TeV, n=1","pl")
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.Draw()

leg2= TLegend(0.35,0.55,0.85,0.69, "Observed Cross Section Limits", "brNDC")
leg2.AddEntry(MD4000_obs,"M_{D}=4 TeV, n=1","pl")
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.045)
leg2.Draw()

canvas.SaveAs("RS1_limit_final.pdf")
