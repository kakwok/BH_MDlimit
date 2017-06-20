# Given a list of flatTuple, add all ST histograms 

from ROOT import *
import glob

def Findweight(pDataSet,Lumi,Xsection):
    xsecFile = open(Xsection,"r")
    weight   = 1
    for line in xsecFile:
        if(not "#" in line):
            line = line.strip().split()
            dataSetName = line[0]
            Nevent      = float(line[1])
            xsec        = float(line[2])
            if(dataSetName == pDataSet):
                weight  = (xsec * Lumi*1000)/Nevent
                print "%s   Weight =%s " %(pDataSet,weight)
                break
    xsecFile.close()
    return weight

pathToFlatTuples = "/afs/cern.ch/user/k/kakwok/work/public/Blackhole/BH2016/flatTuple/QCD/" 
QCDflatTuples = glob.glob("%s*.root"%pathToFlatTuples)
Xsection   = "Pythia_xsec.txt"
Lumi       = 35.8 

flat_dict   = {}   # {hname:TH1, hname2:TH1, ...}}
ST_dict     = {}   # {hname:TH1, hname2:TH1, ...}
mBH_dict    = {}   # {hname:TH1, hname2:TH1, ...}

for flatTuple in QCDflatTuples:
    #fname    = BHflatTuple_QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_Moriond17_May11_70GeV.root 
    #pDataSet = QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8
    fname     = flatTuple.split("/")[-1]
    pDataSet  = fname.replace("BHflatTuple_","").replace("_"+fname.split("_")[-1],"").replace("_"+fname.split("_")[-2],"").replace("_"+fname.split("_")[-3],"")
    rootFile  = TFile.Open(flatTuple)
    weight   = Findweight(pDataSet,Lumi,Xsection)

    # FlatHistogram
    for key in rootFile.GetListOfKeys():
        if( "TH1" in key.GetClassName()):
            hist      = rootFile.Get(key.GetName())
            hist_name = key.GetName()
            hist.SetDirectory(0)
            if hist_name in flat_dict:
                flat_dict[hist_name].Add(hist,weight)
            else:
                hist.Scale(weight)
                flat_dict[hist_name] = hist 

    #print fname, pDataSet
    for key in rootFile.Get("ST").GetListOfKeys():
        if( "TH1" in key.GetClassName()):
            ST_hist      = rootFile.Get("ST").Get(key.GetName())
            ST_hist_name = key.GetName()
            ST_hist.SetDirectory(0)
            if ST_hist_name in ST_dict:
                ST_dict[ST_hist_name].Add(ST_hist,weight)
            else:
                ST_hist.Scale(weight)
                ST_dict[ST_hist_name] = ST_hist 
    #print fname, pDataSet
    for key in rootFile.Get("m_BH").GetListOfKeys():
        if( "TH1" in key.GetClassName()):
            mBH_hist      = rootFile.Get("m_BH").Get(key.GetName())
            mBH_hist_name = key.GetName()
            mBH_hist.SetDirectory(0)
            if mBH_hist_name in mBH_dict:
                mBH_dict[mBH_hist_name].Add(mBH_hist,weight)
            else:
                mBH_hist.Scale(weight)
                mBH_dict[mBH_hist_name] = mBH_hist
                
outputRoot = TFile("QCD_weighted.root","RECREATE")

for hname in sorted(flat_dict.iterkeys()):
    h = flat_dict[hname].Clone()
    print "Writing %s in ST"%(hname)
    outputRoot.Write(h.GetName())
#Write the histograms
outputRoot.mkdir("ST")
outputRoot.mkdir("m_BH")
outputRoot.cd("ST")
for hname in sorted(ST_dict.iterkeys()):
    h = ST_dict[hname].Clone()
    print "Writing %s in ST"%(hname)
    outputRoot.Write(h.GetName())
outputRoot.cd("m_BH")
for hname in sorted(mBH_dict.iterkeys()):
    h = mBH_dict[hname].Clone()
    print "Writing %s in mBH"%(hname)
    outputRoot.Write(h.GetName())
outputRoot.Close()
