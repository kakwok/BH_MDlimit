import os

def getMI(Stmin,Nmin,MILimit):
	MIdata =[]
	StRound = round(float(Stmin)/500,0)*500
	#print "Required for STmin = %s, Searching for STmin=%s in MIlimit" %(Stmin,StTar)
	for StTar in [Stmin,StRound]:
		if(os.path.exists("%s"%MILimit)):
			MIFile = open("%s"%MILimit,"r")
			next(MIFile)
			for line in MIFile:
				line = line.strip()
				n     = line.split()[0].replace(" ","")
				St    = line.split()[1].replace(" ","")
				Obs   = line.split()[2].replace(" ","")
				m2Sig = line.split()[3].replace(" ","")
				m1Sig = line.split()[4].replace(" ","")
				Exp   = line.split()[5].replace(" ","")
				p1Sig = line.split()[6].replace(" ","")
				p2Sig = line.split()[7].replace(" ","")
				if( float(n)==float(Nmin) and float(St) ==float( StTar)):
					MIdata.append(float(St))
					MIdata.append(float(Obs))
					MIdata.append(float(m2Sig))
					MIdata.append(float(m1Sig))
					MIdata.append(float(Exp))
					MIdata.append(float(p1Sig))
					MIdata.append(float(p2Sig))
			if MIdata:
				return MIdata
		else:
			print "Cannot find MILimit input file"
			break
	if not MIdata:
		print "Cannot find matching ST and N in MI limit! Requested Nmin=%s, STmin=%s"%(Nmin,Stmin)
		return [StTar,999,999,999,999,999,999]	

