#!/usr/bin/env python3
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i1", help="Input Bed file 1", required = True)
parser.add_argument("-i2", help="Input Bed file 2", required = True)
parser.add_argument("-m", help = "Minimun overlap to be shown", required = True)
parser.add_argument("-j", "--join", help = "Compare files", action="store_true")
parser.add_argument("-o", help = "Output file", required = True)
args = parser.parse_args()
args.m = int(args.m)
start1=[]
stop1=[]
start2=[]
stop2=[]
list1={}
list2={}
names=[]

def checkIFOverlapEnough(s1, e1, s2, e2, m):
    l = max(s1, s2)
    r = min(e1, e2)
    if l > r:
        return 0
    if (100 * (r - l) >= m * (e1 - s1)):
        return 1
    return 0

with open(args.i1, 'r') as f1:
    for line in f1:
        cols = line.rstrip().split("\t")[0:3]
        name1 = cols[0]
        start1 = cols[1]
        stop1 = cols[2]
        if name1 not in list1.keys():
            list1[name1] = []
            names.append(name1)
        list1[name1].append((int(start1), int(stop1)))


with open(args.i2, 'r') as f2:
    for line in f2:
        cols = line.rstrip().split("\t")[0:3]
        # bed2.append(cols2)
        name2 = cols[0]
        start2 = cols[1]
        stop2 = cols[2]
        if name2 not in list2.keys():
            list2[name2] = []
        list2[name2].append((int(start2), int(stop2)))


for name in names:
    chromosome = list2[name]
    n = len(chromosome)
    count = 0
    for i in list1[name]:
        while count < n and i[0] > chromosome[count][1]:
            count += 1
        j = count
        while j < n:
            if i[1] < chromosome[j][0]:
                break
            if max(i[0], chromosome[j][0]) > min(i[1], chromosome[j][1]):
            	j += 1
            	continue
            if checkIFOverlapEnough(i[0], i[1], chromosome[j][0], chromosome[j][1], args.m):
                if args.join:
                    file = open(args.o, "a")
                    sys.stdout = file
                    print(name, i[0], i[1], name, chromosome[j][0], chromosome[j][1])
                else:
                    file = open(args.o, "a")
                    sys.stdout = file
                    print(name, i[0], i[1])
                    break
            j += 1




