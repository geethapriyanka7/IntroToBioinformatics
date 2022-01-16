#!/usr/bin/env python3

import sys

seq1 = ""
seq2 = ""
# Input FASTA sequences
seqA = sys.argv[1]

with open(seqA) as seq1_fh:
    for line in seq1_fh.readlines():
        if line.startswith(">"):
            continue
        else:
            seq1 += line
seq1 = seq1.rstrip("\n")

seqB = sys.argv[2]
with open(seqB) as seq2_fh:
    for line in seq2_fh.readlines():
        if line.startswith(">"):
            continue
        else:
            seq2 += line
seq2 = seq2.rstrip("\n")

m = len(seq1)
n = len(seq2)
h = []

match = 1
mismatch = -1
gap = -1

# fill up the first row and column of the matrix


for i in range(m+1):
    t = []
    for j in range(n+1):
        t.append(0)
    h.append(t)
for j in range(n+1):
    h[0][j] = gap*j

for i in range(m+1):
    h[i][0] = gap*i


# filling the matrix
for i in range(1, m+1):
    for j in range(1, n+1):
        if seq1[i-1] == seq2[j-1]:
            h[i][j] = max(h[i][j-1]+gap, h[i-1][j]+gap, h[i-1][j-1]+match)
        else:
            h[i][j] = max(h[i][j-1]+gap, h[i-1][j]+gap, h[i-1][j-1]+mismatch)

# Backtracing
seq1_align = ""
seq2_align = ""
count = 0

i = m
j = n

while (i>0 or j>0):

    
    if seq1[i-1] == seq2[j-1]:
        seq1_align += seq1[i-1]
        seq2_align += seq2[j-1]
        i -= 1
        j -= 1

    
    elif seq1[i-1] != seq2[j-1]:
        temp = [h[i-1][j-1], h[i-1][j], h[i][j-1]]        

        
        if max(temp) == temp[0]:
            seq1_align += seq1[i-1]
            seq2_align += seq2[j-1]
            i -= 1
            j -= 1

        
        elif max(temp) == temp[1]:
            seq1_align += seq1[i-1]
            seq2_align += "-"
            i -= 1

        
        elif max(temp) == temp[-1]:
            seq1_align += "-"
            seq2_align += seq2[j-1]
            j-=1

    
    else:
        print("Error")
        i=0
        j=0

seq1_align = seq1_align[::-1]                   
seq2_align = seq2_align[::-1]  


matchs = ""
for i in range(len(seq1_align)):
    if seq1_align[i] == seq2_align[i]:
        matchs += "|"
    elif seq1_align[i] != seq2_align[i]:
        if (seq1_align[i] == "-" or seq2_align[i] == "-"):
            matchs += " "
        else:
            matchs += "*"

#Calculating the alignment score:
alignment_score = 0
for i in range(len(matchs)):
    if matchs[i] == "|":
        alignment_score += 1
    elif (matchs[i] == "*" or matchs[i] == " "):
        alignment_score += -1

#Printing out the final result:
print(seq1_align)
print(matchs)
print(seq2_align)
print("Alignment score:", alignment_score)

