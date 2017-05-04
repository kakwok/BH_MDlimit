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

f = TFile("StOpt_SB_charybdis_plot.root")

MD5930_xsec = f.Get("Xsec_SB_MD5930_n6")
MD5930_obs = f.Get("Observed_SB_MD5930_n6")
MD5930_exp = f.Get("Expected_SB_MD5930_n6")

MD5360_xsec = f.Get("Xsec_SB_MD5360_n6")
MD5360_obs  = f.Get("Observed_SB_MD5360_n6")
MD5360_exp  = f.Get("Expected_SB_MD5360_n6")

MD6800_xsec = f.Get("Xsec_SB_MD6800_n6")
MD6800_obs  = f.Get("Observed_SB_MD6800_n6")
MD6800_exp  = f.Get("Expected_SB_MD6800_n6")

MD8570_xsec = f.Get("Xsec_SB_MD8570_n6")
MD8570_obs  = f.Get("Observed_SB_MD8570_n6")
MD8570_exp  = f.Get("Expected_SB_MD8570_n6")



MD5930=[MD5930_xsec, MD5930_obs]
MD5360=[MD5360_xsec, MD5360_obs]
MD6800=[MD6800_xsec, MD6800_obs]
MD8570=[MD8570_xsec, MD8570_obs]

for g in MD5930:
	g.SetLineColor(12)
	g.SetFillColor(12)
	if not "Xsec" in g.GetName():
		g.SetMarkerStyle(kFullCircle)
	g.SetMarkerColor(12)
	g.SetLineWidth(2)
	#if "Xsec" in g.GetName():
	if not "Obs" in g.GetName() and not "Exp" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)
	
for g in MD5360:
	g.SetLineColor(kBlue)
	g.SetFillColor(kBlue)
	g.SetMarkerColor(kBlue)
	g.SetLineWidth(2)
	g.SetMarkerStyle(kFullSquare)
	#if "Xsec" in g.GetName():
	if not "Obs" in g.GetName() and not "Exp" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)
for g in MD6800:
	g.SetLineColor(kRed)
	g.SetFillColor(kRed)
	g.SetMarkerColor(kRed)
	g.SetLineWidth(2)
	g.SetMarkerStyle(kOpenCircle)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)
for g in MD8570:
	g.SetLineColor(kGreen)
	g.SetFillColor(kGreen)
	g.SetMarkerColor(kGreen)
	g.SetLineWidth(2)
	g.SetMarkerStyle(kOpenSquare)
	if "Xsec" in g.GetName():
		g.SetLineStyle(2)
		g.SetMarkerStyle(0)



mg = TMultiGraph()

for g in MD5930:
	mg.Add(g)
for g in MD5360:
	mg.Add(g)
for g in MD6800:
	mg.Add(g)
for g in MD8570:
	mg.Add(g)

mg.SetMinimum(1E-1)
mg.SetMaximum(1E5)
#mg.SetMinimum(1E-2)
#mg.SetMaximum(1E5)

canvas.SetLogy()

mg.Draw("ALP")
mg.GetXaxis().SetTitle("M_{SB}^{min} (TeV)")
mg.GetXaxis().SetLimits(4.5,10.5)
mg.GetXaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitle("#sigma (fb)")
mg.GetYaxis().SetTitleSize(0.045)
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
latex.DrawLatex(0.36,0.87,"String balls (Charybdis2)")
leg= TLegend(0.35,0.65,0.75,0.85, "Cross Section", "brNDC")
leg.AddEntry(MD5930_xsec," ","pl")
leg.AddEntry(MD5360_xsec," ","pl")
leg.AddEntry(MD6800_xsec," ","pl")
leg.AddEntry(MD8570_xsec," ","pl")
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.Draw()

leg2= TLegend(0.49,0.65,0.85,0.85, "Observed Limits", "brNDC")
leg2.AddEntry(MD5930_obs ,"M_{D}=5.93 TeV, M_{S}=1.1 TeV, g_{S}=0.2","pl")
leg2.AddEntry(MD5360_obs ,"M_{D}=5.36 TeV, M_{S}=1.1 TeV, g_{S}=0.3","pl")
leg2.AddEntry(MD6800_obs ,"M_{D}=6.80 TeV, M_{S}=1.5 TeV, g_{S}=0.4","pl")
leg2.AddEntry(MD8570_obs ,"M_{D}=8.57 TeV, M_{S}=2.0 TeV, g_{S}=0.5","pl")
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.03)
leg2.Draw()

canvas.SaveAs("SBlimit_charybdis.pdf")
