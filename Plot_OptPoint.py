from ROOT import *
from sys import argv
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
iPeriod = 4

def getOptPtDict(f,key,MD,n):
    data=[]
    datafile = open(f,"r")
    for line in datafile:
        line = line.strip().split()
        if (line[0]==key and line[1]==MD and line[2]==n):
            StOpt = float(line[4])
            nOpt  = float(line[5])
            MBH   = float(line[6])
            data.append([StOpt,nOpt,MBH])
    return data

def getTGraph(datalist):
        g=TGraph()
        datalist.sort()
        for data in datalist:
                g.SetPoint(g.GetN(),data[0],data[1])
        g.SetFillStyle(0)
        g.SetFillColor(0)
        return g

f = open(argv[1],"r")
f.next()
colors =[kBlack,kBlue,kRed,kGreen]
icolor=0

#SB_MD1100_gs02 = getOptPtDict(argv[1],"SB","5930","6")
#SB_MD1100_gs03 = getOptPtDict(argv[1],"SB","5360","6")
#SB_MD1500_gs04 = getOptPtDict(argv[1],"SB","6800","6")
#SB_MD2000_gs05 = getOptPtDict(argv[1],"SB","8570","6")
#glist    = [SB_MD1100_gs02,SB_MD1100_gs03,SB_MD1500_gs04,SB_MD2000_gs05]
#namelist = ["SB_MD1100_gs02","SB_MD1100_gs03","SB_MD1500_gs04","SB_MD2000_gs05"]

BH1_MD2000_n6 = getOptPtDict(argv[1],"BH1","2000","6")
BH1_MD3000_n6 = getOptPtDict(argv[1],"BH1","3000","6")
BH1_MD4000_n6 = getOptPtDict(argv[1],"BH1","4000","6")
glist    = [BH1_MD4000_n6]
namelist = ["BH1_MD4000_n6"]
#glist    = [BH1_MD2000_n6,BH1_MD3000_n6,BH1_MD4000_n6]
#namelist = ["BH1_MD2000_n6","BH1_MD3000_n6","BH1_MD4000_n6"]


print glist
c1 = TCanvas("c1","c1",800,600)
mg = TMultiGraph()
latex = TLatex()
latex.SetNDC()
leg = TLegend(0.6,0.7,0.8,0.9,"BlackMax:Non-rotating BH")
leg.SetBorderSize(0)
leg.SetTextSize(0.04)
for g in glist:
    graph = getTGraph(g)
    graph.SetMarkerColor(colors[icolor])
    graph.SetName(namelist[icolor])
    graph.SetMarkerStyle(kFullSquare)
    mg.Add(graph)
    leg.AddEntry(graph,"M_{D}=4 TeV, n=6","p")
    icolor+=1
mg.Draw("AP")
mg.SetMaximum(13)
mg.SetMinimum(0)
mg.GetXaxis().SetTitle("S_{T}^{min} [GeV]")
mg.GetYaxis().SetTitle("N_{min}")
mg.GetYaxis().SetTitleOffset(0.8)
CMS_lumi.CMS_lumi(c1,iPeriod,iPos)
leg.Draw("same")
raw_input('te')
c1.SaveAs("OptPt_%s.pdf"% (argv[1].replace(".txt","")))
