import os
from sys import argv
from subprocess import call

#f = open("StOpt_BHtest.txt")
f = open("%s"%argv[1],"r")
out = open("%s_sorted.txt"%argv[1].replace(".txt",""),"w")

lines = []
NoSplitLines = []
for line in f:
	NoSplitLines.append("%s"%line)
	lines.append(line.split())

lines.pop(0)
header = NoSplitLines.pop(0)

lines= sorted(lines,key=lambda Hash:float(Hash[3]))
lines= sorted(lines,key=lambda Hash:float(Hash[1])+float(Hash[2]))
lines= sorted(lines,key=lambda Hash:Hash[0])

out.write("%s"%header)
for l in lines:
	key_sorted = l[0]+l[1]+l[2]+l[3]
	for line in NoSplitLines:
		split_line = line.split()
		key        = split_line[0]+split_line[1]+split_line[2]+split_line[3]
		#print key + "      " + key_sorted
		if (key==key_sorted):
			out.write("%s"%line)
print "Moving %s to %s" %(argv[1],argv[1].replace(".txt",".bk"))
renameIN="mv %s %s"%(argv[1],argv[1].replace(".txt",".bk"))
print "Moving %s_sorted.txt to %s" %(argv[1].replace(".txt",""),argv[1])
renameOUT="mv %s_sorted.txt %s"%(argv[1].replace(".txt",""),argv[1])
os.system(renameIN)
os.system(renameOUT)
