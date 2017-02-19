from ROOT import *
from hPlus import *
from style import *
import glob
def DrawSameFromList(hTitle,hlist):
	ymins = []
	ymaxs = []
	for h in hlist:
		h.setStyle()
		h.setLabel()
		ymins.append( h.getTH1().GetMinimum() )
		ymaxs.append( h.getTH1().GetMaximum() )
		legend.AddEntry(h.getTH1(),h.getTH1().GetName(),"l")
	hlist[0].getTH1().SetMaximum( max(ymaxs)*1.2 )
	hlist[0].getTH1().GetXaxis().SetRangeUser(1500,13000)
	if (not min(ymins)==0):	
		hlist[0].getTH1().SetMinimum( min(ymins) )
	else:
		hlist[0].getTH1().SetMinimum( min(ymins)+1E-1 )
	hlist[0].getTH1().SetTitle(hTitle)
	hlist.pop(0).getTH1().Draw()
	for h in hlist:
		print h.getTH1().GetName(),h.getTH1().GetMean(1)
		h.getTH1().Draw("Same")
	legend.SetTextFont(42)
	legend.SetTextSize(0.03)
	legend.Draw()
	#c1.BuildLegend(0.7,0.7,0.9,0.9)
	
# Loop through a list of hPlus, print it into a pdf file
# histo_Dict:
# key hname, value list of hPlus objects from flist with name hTitle
def makepdf(pages,outputFile):
	nItems = len(pages)
	i      = 1
	nPad   = 1
	nPages = 0
	IsLast = False
	for page in pages:
		# Prepare the canvas
		DrawSameFromList(page["Title"],page["list"])
		# Open a new page
		if(nPages==0): 
			if(int(nItems/nPad)==1):
				c1.Print(outputFile,"pdf")
			else:
				c1.Print(outputFile+"(","pdf")
		if(i == nItems):
			c1.Print(outputFile+")","pdf")
			IsLast = True
		else:
			if(nPages!=0 and IsLast==False):
				 c1.Print(outputFile,"pdf")
		nPages+=1
		i+=1
		nPad = 1
		c1.Clear()
		legend.Clear()
	#print IsLast
	if(IsLast==False): 
		c1.Print(outputFile+")","pdf")

# input: List of dicts{fname,hname}, hKey
# fname = name of file,   hname = name of histo label
# hKey  = historgram name in each files
def getHlistFromFiles(flist,hKey,xLabel,yLabel):
	hlist =[]
	istyle=0
	for f in flist:
		rootfile = TFile(f['fname'])
		#rootfile.ls()
		hist     = rootfile.Get(hKey)
		hist.SetDirectory(0)
		label    = {'Name':f['hname'],'x':xLabel,'y':yLabel}
		hlist.append(hPlus(hist,style(istyle),label))
		istyle= istyle+1
	return hlist
###################################################################
#./SBcheck/BlackMaxLHArecord_SB_MD1640_MBH8500_n6_FlatTuple.root
#Topdir="./SBcheck"
##flist= glob.glob("%s/*MD2380*n6*.root"%(Topdir))
#flist= glob.glob("%s/*MD1640*n6*.root"%(Topdir))
#flistOfDict=[]
#for f in flist:
#	histname = f.split("/")[len(f.split("/"))-1].replace("_FlatTuple.root","")
#	fdict = {'fname':f,'hname': histname}
#	if (len(flistOfDict)>=9): continue
#	if "MBH5000" in histname: continue
#	flistOfDict.append(fdict)
#page1 = getHlistFromFiles(flistOfDict,"mBH","M_BH/GeV","N")
#page2 = getHlistFromFiles(flistOfDict,"NJets","N Jet","N")

#StringBall_MD11030_MBH5000_MS2000_gs05_n6_blackmax_FlatTuple.root
f1 ="./JEC/BHflatTuple_2016_BtoG_reRECO.root"
f2 ="./JEC/BHflatTuple_2016BtoG_JetID.root"
f3 ="./JEC/BHflatTuple_2016BtoG_JetID_40GeV.root"
f4 ="./JEC/BHflatTuple_2016BtoG_JetID_30GeV.root"
f5 ="./JEC/BHflatTuple_2016BtoG_JetID_60GeV.root"
f6 ="./JEC/BHflatTuple_2016BtoG_JetID_70GeV.root"
flistOfDict=[]
flistOfDict.append({'fname':f1,'hname':"2016_reRECO"})
flistOfDict.append({'fname':f2,'hname':"2016_JEC+50GeV"})
flistOfDict.append({'fname':f3,'hname':"2016_JEC+40GeV"})
flistOfDict.append({'fname':f4,'hname':"2016_JEC+30GeV"})
flistOfDict.append({'fname':f5,'hname':"2016_JEC+60GeV"})
flistOfDict.append({'fname':f6,'hname':"2016_JEC+70GeV"})

Pages=[]
for i in range(2,10):
	page = getHlistFromFiles(flistOfDict,"ST/stExc%02iHist"%i,"ST/GeV","N")
	Pages.append({'Title':"ST(N=%s)"%i,"list":page})
for i in range(2,10):
	page = getHlistFromFiles(flistOfDict,"ST/stInc%02iHist"%i,"ST/GeV","N")
	Pages.append({'Title':"ST(N>=%s)"%i,"list":page})


c1 = TCanvas("c1","c1",800,600)
legend = TLegend(0.6,0.7,0.9,0.9, "", "brNDC")
gStyle.SetOptStat(0)
c1.SetLogy(1)
#Pages = [
#{'Title':"ST(N>=2 )","list":page1},
#]
makepdf(Pages, "2016BtoG_JEC.pdf")
