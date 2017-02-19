# Class to include a TH1 with style

from ROOT import *
from style import *
class hPlus:
	def __init__(self, histo, style,label):
		self.histo = histo
		self.style = style
		self.label = label

	def setStyle(self):
		self.histo.SetLineColor ( self.style.color )
		self.histo.SetMarkerColor( self.style.color )
		self.histo.SetFillColor ( 0 )
		#self.histo.SetFillColor ( self.style.color )
		self.histo.SetFillStyle ( self.style.FillStyle )
	#For update style
	#def setStyle(self,style):
	#	self.histo.SetLineColor ( style.color )
	#	self.histo.SetMakerColor( style.color )
	#	self.histo.SetFillColor ( style.color )
	#	self.histo.SetFillStyle ( style.FillStyle )
		
	def setLabel(self):
		self.histo.SetName(self.label['Name'])
		self.histo.SetTitle(self.label['Name'])
		self.histo.GetXaxis().SetTitle(self.label['x'])
		self.histo.GetYaxis().SetTitle(self.label['y'])
	#Return histo
	def getTH1(self):
		return self.histo

