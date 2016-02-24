##
##  This macro takes 1)The file name of signal FLAT tuple 2) Cross section database txt 
##  to return a list containing
##  1) MD of the current signal file 
##  2) MBH of the current signal file 
##  3) Xsec of the current signal file (in pb)
## 
##  by Martin Kwok 23 Feb 2016


import os


def getXsec(signal , lookupfiles, modelClass):
	masspoint = []
	if(os.path.exists("./SignalFlatTuple/%s"%signal)and os.path.exists(lookupfiles)):
		if(modelClass=="BM"):
			#format: BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n6_FlatTuple.root
			Model=signal.split("_")[1]
			MD = signal.split("_")[3]
			MBH= signal.split("_")[4]
			n  = signal.split("_")[5]
			masspoint.append(Model)
			masspoint.append(float(MD.replace("MD","")))
			masspoint.append(float(MBH.replace("MBH","")))
			masspoint.append(float(n.replace("n","")))
			Found = False
			print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
			File = open(lookupfiles,"r")
			for line in File:
				# format: /afs/cern.ch/user/b/belotel/work/public/BH/BH1_BM_MD2000_MBH10000_n4/BlackMaxLHArecord.lhe      1.5742500E-04
				path = line.split("\t")[0]
				xsec  = line.split("\t")[1]
				key = path.split("/")[9]
				if (key.split("_")[2]==MD and key.split("_")[3]==MBH and key.split("_")[4]==n and key.split("_")[0]==Model):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
		if(modelClass=="SB"):
			#format: BlackMaxLHArecord_SB_MD1640_MBH9500_n6_FlatTuple.root
			Model=signal.split("_")[1]
			MD   =signal.split("_")[2]
			MBH  =signal.split("_")[3]
			n    =signal.split("_")[4]
			Found = False
			masspoint.append(Model)
			masspoint.append(float(MD.replace("MD","")))
			masspoint.append(float(MBH.replace("MBH","")))
			masspoint.append(float(n.replace("n","")))

                        print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
                        File = open(lookupfiles,"r")
			for line in File:
				# format: StringBall_MD1640_MBH6500_MS1100_gs02_n2_13TeV_TuneCUETP8M1-blackmax    1.02E-01
				key = line.split("\t")[0]
				xsec= line.split("\t")[1]
				if (key.split("_")[1]==MD and key.split("_")[2]==MBH and key.split("_")[5]==n ):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
		if("QBH" in modelClass and "ADD" in modelClass): 
			# format: QBH_MD_9_MQBH_12_n_6_FlatTuple.root
			Model=signal.split("_")[0]
			MD = signal.split("_")[2]
			MBH= signal.split("_")[4]
			n  = signal.split("_")[6]
			masspoint.append(Model)
			masspoint.append( float(MD)*1000 )
			masspoint.append( float(MBH)*1000)
			masspoint.append( int(n)  )
			Found = False
			print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
			File = open(lookupfiles,"r")
			for line in File:
				# format: /eos/cms/store/group/phys_exotica/QBH_LHE_John/MD_4_MQBH_4_n_1/LHEFfile.lhe     3.35E+00
				path = line.split("\t")[0]
				xsec  = line.split("\t")[1]
				key = path.split("/")[6]
				if (key.split("_")[1]==MD and key.split("_")[3]==MBH and key.split("_")[5]==n ):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
		if("QBH" in modelClass and "RS1" in modelClass): 
			# format: QBH_MD_RS1_9_MQBH_10_n_1_FlatTuple.root
			Model=signal.split("_")[0]+"_RS1"
			MD = signal.split("_")[2]
			MBH= signal.split("_")[4]
			n  = signal.split("_")[6]
			masspoint.append(Model)
			masspoint.append( float(MD)*1000 )
			masspoint.append( float(MBH)*1000)
			masspoint.append( int(n)  )
			Found = False
			print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
			File = open(lookupfiles,"r")
			for line in File:
				# format: /eos/cms/store/group/phys_exotica/QBH_LHE_John/MD_4_MQBH_4_n_1/LHEFfile.lhe     3.35E+00
				path = line.split("\t")[0]
				xsec  = line.split("\t")[1]
				key = path.split("/")[6]
				if (key.split("_")[1]==MD and key.split("_")[3]==MBH and key.split("_")[5]==n ):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
	
	else:
		print "Signal files /look up file missing OR wrong modelClass input"
		return;


