# Class  define style for hPlus

from ROOT import *

class style:
	def setFromDict(self,styledict):
		self.color     = styledict['color']	
		self.FillStyle = styledict['FillStyle']	
	def setColor(self,Color):
		self.color = Color	
	def __init__(self,n):
		dict1={'color':kBlack,'FillStyle':0}
		dict2={'color':kRed,'FillStyle':0}
		dict3={'color':kBlue,'FillStyle':0}
		dict4={'color':kGreen,'FillStyle':0}
		dict5={'color':kViolet,'FillStyle':0}
		dict6={'color':kCyan,'FillStyle':0}
		dict7={'color':kPink,'FillStyle':0}
		dict8={'color':kOrange,'FillStyle':0}
		dict9={'color':kMagenta,'FillStyle':0}
		dictList =[dict1,dict2,dict3,dict4,dict5,dict6,dict7,dict8,dict9]
		self.color     = kBlack
		self.FillStyle = 0
		self.setFromDict(dictList[n])
        def getColor(self):
                return self.color
#ikWhit 0,   kBlack  = 1,   kGray    = 920,  kRed    = 632,  kGreen  = 416,
#kBlue   = 600, kYellow = 400, kMagenta = 616,  kCyan   = 432,  kOrange = 800,
#kSpring = 820, kTeal   = 840, kAzure   =  860, kViolet = 880,  kPink   = 900
