from GetMI import *

IntLumi =  2263.5

MILimit="MILimits.txt"
#MIplotTable=open("MIplotData.txt","w")
MIplotTable=open("MIplotData.oldhepdata","w")
MIplotTable.write("nMin STmin[GeV]    Obs_UL      -2Sig    -1Sig      Exp_UL   +1Sig     +2Sig [xsection in fb]\n")
for i in range(2,11):
    if (i==2 or i==3):
        lowerBound = 25
    elif(i==4 or i==5 or i==6 or i==7):
        lowerBound = 27
    else:
        lowerBound = 30
    for stmin in range(lowerBound,81):
        midata   = getMI(stmin*100, i , MILimit) 
        norm     = float((IntLumi/1000.))
        if not float("999") in midata:
            dataString = "%i;"%i
            for j,data in enumerate(midata):
                if j>0:
                    data = data/norm
                    if not j==len(midata): 
                        dataString += " {:>7.2f};".format(data) 
                    else:
                        dataString += " {:>7.2f}".format(data) 
                else:
                    dataString += " %s;"%data
            dataString +="\n"
            MIplotTable.write(dataString)
        
