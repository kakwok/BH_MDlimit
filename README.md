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
Ingredients:
* Theoretic cross sections: e.g.`QBH_xsection.txt` or `BlackMax_xsection.txt`  
  For all cross sections, refer to twiki:  
  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BlackHoleAnalysis2015
* Data FlatTuple          : `all2015C+D_NoMetCut+NewMETFilter.root`
* MILimit                 : `MILimit.txt`  

**Modify the Input constants section in `ZbiCalculator.py` before running**

`ZbiCalculator` loops over all the samples in the `MasspointList.txt` 
```
cmsenv  
eosmount eos
python ZbiCalculator_v4.py MasspointList.txt Output.txt
```
