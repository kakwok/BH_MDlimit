# BH_MDlimit
## 1) Generate the signal flat Tuple
Input: a eos path like `/store/group/phys_exotica/BH_RunII/BlackMax_NTuple/`  
Change the `$DIR` in the shell script, prepare a directory called `"SignalFlatTuple/ModelClass"`
Usage:  
```
cmsenv  
mkdir SignalFlatTuple
cd SignalFlatTuple
mkdir ModelClass
cd ../
sh GenSignalFlatTuple.sh
```

## 2) Find the Optimal (Stmin,Nmin) points
####i) Ingredients:
* Theoretic cross sections: e.g.`QBH_xsection.txt` or `BlackMax_xsection.txt`  
  For all cross sections, refer to twiki:  
  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BlackHoleAnalysis2015
* Data FlatTuple          : `all2015C+D_NoMetCut+NewMETFilter.root`
* MILimit                 : `MILimit.txt`  

####ii) Prepare the input list with:  
```
ls SignalFlatTuple/ModelClass/*.root > MasspointList.txt
```

**The * is important.** This will generate a txt file with format path/root 

####iii)** Modify the Input constants section in `ZbiCalculator.py` before running**  
`eospath` is neccessary only if the Ntuple file is in eos. Only the path listed in the code are necessary. 
The FlatTuples of BH_fullsim and Charybdis already contains Ngen info.

####iv) Running the code 
ZbiCalculator_v5 = optimizing with observed MI limit.  
ZbiCalculator_v4 = optimizing with Zbi.  
```
cmsenv  
eosmount eos
python ZbiCalculator_v5.py MasspointList.txt StOpt_Model.txt
``` 
`StOpt_Model.txt` and `StOpt_Model.root` will be the output files. 
`StOpt_Model.txt` will contain the optimal points for each sample and the limits data for plotting.  
`StOpt_Model.root` will contain validation plots for searching optimal points. 

##3) Making the plots
####i) Sort the output
```
python sort.py StOpt_Model.txt
```
This is important for interpolating the correct minMBH.

####ii) Make the root file with plots
```
mkdir ./plots
python MakeMDroot.py StOpt_Model.txt -b
```
Output: `./plots/StOpt_Model_plots.root`

####iii) Make the final limit plot
There is one seperate plotting script for each final plot.
```
python drawSB.py -b
```
####iv) Make sanity check plots
```
cd plots
python makepdf.py StOpt_Model_plots.root -b
```
