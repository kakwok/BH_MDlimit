from ROOT import *

f = TFile("StOpt_SBextra_edited_plot.root")
g = f.Get("SB_n6")
g.Draw("AP*")
g.GetXaxis().SetTitle("MD (GeV)")
g.GetYaxis().SetTitle("Min MBH (GeV)")
g.SetTitle("")
leg= TLegend(0.6,0.6,0.9,0.9, "String Ball", "brNDC")
leg.AddEntry(g,"MS=1.1TeV gs=0.2, n=6","p")
leg.Draw()
leg.SetTextFont(42);
leg.SetTextSize(0.03);

c1.SaveAs("MDFinal.pdf")
