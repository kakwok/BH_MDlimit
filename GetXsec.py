##
##  This macro takes 1)The file name of signal FLAT tuple 2) Cross section database txt 
##  to return a list containing
##  1) MD of the current signal file 
##  2) MBH of the current signal file 
##  3) Xsec of the current signal file (in pb)
## 
##  by Martin Kwok 23 Feb 2016


import os


def getXsec(PathAndFile , lookupfiles, modelClass):
	masspoint = []
	if(os.path.exists(PathAndFile)and os.path.exists(lookupfiles)):
	#if(os.path.exists("./SignalFlatTuple/%s"%signal)and os.path.exists(lookupfiles)):
		signal = PathAndFile.split("/")[2]
		#if(modelClass=="BM"):
		if("BM" in modelClass):
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
		if("CYBD" in modelClass):
			#format: Charybdis_BH2_BM_MD2000_MBH10000_n4_FlatTuple.root
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
				# format: BlackHole_BH9_MD7000_MBH9000_n6_13TeV_TuneCUETP8M1-charybdis
				xsec  = line.split()[1]
				key   = line.split()[0]
				if (key.split("_")[2]==MD and key.split("_")[3]==MBH and key.split("_")[4]==n and key.split("_")[1]==Model):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"

		if(modelClass=="SB"):
			#format: BlackMaxLHArecord_SB_MD1640_MBH9500_n6_FlatTuple.root
			#StringBall_MD11030_MBH5000_MS2000_gs05_n6_blackmax_FlatTuple.root 
			#StringBall_MD11030_MBH5000_MS2000_gs05_n6_charybdis_FlatTuple.root 
			Model="SB"
			if "BlackMaxLHArecord" in signal:
				MD   =signal.split("_")[2]
				MBH  =signal.split("_")[3]
				n    =signal.split("_")[4]
				if (MD=="MD1640"):
					MD="MD7630"
				if (MD=="MD1490"):
					MD="MD6890"
				if (MD=="MD1890"):
					MD="MD8750"
				if (MD=="MD2380"):
					MD="MD11030"
			if "StringBall" in signal:
				MD   =signal.split("_")[1]
				MBH  =signal.split("_")[2]
				n    =signal.split("_")[5]
			Found = False
			masspoint.append(Model)
			masspoint.append(float(MD.replace("MD","")))
			masspoint.append(float(MBH.replace("MBH","")))
			masspoint.append(float(n.replace("n","")))

                        print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
                        File = open(lookupfiles,"r")
			for line in File:
				# old format: StringBall_MD1640_MBH6500_MS1100_gs02_n2_13TeV_TuneCUETP8M1-blackmax    1.02E-01
				# new format: StringBall_MD11030_MBH5000_MS2000_gs05_n6_blackmax                  7.0913174e-01
				key = line.split("\t")[0]
				xsec= line.split("\t")[1]
				if (key.split("_")[1]==MD and key.split("_")[2]==MBH and key.split("_")[5]==n ):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
		if("QBH" in modelClass and "ADD" in modelClass): 
			# format: QBH_MD_9_MQBH_12_n_6_FlatTuple.root
			Model=signal.split("_")[0]+"_ADD"
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
				# format: /store/group/phys_exotica/QBH_LHE_ADD/MD_4_MQBH_4_n_1     3.35E+00
				path = line.split("\t")[0]
				xsec  = line.split("\t")[1]
				key = path.split("/")[5]
				if (key.split("_")[1]==MD and key.split("_")[3]==MBH and key.split("_")[5]==n ):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
		if("QBH" in modelClass and "RS1" in modelClass): 
			# format: QBH_MD_RS1_9_MQBH_10_n_1_FlatTuple.root
			Model=signal.split("_")[0]+"_RS1"
			MD = signal.split("_")[3]
			MBH= signal.split("_")[5]
			n  = signal.split("_")[7]
			masspoint.append(Model)
			masspoint.append( float(MD)*1000 )
			masspoint.append( float(MBH)*1000)
			masspoint.append( int(n)  )
			Found = False
			print "Looking for x sec of model=%s MD=%s, MBH=%s, n=%s" % (Model,MD,MBH,n)
			File = open(lookupfiles,"r")
			for line in File:
				# format: /store/group/phys_exotica/QBH_LHE_RS1/MD_4_MQBH_4_n_1     3.35E+00
				path = line.split("\t")[0]
				xsec  = line.split("\t")[1]
				key = path.split("/")[5]
				if (key.split("_")[1]==MD and key.split("_")[3]==MBH and key.split("_")[5]==n ):
					masspoint.append(float(xsec))
					return masspoint;
			if(not Found):
				print "Cannot find matching mass point in the x-section DB"
	
	else:
		print "Signal files /look up file missing OR wrong modelClass input"
		return;


