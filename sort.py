import os
from sys import argv
from subprocess import call

#f = open("StOpt_BHtest.txt")
f = open("%s"%argv[1],"r")
out = open("%s_sorted.txt"%argv[1].replace(".txt",""),"w")

lines = []

for line in f:
	line=line.split()
	lines.append(line)

header = lines.pop(0)
del lines[0]

lines= sorted(lines,key=lambda Hash:float(Hash[3]))
lines= sorted(lines,key=lambda Hash:float(Hash[1])+float(Hash[2]))
lines= sorted(lines,key=lambda Hash:Hash[0])

lines.insert(0,header)
for l in lines:
	for item in l:
		out.write("%s "%item)
	out.write("\n")
print "Moving %s to %s" %(argv[1],argv[1].replace(".txt",".bk"))
renameIN="mv %s %s"%(argv[1],argv[1].replace(".txt",".bk"))
print "Moving %s_sorted.txt to %s" %(argv[1].replace(".txt",""),argv[1])
renameOUT="mv %s_sorted.txt %s"%(argv[1].replace(".txt",""),argv[1])
os.system(renameIN)
os.system(renameOUT)
