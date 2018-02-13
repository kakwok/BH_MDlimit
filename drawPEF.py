from ROOT import *
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
iPeriod = 4

#f = TFile("StOpt_Sphaleron.root")
#h = f.Get("SPHA_9000_1.0_6")
#c1 = TCanvas("c1","c1",800,600)
##h.SetTitle("Expected limit on PEF")
#h.GetYaxis().SetRangeUser(4000,8900)
#h.GetXaxis().SetRangeUser(7,11)
#h.GetXaxis().SetTitle("N_{min}")
#h.GetYaxis().SetTitle("S_{T}^{min}")
#h.Scale(1.0/7.3)
#h.Draw("COLZ")
#raw_input("test")
txt = open("StOpt_Sphaleron.log")
n7  = TGraph()
n8  = TGraph()
n9  = TGraph()
#n9.SetTitle("Expected limit on PEF for nMin=9,10,11")
n10  = TGraph()
n11  = TGraph()
n10.SetTitle("Expected limit on PEF for nMin=9")
for line in txt:
    line = line.strip().split()
    if (len(line)==5):
        nMin    = int(line[0])
        StMin   = float(line[1])
        Accept  = float(line[2])
        limit   = float(line[4])
        if(nMin ==7):
            PEF =  limit/7.3
            n7.SetPoint(n7.GetN(),StMin, PEF)
        if(nMin ==8):
            PEF =  limit/7.3
            n8.SetPoint(n8.GetN(),StMin, PEF)
        if(nMin ==9):
            PEF =  limit/7.3
            n9.SetPoint(n9.GetN(),StMin, PEF)
        if(nMin ==10):
            PEF =  limit/7.3
            n10.SetPoint(n10.GetN(),StMin, PEF)
        #if(nMin ==11):
        #    PEF =  limit/7.3
        #    n11.SetPoint(n11.GetN(),StMin, PEF)

n7.SetLineColor(kBlue)
n8.SetLineColor(kGreen)
n9.SetLineColor(kRed)
n10.SetLineColor(kViolet)
#n11.SetLineColor(kGreen)
leg = TLegend(0.58,0.71,0.78,0.91)
leg.AddEntry(n7,"N_{min} =7","l")
leg.AddEntry(n8,"N_{min} =8","l")
leg.AddEntry(n9,"N_{min} =9","l")
leg.AddEntry(n10,"N_{min} =10","l")
#leg.AddEntry(n11,"N_{min} =11","l")
n9.Draw("AC")
n9.GetXaxis().SetTitle("S_{T}^{min} [GeV]")
n9.GetYaxis().SetTitle("Expected limit on PEF")
n9.GetXaxis().SetTitleSize(0.04)
n9.GetYaxis().SetTitleSize(0.03)
n9.GetXaxis().SetTitleOffset(1.2)
n9.GetYaxis().SetTitleOffset(1.25)
n9.GetXaxis().SetLabelSize(0.05)
n9.GetYaxis().SetLabelSize(0.03)
n7.Draw("same")
n8.Draw("same")
n10.Draw("same")
#n11.Draw("same")
leg.Draw("same")
CMS_lumi.CMS_lumi(c1,iPeriod,iPos)
c1.SaveAs("PEF_limit_n8n9n10.pdf")
