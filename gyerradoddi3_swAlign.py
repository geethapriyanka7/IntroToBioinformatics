#!/usr/bin/env python3

import sys

seqA = sys.argv[1]
seqB = sys.argv[2]

seq1 = ""

with open(seqA) as seq1_fh:
    for line in seq1_fh.readlines():
        if line.startswith(">"):
            continue
        else:
            seq1 += line
seq1 = seq1.rstrip("\n")

seq2 = ""

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


match = +1
mismatch = -1
gap = -1

#Initialising the matrix to 0 (Part1):
for i in range(m+1):
    temp = []
    for j in range(n+1):
        temp.append(0)
    h.append(temp)


#Matrix filling (Part2):
for i in range(1,m+1):
    for j in range(1, n+1):
        if seq1[i-1] == seq2[j-1]:
            h[i][j] = max(h[i][j-1]+gap, h[i-1][j]+gap, h[i-1][j-1]+match, 0)
        else:
            h[i][j] = max(h[i][j-1]+gap, h[i-1][j]+gap, h[i-1][j-1]+mismatch,0)


seq1_back = ""
seq2_back = ""
maximum = 0
for row in range(1, m+1):
    for column in range(1,n+1):
        if maximum < h[row][column]:
            maximum = h[row][column]     
            i = row                             
            j = column 

#Backtracking (Part3):
while h[i][j] != 0:
    if seq1[i-1] == seq2[j-1]:
        seq1_back += seq1[i-1]
        seq2_back += seq2[j-1]
        i -= 1
        j -= 1

    elif seq1[i-1] != seq2[j-1]:
        temp = [h[i-1][j-1], h[i-1][j], h[i][j-1]]
        if max(temp) == temp[0]:
            seq1_back += seq1[i-1]
            seq2_back += seq2[j-1]
            i -= 1
            j -= 1

        elif max(temp) == temp[1]:
            seq1_back += seq1[i-1]
            seq2_back += "-"
            i -= 1

        elif max(temp) == temp[-1]:
            seq1_back += "-"
            seq2_back += seq2[j-1]
            j -= 1

    else:
        print("Error")
        i=0
        j=0

seq1_align = seq1_back[::-1]                   #Reverse the string seq1_align
seq2_align = seq2_back[::-1]                   #Reverse the string seq2_align


matchs = ""
for i in range(len(seq1_align)):
    if seq1_align[i] == seq2_align[i]:
        matchs += "|"
    elif seq1_align[i] != seq2_align[i]:
        if seq1_align[i] == "-" or seq2_align[i] == "-":
            matchs += " "
        else:
            matchs += "*"

#Calculating the alignment score:
alignment_score = 0
for i in range(len(matchs)):
    if matchs[i] == "|":
        alignment_score += 1
    elif matchs[i] == "*" or matchs[i] == " ":
        alignment_score += -1

#Printing out the final result:
print(seq1_align)
print(matchs)
print(seq2_align)
print("Alignment score:", alignment_score)
