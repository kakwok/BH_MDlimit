#!/usr/bin/env python
from ROOT import *
from sys  import argv
from Modelpoint import *
import CMS_lumi, tdrstyle
import array

Input = open("%s"%argv[1])
PlotRoot = TFile.Open("./plots/%s_plot.root"%argv[1].replace(".txt",""),"recreate")
PlotTxt = open("./plots/%s_plot.txt"%argv[1].replace(".txt",""),"w")

ymin = 1e-2
ymax = 1e3

#############
Modelpoints =[]
MD_last      ="default"
ModelID_last =0
n_last       =0
key_last     = ""
Model        = Modelpoint(ModelID_last,MD_last,n_last)

#print Model.datalist
next(Input)
for line in Input:
    line   = line.split()
    ModelID= line[0]
    MD        = int  (line[1])
    n         = int  (line[2])
    MBH       = float(line[3])
    Stmin     = float(line[4])
    nmin      = int  (line[5])
    Zbi       = float(line[6])
    signal    = float(line[7])
    accpt     = float(line[8])
    Stlimit   = float(line[9])
    Xsec      = float(line[10])
    Obs       = float(line[11])
    m2sig     = float(line[12])
    m1sig     = float(line[13])
    Exp       = float(line[14])
    p1sig     = float(line[15])
    p2sig     = float(line[16])

    key    = ModelID+"_MD"+line[1]+"_n"+line[2]
    data   = [MBH, Stmin, nmin, Zbi,signal,Xsec,accpt,Stlimit,Obs,m2sig,m1sig,Exp,p1sig,p2sig]
    if ( key_last!=key):
        print "Adding model:  %s "% (key)
        # Add a new model point when we are reading a new model and the data in Model is not empty
        if Model.datalist:
            Modelpoints.append( Model )
        Model  = Modelpoint(ModelID, MD, n)
        Model.addData(data)
    else:
        Model.addData(data)
    key_last = key 
# if we finish scanning the input text file with a non-empty datalist, add it as a Model
if  Model.datalist:
    Modelpoints.append( Model )
print "found %s model points " % (len(Modelpoints)) 

# Sort the Models :
Modelpoints = sorted(Modelpoints,key=lambda item: item.MD)
Modelpoints = sorted(Modelpoints,key=lambda item: item.n)
Modelpoints = sorted(Modelpoints,key=lambda item: item.ModelID)

# Plot the graphs
ZbiOpt_grph =[]
StOpt_grph  =[] 
NOpt_grph   =[]
Xsec_grph   =[]
Obs_limit   =[]
TwoSig_limit  =[]
OneSig_limit  =[]
Exp_limit   =[]

Modellines =[]
Modellines_exp =[]
Modellines_OneSig =[]
Modellines_TwoSig =[]
iModel=0
iModellines=0
for M in Modelpoints:
    #print "Printing info of model:",M.key
    #
    #print "[MBH, Stmin, nmin, Zbi,signal,Xsec,accpt,Stlimit,Obs,m2sig,m1sig,Exp,p1sig,p2sig]"
    #M.printData()
    #print M.getMinMBH("Exp")
    
    ZbiOpt_grph.append( TGraph())
    ZbiOpt_grph[iModel].SetTitle("ZbiOpt_%s"%M.key)
    ZbiOpt_grph[iModel].SetName("ZbiOpt_%s"%M.key)
    StOpt_grph.append( TGraph())
    StOpt_grph[iModel].SetTitle("StOpt_%s"%M.key)
    StOpt_grph[iModel].SetName("StOpt_%s"%M.key)
    NOpt_grph.append( TGraph())
    NOpt_grph[iModel].SetTitle("NOpt_%s"%M.key)
    NOpt_grph[iModel].SetName("NOpt_%s"%M.key)
    Xsec_grph.append( TGraph())
    Xsec_grph[iModel].SetTitle("Xsec_%s"%M.key)
    Xsec_grph[iModel].SetName("Xsec_%s"%M.key)

    Obs_limit.append( TGraph())
    Obs_limit[iModel].SetTitle("Observed")
    Obs_limit[iModel].SetName("Observed_%s"%M.key)
    TwoSig_limit.append( TGraphAsymmErrors())
    #TwoSig_limit[iModel].SetTitle("Expected 2-#sigma")
    OneSig_limit.append( TGraphAsymmErrors())
    #OneSig_limit[iModel].SetTitle("Expected 1-#sigma")
    Exp_limit.append( TGraph())
    Exp_limit[iModel].SetTitle("Expected")
    Exp_limit[iModel].SetName("Expected_%s"%M.key)

    #         [  0,    1 ,   2 ,  3 ,   4  ,  5 ,  6  ,   7   , 8 ,  9  ,  10 , 11,  12 , 13  ]
    #data   = [MBH, Stmin, nmin, Zbi,signal,Xsec,accpt,Stlimit,Exp,m2sig,m1sig,Obs,p1sig,p2sig]
    for data in M.datalist:
        ZbiOpt_grph[iModel].SetPoint(ZbiOpt_grph[iModel].GetN(), data[0]/1000, data[3])
        StOpt_grph[iModel].SetPoint(  StOpt_grph[iModel].GetN(), data[0]/1000, data[1]/1000)
        NOpt_grph[iModel].SetPoint(    NOpt_grph[iModel].GetN(), data[0]/1000, data[2])
        Xsec_grph[iModel].SetPoint(    Xsec_grph[iModel].GetN(), data[0]/1000, data[5])
        Obs_limit[iModel].SetPoint(    Obs_limit[iModel].GetN(), data[0]/1000, data[8])
        Exp_limit[iModel].SetPoint(    Exp_limit[iModel].GetN(), data[0]/1000, data[11])
        # In AsymError Grap , Difference w.r.t. central points are plotted. 
        TwoSig_limit[iModel].SetPoint(  TwoSig_limit[iModel].GetN(), data[0]/1000, data[8])
        TwoSig_limit[iModel].SetPointError(  TwoSig_limit[iModel].GetN()-1, 0,0,  (data[8]-data[9]), (data[13]-data[8]) ) #  Obs-2sigma_down,2sigmaUp-Obs
        OneSig_limit[iModel].SetPoint(  OneSig_limit[iModel].GetN(), data[0]/1000, data[8])
        OneSig_limit[iModel].SetPointError(  OneSig_limit[iModel].GetN()-1, 0,0,  (data[8]-data[10]), (data[12]-data[8]) )#  Obs-1sigma_down,1sigmaUp-Obs

    NOpt_grph[iModel].Write()
    StOpt_grph[iModel].Write()
    ZbiOpt_grph[iModel].Write()
    Xsec_grph[iModel].Write()
    Obs_limit[iModel].Write()
    Exp_limit[iModel].Write()
    if( iModel==0 ):
        Modellines.append( TGraph())
        Modellines[iModellines].SetName("%s_n%s"%(M.ModelID,M.n))   
        Modellines[iModellines].SetTitle("%s_n%s"%(M.ModelID,M.n))  
        
        Modellines_exp.append( TGraph())
        Modellines_exp[iModellines].SetName("%s_n%s_exp"%(M.ModelID,M.n))   
        Modellines_exp[iModellines].SetTitle("%s_n%s_exp"%(M.ModelID,M.n))  
        Modellines_OneSig.append( TGraphAsymmErrors())
        Modellines_OneSig[iModellines].SetName("%s_n%s_OneSig"%(M.ModelID,M.n))   
        Modellines_OneSig[iModellines].SetTitle("%s_n%s_OneSig"%(M.ModelID,M.n))  
        Modellines_TwoSig.append( TGraphAsymmErrors())
        Modellines_TwoSig[iModellines].SetName("%s_n%s_TwoSig"%(M.ModelID,M.n))   
        Modellines_TwoSig[iModellines].SetTitle("%s_n%s_TwoSig"%(M.ModelID,M.n))  

        minMBH_obs= M.getMinMBH("Obs")
        minMBH_exp= M.getMinMBH("Exp")
        minMBH_OneSigP=max(M.getMinMBH("OneSigP"),M.getMinMBH("OneSigM"))
        minMBH_OneSigM=min(M.getMinMBH("OneSigP"),M.getMinMBH("OneSigM"))
        minMBH_TwoSigP=max(M.getMinMBH("TwoSigP"),M.getMinMBH("TwoSigM"))
        minMBH_TwoSigM=min(M.getMinMBH("TwoSigP"),M.getMinMBH("TwoSigM"))
        if not minMBH_obs==0.0:
            Modellines[iModellines].SetPoint(Modellines[iModellines].GetN(), M.MD/1000., minMBH_obs/1000.)
            Modellines_exp[iModellines].SetPoint(Modellines_exp[iModellines].GetN(), M.MD/1000., minMBH_exp/1000.)
            Modellines_OneSig[iModellines].SetPoint(     Modellines_OneSig[iModellines].GetN()  , M.MD/1000., minMBH_obs/1000.)
            Modellines_TwoSig[iModellines].SetPoint(     Modellines_TwoSig[iModellines].GetN()  , M.MD/1000., minMBH_obs/1000.)
            Modellines_OneSig[iModellines].SetPointError(Modellines_OneSig[iModellines].GetN()-1, 0, 0      , (minMBH_obs-minMBH_OneSigM)/1000., (minMBH_OneSigP-minMBH_obs)/1000.)
            Modellines_TwoSig[iModellines].SetPointError(Modellines_TwoSig[iModellines].GetN()-1, 0, 0      , (minMBH_obs-minMBH_TwoSigM)/1000., (minMBH_TwoSigP-minMBH_obs)/1000.)
        print "Adding Model line: %s_n%s" %(M.ModelID,M.n)
        print "MD=%s Min MBH=%s"% (M.MD, minMBH_obs)
        PlotTxt.write("For Model line  %s_n%s: \n" % (M.ModelID, M.n))
        PlotTxt.write("MD = %s   MinMBH = %s\n" % (M.MD, minMBH_obs))
    else:
        M_pre = Modelpoints[iModel-1]
        #print M_pre.MD,M_pre.MD, M.n,M_pre.n,M.ModelID,M_pre.ModelID

        #if model points differ only by MD, add the points to current Modellins
        if( M.MD != M_pre.MD and M.n == M_pre.n and M.ModelID == M_pre.ModelID):
            minMBH_obs = M.getMinMBH("Obs")
            minMBH_exp = M.getMinMBH("Exp")
            minMBH_OneSigP=max(M.getMinMBH("OneSigP"),M.getMinMBH("OneSigM"))
            minMBH_OneSigM=min(M.getMinMBH("OneSigP"),M.getMinMBH("OneSigM"))
            minMBH_TwoSigP=max(M.getMinMBH("TwoSigP"),M.getMinMBH("TwoSigM"))
            minMBH_TwoSigM=min(M.getMinMBH("TwoSigP"),M.getMinMBH("TwoSigM"))
            if not minMBH_obs==0.0:
                Modellines[iModellines].SetPoint(Modellines[iModellines].GetN(), M.MD/1000., minMBH_obs/1000.)
                Modellines_exp[iModellines].SetPoint(Modellines_exp[iModellines].GetN(), M.MD/1000., minMBH_exp/1000.)
                Modellines_OneSig[iModellines].SetPoint(     Modellines_OneSig[iModellines].GetN()  , M.MD/1000., minMBH_obs/1000.)
                Modellines_TwoSig[iModellines].SetPoint(     Modellines_TwoSig[iModellines].GetN()  , M.MD/1000., minMBH_obs/1000.)
                Modellines_OneSig[iModellines].SetPointError(Modellines_OneSig[iModellines].GetN()-1, 0, 0      , (minMBH_obs-minMBH_OneSigM)/1000., (minMBH_OneSigP-minMBH_obs)/1000.)
                Modellines_TwoSig[iModellines].SetPointError(Modellines_TwoSig[iModellines].GetN()-1, 0, 0      , (minMBH_obs-minMBH_TwoSigM)/1000., (minMBH_TwoSigP-minMBH_obs)/1000.)
            print "MD=%s Min MBH=%s"% (M.MD, minMBH_obs)
            PlotTxt.write("MD = %s   MinMBH = %s\n" % (M.MD, minMBH_obs))
        else:
            minMBH_obs = M.getMinMBH("Obs")
            minMBH_exp = M.getMinMBH("Exp")
            minMBH_OneSigP=max(M.getMinMBH("OneSigP"),M.getMinMBH("OneSigM"))
            minMBH_OneSigM=min(M.getMinMBH("OneSigP"),M.getMinMBH("OneSigM"))
            minMBH_TwoSigP=max(M.getMinMBH("TwoSigP"),M.getMinMBH("TwoSigM"))
            minMBH_TwoSigM=min(M.getMinMBH("TwoSigP"),M.getMinMBH("TwoSigM"))
            Modellines.append( TGraph())
            iModellines = iModellines+1
            Modellines[iModellines].SetName("%s_n%s"%(M.ModelID,M.n))   
            Modellines[iModellines].SetTitle("%s_n%s"%(M.ModelID,M.n))  

            Modellines_exp.append( TGraph())
            Modellines_exp[iModellines].SetName("%s_n%s_exp"%(M.ModelID,M.n))   
            Modellines_exp[iModellines].SetTitle("%s_n%s_exp"%(M.ModelID,M.n))  
            Modellines_OneSig.append( TGraphAsymmErrors())
            Modellines_OneSig[iModellines].SetName("%s_n%s_OneSig"%(M.ModelID,M.n))   
            Modellines_OneSig[iModellines].SetTitle("%s_n%s_OneSig"%(M.ModelID,M.n))  
            Modellines_TwoSig.append( TGraphAsymmErrors())
            Modellines_TwoSig[iModellines].SetName("%s_n%s_TwoSig"%(M.ModelID,M.n))   
            Modellines_TwoSig[iModellines].SetTitle("%s_n%s_TwoSig"%(M.ModelID,M.n))  


            if not minMBH_obs==0.0:
                Modellines[iModellines].SetPoint(Modellines[iModellines].GetN(), M.MD/1000., minMBH_obs/1000.)
                Modellines_exp[iModellines].SetPoint(Modellines_exp[iModellines].GetN(), M.MD/1000., minMBH_exp/1000.)
                Modellines_OneSig[iModellines].SetPoint(     Modellines_OneSig[iModellines].GetN()  , M.MD/1000., minMBH_obs/1000.)
                Modellines_TwoSig[iModellines].SetPoint(     Modellines_TwoSig[iModellines].GetN()  , M.MD/1000., minMBH_obs/1000.)
                Modellines_OneSig[iModellines].SetPointError(Modellines_OneSig[iModellines].GetN()-1, 0, 0      , (minMBH_obs-minMBH_OneSigM)/1000., (minMBH_OneSigP-minMBH_obs)/1000.)
                Modellines_TwoSig[iModellines].SetPointError(Modellines_TwoSig[iModellines].GetN()-1, 0, 0      , (minMBH_obs-minMBH_TwoSigM)/1000., (minMBH_TwoSigP-minMBH_obs)/1000.)
            print "Adding Model line: %s_n%s" %(M.ModelID,M.n)
            print "MD=%s Min MBH=%s"% (M.MD, minMBH_obs)
            PlotTxt.write("For Model line  %s_n%s: \n" % (M.ModelID, M.n))
            PlotTxt.write("MD = %s   MinMBH = %s\n" % (M.MD, minMBH_obs))
    iModel=iModel+1
iline =0
c1 = TCanvas("c1","c1",800,600)
for line in Modellines:
    line.SetLineColor(kBlue)
    line.SetMarkerStyle(kFullSquare)
    line.SetMarkerColor(kBlue)

    Modellines_exp[iline].SetLineColor(kBlack)
    Modellines_exp[iline].SetLineStyle(2)
    Modellines_exp[iline].SetMarkerStyle(kFullCircle)
    Modellines_exp[iline].SetMarkerColor(kBlack)

    Modellines_OneSig[iline].SetLineColor(kGreen+1)
    Modellines_OneSig[iline].SetFillColor(kGreen+1)
    Modellines_TwoSig[iline].SetLineColor(kOrange)
    Modellines_TwoSig[iline].SetFillColor(kOrange)

    leg = TLegend(0.7,0.7,0.9,0.9)
    leg.AddEntry( line,"Observed","lp")
    leg.AddEntry( Modellines_exp[iline],"Expected","lp")
    line.Draw("ALP")
    Modellines_exp[iline].Draw("LPsame")
    leg.Draw()
    print "Modelline name= %s"%line.GetName()
    line.GetXaxis().SetTitle("MD(TeV)")
    line.GetYaxis().SetTitle("Min MBH(TeV)")
    c1.SetName("%s_canvas"%line.GetName())
    c1.Update()
    c1.Write()
    line.Write()
    Modellines_exp[iline].Write()
    Modellines_OneSig[iline].Write()
    Modellines_TwoSig[iline].Write()
    c1.Clear()
    iline+=1
print "Found %i model lines" % len(Modellines)
####################################################
print "Start making plots ..."

### Stage 1: Set Styles ###
#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = ""
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

#### Stage 2: Draw multigraphs (one multigraph for ALL modelpoints) ###
#Zbi_mg   = TMultiGraph()
#StOpt_mg = TMultiGraph()
#NOpt_mg  = TMultiGraph()
#
##Zbi_mg.SetName("Zbi_mg")
##StOpt_mg.SetName("StOpt_mg")
##NOpt_mg.SetName("NOpt_mg")
##Zbi_mg.SetName("Zbi_mg")
##Zbi_mg.SetTitle(";MBH(TeV);Best Zbi")
##StOpt_mg.SetTitle(";MBH(TeV);ST Opt (GeV)")
##NOpt_mg.SetTitle(";MBH(TeV);N Opt")
#
##LegendPos:
#TR = [0.7,0.7,0.9,0.9]
#BR = [0.7,0.2,0.9,0.4]
#
##Add Graphs
#iColor=1
#
#drawTR = True
###Draw ZBI
#iColor=1
#
#drawTR = True
#for g in ZbiOpt_grph:
#   g.SetLineColor(iColor)
#   g.SetFillColor(0)
#   g.SetFillStyle(0)
#   g.SetMarkerStyle(2)
#   Zbi_mg.Add(g)   
#   iColor +=1
#Zbi_mg.Draw("AL*")
#if drawTR:
#   canvas.BuildLegend(TR[0],TR[1],TR[2],TR[3])
#else:
#   canvas.BuildLegend(BR[0],BR[1],BR[2],BR[3])
#Zbi_mg.GetXaxis().SetTitle("MBH(TeV)")
#Zbi_mg.GetYaxis().SetTitle("Best Zbi")
#Zbi_mg.GetYaxis().SetTitleOffset(1)    
#
##draw the lumi text on the canvas
#CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
#
#canvas.cd()
#canvas.Update()
#canvas.RedrawAxis()
#frame = canvas.GetFrame()
#frame.Draw()
#
#canvas.SetName("Zbi_mg")
#canvas.Update()
#canvas.Write()
######################################### 
###Draw StOpt
#iColor=1
#
#drawTR = True
#for g in StOpt_grph:
#   g.SetLineColor(iColor)
#   g.SetFillColor(0)
#   g.SetFillStyle(0)
#   g.SetMarkerStyle(2)
#   StOpt_mg.Add(g) 
#   iColor +=1
#StOpt_mg.Draw("AL*")
#if drawTR:
#   canvas.BuildLegend(TR[0],TR[1],TR[2],TR[3])
#else:
#   canvas.BuildLegend(BR[0],BR[1],BR[2],BR[3])
#StOpt_mg.GetXaxis().SetTitle("MBH(TeV)")
#StOpt_mg.GetYaxis().SetTitle("ST Opt (TeV)")
#StOpt_mg.GetYaxis().SetTitleOffset(1)  
#
##draw the lumi text on the canvas
#CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
#
#canvas.cd()
#canvas.Update()
#canvas.RedrawAxis()
#frame = canvas.GetFrame()
#frame.Draw()
#
#canvas.SetName("StOpt_mg")
#canvas.Update()
#canvas.Write()
########################################### 
###Draw NOpt
#iColor=1
#
#drawTR = True
#for g in NOpt_grph:
#   g.SetLineColor(iColor)
#   g.SetFillColor(0)
#   g.SetFillStyle(0)
#   g.SetMarkerStyle(2)
#   NOpt_mg.Add(g)  
#   iColor +=1
#NOpt_mg.Draw("AL*")
#if drawTR:
#   canvas.BuildLegend(TR[0],TR[1],TR[2],TR[3])
#else:
#   canvas.BuildLegend(BR[0],BR[1],BR[2],BR[3])
#NOpt_mg.GetXaxis().SetTitle("MBH(TeV)")
#NOpt_mg.GetYaxis().SetTitle("N Opt")
#NOpt_mg.GetYaxis().SetTitleOffset(1)   
#
##draw the lumi text on the canvas
#CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
#
#canvas.cd()
#canvas.Update()
#canvas.RedrawAxis()
#frame = canvas.GetFrame()
#frame.Draw()
#
#canvas.SetName("NOpt_mg")
#canvas.Update()
#canvas.Write()
########################################### 
### Stage 3: Draw limit curves(one multigraph for each modelpoint) ###
iColor=1

drawTR = True
for i in range(0,len(Exp_limit)):
    TwoSig_limit[i].SetFillColor(kOrange)
    TwoSig_limit[i].SetLineColor(kBlack)
    TwoSig_limit[i].SetLineWidth(2)
    TwoSig_limit[i].SetLineStyle(2)
    OneSig_limit[i].SetFillColor(kGreen+1)
    OneSig_limit[i].SetLineColor(kBlack)
    OneSig_limit[i].SetLineWidth(2)
    OneSig_limit[i].SetLineStyle(2)
    Exp_limit[i].SetLineWidth(2)
    Exp_limit[i].SetLineStyle(9)
    Obs_limit[i].SetLineWidth(2)
    Obs_limit[i].SetLineColor(1)
    Obs_limit[i].SetMarkerColor(1)
    Obs_limit[i].SetMarkerStyle(20)
    Obs_limit[i].SetMarkerSize(0.7)
    Xsec_grph[i].SetLineStyle(2)
    Xsec_grph[i].SetLineWidth(2)
    Xsec_grph[i].SetLineColor(kRed)

    canvas.SetLogy()    
    TwoSig_limit[i].GetXaxis().SetTitle("M_{BH} [TeV]")
    TwoSig_limit[i].GetYaxis().SetTitle("95% CL on #sigma [fb]")
    TwoSig_limit[i].GetYaxis().SetTitleOffset(1)
    TwoSig_limit[i].SetTitle("")
    TwoSig_limit[i].SetMinimum(ymin)
    TwoSig_limit[i].SetMaximum(ymax)
    TwoSig_limit[i].Draw("AE3L")
    OneSig_limit[i].Draw("sameE3")
    Exp_limit[i].Draw("sameL")
    Obs_limit[i].Draw("sameLP")
    Xsec_grph[i].Draw("sameL")

    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

    if Modelpoints[i].ModelID=="BH1":
        modelText = "BlackMax: Nonrotating BH"
    else:
        modelText = Modelpoints[i].ModelID
    
    leg= TLegend(0.65,0.65,0.9,0.9, "%s"%modelText, "brNDC")
    leg.AddEntry(Obs_limit[i],"Observed","LP")
    #leg.AddEntry(Exp_limit[i],"Expected","L")
    leg.AddEntry(OneSig_limit[i],"68% expected","lf")
    leg.AddEntry(TwoSig_limit[i],"95% expected","lf")
    leg.AddEntry(Xsec_grph[i],"M_{D} = %s TeV, n = %i"%(Modelpoints[i].MD/1000,Modelpoints[i].n),"L")
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.03)
    leg.Draw()

    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()

    #canvas.SetName("%s"% ZbiOpt_grph[i].GetTitle().replace("ZbiOpt_",""))
    canvas.SetName("%s"% Modelpoints[i].key)
    canvas.Update()
    canvas.Write()
