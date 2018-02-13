from ROOT import *

g = TGraph()
g.SetPoint(g.GetN(), 1,1)
g.SetPoint(g.GetN(), 2,2)
x=Double(0.0)
y=Double(0.0)
g.GetPoint(0, x,y)
print x,y
