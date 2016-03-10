# Class for making a mass point on the MD plot
# Initialize the class by giving 1) ModelID 2) MD 3)n
# Each Modelpoint object should contain:
# A list of lines like this:
#  Model  MD   MBH  n  | STMin   Nmin      Zbi      Nsignal     Xsec(fb)    Acept  | StLimit  Nobs | xsec(fb): Obs -2sig -1sig Exp +1sig +2sig
#  SB  1490  6000 6  3900 8 7.749 51.601010 30.000000  0.75990 4000.0 6.413 3.785 4.698 6.465 8.889 12.151 
# Martin Kwok, 19/2/2016

from ROOT import *
from math import *


class Modelpoint:
	def __init__(self, ModelID, MD, n):
		self.ModelID = ModelID
		self.MD      = MD
		self.n       = n
		self.key     = str(ModelID)+"_MD"+str(MD)+"_n"+str(n)
		self.linekey = str(ModelID)+"_n"+str(n)
		self.datalist=[]
		self.Zbi_graph = TGraph()

	def addData(self,data):
		self.datalist.append(data)

	def printData(self):
	#data   = [MBH, Stmin, nmin, Zbi,signal,Xsec,accpt,Stlimit,Obs,m2sig,m1sig,Exp,p1sig,p2sig]
		for data in self.datalist:
			print data
	def addZbiGraph(self,g):
		self.Zbi_graph = g
	def getZbiGraph(self):
		return self.Zbi_graph
	def getMinMBH(self,ObsOrExp):
		Extrapolate=0
		#       MBH  Xsec(th) Xsec(limit)
		last = []
		MBHminData = self.datalist[0]
		for data in self.datalist:
			if( "Obs" in ObsOrExp):
				new = [data[0], data[5],data[8]]	
			elif ("Exp" in ObsOrExp):
				new = [data[0], data[5],data[11]]	
				
			if data == self.datalist[0]:
				last=new
				continue
			# Extrapolate if: Theoretical xsec in last step is excluded, but in this step cannot be excluded
			#  [0] = MBH  [1] = Xsec(Theory)  [2] = Xsec(Limit)
			if (last[1]>last[2] and new[1]<new[2]):
				#print "%s %s %s %s %s %s" %(last[0],last[1],last[2], new[0],new[1],new[2])
				m_theory = (log(new[1],10)-log(last[1],10))/(new[0]-last[0])	
				m_limit =  (log(new[2],10)-log(last[2],10))/(new[0]-last[0])	
				Extrapolate = last[0] + (log(last[1],10)-log(last[2],10))/(m_limit-m_theory)
				#print "new = ",new
				#print "last=", last
				#print "Last MBH  =%s    Delta = %s" % ( last[0], (last[1]-last[2])/(m_limit-m_theory) )
				return float(Extrapolate)
			else:
				last=new 
		if Extrapolate==0:
			print "Cannot find MinMBH for %s"%self.key
			return float(Extrapolate)
