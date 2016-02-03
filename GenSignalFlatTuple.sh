#!/bin/bash

source /afs/cern.ch/project/eos/installation/cms/etc/setup.sh

DIR=`echo /store/group/phys_exotica/BH_RunII/BlackMax_NTuple/`
Files=`eos ls /store/group/phys_exotica/BH_RunII/BlackMax_NTuple/`
#Files=`eos ls /store/group/phys_exotica/BH_RunII/BlackMax_NTuple/ | grep BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n4`

#root -l -q 'BHflatTuplizer.cc+("root://eoscms.cern.ch//store/group/phys_exotica/BH_RunII/BlackMax_NTuple/BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n4_NTuple.root","BlackMaxLHArecord_BH5_BM_MD9000_MBH11000_n4_FlatTuple.root","METfilteredEvents_Feb02.txt")'

for f in $Files
do 
	echo "Processing $f"
	outname=`echo $f | sed 's/NTuple/FlatTuple/'`
	if [ ! -f $outname ]
	then 
		eval $'root -l -q \'BHflatTuplizer.cc+("root://eoscms.cern.ch//store/group/phys_exotica/BH_RunII/BlackMax_NTuple/'"$f"$'\",\"'$outname$'\",\"METfilteredEvents_Feb02.txt\")\''
	fi
done
