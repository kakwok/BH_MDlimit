import os
import glob

#Topdir="/mnt/hadoop/store/user/johakala/BlackMax/"
Topdir="/mnt/hadoop/store/user/johakala/Charybdis_2/"

folder_list= os.listdir(Topdir)
#outdir="SignalFlatTuple/BM_fullsim"
outdir="SignalFlatTuple/Charybdis"

run  = True

f_list=[]
merged_list=[]
missing_list=[]
for dir in folder_list:
	flist1= glob.glob("%s%s/*/160309*/*/*.root"%(Topdir,dir))
	flist2= glob.glob("%s%s/*/160304*/*/*.root"%(Topdir,dir))
	if len(flist1)>=2:
		merged = False
		MergedName=""
		for f in flist1:
			print f
			if "all" in f:
				MergedName=f
				merged= True
		if not merged:
	
			cmd_tail = ""
			for f in flist1:
				cmd_tail += f+" "
			key = flist1[0].split("/")[7]
			BH  = key.split("_")[1]	
			MD   = "MD%s"%key.split("_")[2].replace("MD-","")
			MBH  = "MBH%s"%key.split("_")[3].replace("MBH-","")
			n    = "n%s"%key.split("_")[4].replace("n-","")
			outname ="Charybdis_%s_BM_%s_%s_%s_NTuple.root" %(BH,MD,MBH,n)

			cmd_head = "hadd -f0 ./mergedTuple/%s "%(outname)
			cmd = cmd_head+ cmd_tail
			print "Merging output files..."
			if not run:
				print cmd
			else:
				os.system(cmd)
			merged_list.append("./mergedTuple/%s"%outname)
		else:
			f_list.append(MergedName)
	elif flist1:
		f_list.append(flist1[0])
	if (not flist1):
		for f in flist2:
			if os.path.exists(f):
				f_list.append(f)
		#		print f
	if (not flist1) and (not flist2):
		missing_list.append(dir)
#f = /mnt/hadoop/store/user/johakala/BlackMax/BlackHole_BH5_MD-9000_MBH-11000_n-6_TuneCUETP8M1_13TeV-blackmax/BHnTuples_-BlackHole_BH5_MD-9000_MBH-11000_n-6_TuneCUETP8M1_13TeV-blackmax-RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1-MINIAODSIM/160307_155719/0000/ntuple_output_1.root
# /mnt/hadoop/store/user/johakala/Charybdis_2/BlackHole_BH9_MD-3000_MBH-11000_n-6_TuneCUETP8M1_13TeV-charybdis/BHnTuples_-BlackHole_BH9_MD-3000_MBH-11000_n-6_TuneCUETP8M1_13TeV-charybdis-RunIISpring15MiniAODv2-Asympt25ns_74X_mcRun2_asymptotic_v2-v1-MINIAODSIM/160309_205014/0000/

#outname = BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n6_FlatTuple.root

for f in f_list:
	#print f
	key = f.split("/")[7]
	BH  = key.split("_")[1]	
	MD   = "MD%s"%key.split("_")[2].replace("MD-","")
	MBH  = "MBH%s"%key.split("_")[3].replace("MBH-","")
	n    = "n%s"%key.split("_")[4].replace("n-","")
	outname ="%s/Charybdis_%s_BM_%s_%s_%s_FlatTuple.root" %(outdir,BH,MD,MBH,n)
	
	print "Working on %s now ... "%outname
	#print "root -l -q 'BHflatTuplizer.cc+(\"%s\",\"%s\",\"empty.txt\")'"% (f, outname)
	cmd="root -l -q 'BHflatTuplizer.cc+(\"%s\",\"%s\",\"empty.txt\")'"% (f, outname)
	if not run:
		print cmd
	else:
		os.system(cmd)
for f in merged_list:
	fname = f.split("/")[2].replace("NTuple","FlatTuple")
	outname ="%s/%s" % ( outdir, fname)
	cmd="root -l -q 'BHflatTuplizer.cc+(\"%s\",\"%s\",\"empty.txt\")'"% (f, outname)
	if not run:
		print cmd
	else:
		os.system(cmd)
	
print "Found %i simple samples"%(len(f_list))
print "Found %i samples need to merge"%(len(merged_list))
print " %s masspoint has no ROOT file in %s" %( len(missing_list), Topdir)
for f in missing_list:
	print f
#if len(outname_list) > len(set(outname_list)):
#	print "double"
#for name1 in set(outname_list):
#	nfound=0
#	for name2 in outname_list:
#		if( name1==name2):
#			nfound+=1
#	if nfound>1:
#		print "%s  %s" %(name1,nfound)



