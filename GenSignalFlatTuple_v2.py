import os
import glob

#Topdir="/mnt/hadoop/store/user/johakala/BlackMax/"
#Topdir="/mnt/hadoop/store/user/johakala/Charybdis_2/"
#Topdir="/mnt/hadoop/users/mkwok/NTuple/"
Topdir="/afs/cern.ch/user/k/kakwok/eos/cms/store/user/kakwok/BH/Signal2016/Charybdis/"
#Topdir="/afs/cern.ch/user/k/kakwok/eos/cms/store/user/kakwok/BH/NTuple/Charybdis/"
#Topdir="/afs/cern.ch/user/k/kakwok/eos/cms/store/user/kakwok/BH/NTuple/SB_charybdis/"
#Topdir="/afs/cern.ch/user/k/kakwok/eos/cms/store/group/phys_exotica/BH_RunII/SB_Ntuple_Final/"

folder_list= os.listdir(Topdir)
flist= glob.glob("%s/*BH2_*.root"%(Topdir))
#outdir="SignalFlatTuple/BM_fullsim"
#outdir="SignalFlatTuple/Charybdis/"
#outdir="SBcheck/"
#outdir="SignalFlatTuple/SB_charybdis/"
#outdir="SignalFlatTuple/Charybdis/BH6_fixed/"
outdir="SignalFlatTuple_2016/Charybdis/"

run  = False

for f in flist:
        outname= outdir+f.split("/")[-1].replace("NTuple","FlatTuple")
        #outname= outdir+dir.replace("NTuple","FlatTuple")

        print "Working on %s now ... "%outname
        #print "root -l -q 'BHflatTuplizer.cc+(\"%s\",\"%s\",\"empty.txt\")'"% (f, outname)
        #cmd="root -l -q 'BHflatTuplizer.cc+(\"%s\",\"%s\",\"empty.txt\")'"% (Topdir+dir, outname)
        cmd="root -l -q 'BHflatTuplizer.cc+(\"%s\",\"%s\",\"empty.txt\",false,70)'"% (f, outname)
        if not run:
                print cmd
        else:
                print cmd
                os.system(cmd)
