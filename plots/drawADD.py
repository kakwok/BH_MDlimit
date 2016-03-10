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


#f = TFile("StOpt_ADD_plot.root")
f = TFile("StOpt_ADDv2_plot.root")
QBHADD_n1 = f.Get("QBH_ADD_n1")
QBHADD_n2 = f.Get("QBH_ADD_n2")
QBHADD_n3 = f.Get("QBH_ADD_n3")
QBHADD_n4 = f.Get("QBH_ADD_n4")
QBHADD_n5 = f.Get("QBH_ADD_n5")
QBHADD_n6 = f.Get("QBH_ADD_n6")

graphs = [QBHADD_n1,QBHADD_n2,QBHADD_n3,QBHADD_n4,QBHADD_n5,QBHADD_n6]
LColor =[kBlue, kGreen, kOrange, kRed, kViolet, 12]
FColor =[kBlue, kGreen, kOrange, kRed, kViolet, 12]
MStyle =[kFullCircle,kFullSquare, kFullTriangleUp,kOpenSquare,kOpenCircle,kOpenSquare]
 
iGraphs=0
for g in graphs:
	g.SetLineColor( LColor[iGraphs])
	g.SetFillColor( FColor[iGraphs])
	g.SetMarkerStyle(MStyle[iGraphs])
	g.SetMarkerColor(FColor[iGraphs])
	g.SetLineWidth(2)
	iGraphs+=1

mg = TMultiGraph()

mg.Add(QBHADD_n1)
mg.Add(QBHADD_n2)
mg.Add(QBHADD_n3)
mg.Add(QBHADD_n4)
mg.Add(QBHADD_n5)
mg.Add(QBHADD_n6)

mg.SetMinimum(5)
mg.SetMaximum(10)

mg.Draw("ALP")
mg.GetXaxis().SetTitle("MD (TeV)")
mg.GetYaxis().SetTitle("Excluded M_{BH}^{min} (TeV)")
mg.SetTitle("")

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

leg= TLegend(0.15,0.15,0.4,0.4, "QBH ADD", "brNDC")
leg.AddEntry(QBHADD_n1,"n=1","pl")
leg.AddEntry(QBHADD_n2,"n=2","pl")
leg.AddEntry(QBHADD_n3,"n=3","pl")
leg.AddEntry(QBHADD_n4,"n=4","pl")
leg.AddEntry(QBHADD_n5,"n=5","pl")
leg.AddEntry(QBHADD_n6,"n=6","pl")
leg.SetBorderSize(0)
leg.Draw()
leg.SetTextFont(42)
leg.SetTextSize(0.045)

canvas.SaveAs("ADDlimit_final.pdf")
