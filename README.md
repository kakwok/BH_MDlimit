# BH_MDlimit
## 1) Generate the signal flat Tuple
Input: a eos path like `/store/group/phys_exotica/BH_RunII/BlackMax_NTuple/`  
Change the $DIR in the shell script, prepare a directory called `"SignalFlatTuple"`
Usage:  
```
cmsenv  
sh GenSignalFlatTuple.sh
```

## 2) Calculate Zbi
i)Ingredients:
* Theoretic cross sections: e.g.`QBH_xsection.txt` or `BlackMax_xsection.txt`  
  For all cross sections, refer to twiki:  
  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BlackHoleAnalysis2015
* Data FlatTuple          : `all2015C+D_NoMetCut+NewMETFilter.root`
* MILimit                 : `MILimit.txt`  

ii) Prepare the input list with:  
`ls SignalFlatTuple/ModelClass/*.root > MasspointList.txt`  
**The * is important.** This will generate a txt file with format path/root 

iii)**Modify the Input constants section in `ZbiCalculator.py` before running**
`eospath` is neccessary only if the Ntuple file is in eos. Only the path listed in the code are necessary. 
The FlatTuples of BH_fullsim and Charybdis already contains Ngen info.

iv) Run the code 
```
cmsenv  
eosmount eos
python ZbiCalculator_v5.py MasspointList.txt StOpt_Model.txt
``` 
`StOpt_Model.txt` and `StOpt_Model.root` will be the output files. 
`StOpt_Model.txt` will contain the optimal points for each sample and the limits data for plotting



