#!/usr/bin/env python3
import sys
import argparse
from multiprocessing import Pool
import os
import subprocess

final = []
parser = argparse.ArgumentParser()
parser.add_argument('-o','--o', help = "Output file name")
parser.add_argument('-t','--t', help = "Number of threads to be used for the program")
parser.add_argument('file', nargs = '+')
args = parser.parse_args()
t = int(args.t)
out = args.o
f = args.file
#print(f)

for i in range(len(f)):
	for j in range(i+1, len(f)):
		final.append((f[i],f[j]))
def dna_diff(d):
	command = 'dnadiff -p '+str(d[0]+d[1])+'result'+' '+str(d[0])+' '+str(d[1])
	f = subprocess.check_call(command.split())
	command2 = "grep -E 'AvgIdentity' "+str(d[0]+d[1])+"result.report | awk '{print $2}'| head -1"
	r = os.popen(command2).read()
	return r.strip() 

pool = Pool(t)
p = list((pool.map(dna_diff, final)))
# for i in p:
# 	print(i)
#print(p)
pool.close()
pool.join()

for k in final:
	remove = "rm -rf "+str(k[0])+"g*"
	os.system(remove)


#Obtain a lower triangle from a list
files = p 
n = len(f)
m = []

# Upper triangle
for i in range(1, n):
	m.append(i)
	mn = reversed(m)
	m2 = list(mn)


sub = []
mu = [[100]]
count = 0
for i in m2:
	sub.append(files[count:count + i])
	count = i + count
for i in sub:
	i.insert(0, 100)
sub.extend(mu)
#print(sub)
a = []
for i in sub:
	a.append(len(i))
	#print(a)
	for k in range(len(a)):
		if a[k] < a[k-1]:
			i.insert(0, 0)


# #Lower triangle
for i in range(n):
	for j in range(n):
			sub[j][i] = sub[i][j]

#print(sub)

# Adding header to the matrix
fg = f
l = len(fg)
a = sub
 # adding row header 
a = [fg] + a
 # adding column header 

mod = [' '] + fg
na = [[mod[i]] + a[i] for i in range(l+1)]
# for i in na:
# 	print(*i)

sys.stdout=open(out ,"w")
for i in na:
	print(*i, sep = '\t')
sys.stdout.close()
