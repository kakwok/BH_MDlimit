# BH_MDlimit
# 1) Generate the signal flat Tuple
    Input: a eos path like /store/group/phys_exotica/BH_RunII/BlackMax_NTuple/ 
    Change the $DIR in the shell script, prepare a directory called "SignalFlatTuple"
    Usage: cmenv
	   sh GenSignalFlatTuple.sh

# 2) Calculate Zbi
    Ingredients:
* Theoretic cross sections: QBH_xsection.txt BlackMax_xsection.txt SB_xsection.txt
* Data FlatTuple          : all2015C+D_NoMetCut+NewMETFilter.root
* FitFunction             : fitfunctions_ex2.root
* MILimit                 : MILimit.txt

   Usage: 
```
   python ZbiCalculator_v4.py MasspointList.txt Output.txt
```
