#!/bin/bash

source /afs/cern.ch/project/eos/installation/cms/etc/setup.sh

#DIR=`echo /store/group/phys_exotica/BH_RunII/BlackMax_NTuple/`
#DIR=`echo /store/group/phys_exotica/BH_RunII/SB_Ntuple_Final/`
#DIR=`echo /store/group/phys_exotica/BH_RunII/QBH_ADD_NTuple/`
DIR=`echo /store/group/phys_exotica/BH_RunII/QBH_RS1_NTuple/`

Files=`eos ls $DIR`
#Files=`eos ls $DIR | grep BlackMaxLHArecord_SB_MD1640_MBH5500_n6_NTuple.root`
#Files=`eos ls $DIR | grep QBH_MD_RS1_5_MQBH_5_n_1_NTuple.root`

#root -l -q 'BHflatTuplizer.cc+("root://eoscms.cern.ch//store/group/phys_exotica/BH_RunII/BlackMax_NTuple/BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n4_NTuple.root","BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n4_FlatTuple.root","METfilteredEvents_Feb02.txt")'

for f in $Files
do 
	echo "Processing $f"
	outname=`echo $f | sed 's/NTuple/FlatTuple/'`
	log='_log.tx'
	if  [ ! -f $outname ] && [ ! -f ./SignalFlatTuple/$outname ]
	then 
		#eval $'root -l -q \'BHflatTuplizer.cc+("root://eoscms.cern.ch/'"$DIR$f"$'\",\"'$outname$'\",\"empty.txt\")\''
		eval $'root -l -q \'BHflatTuplizer.cc+("./eos/cms/'"$DIR$f"$'\",\"'$outname$'\",\"empty.txt\")\''
		mv $outname ./SignalFlatTuple
		rm $outname$log
	else
		echo "... File already exist! Skipping"
	fi
done
