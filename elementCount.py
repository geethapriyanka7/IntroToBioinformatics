#!/usr/bin/env python3
import sys
import argparse
# Reading bed file as input in the command
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="Input file")
args = parser.parse_args()
mainbed = []
bed = []
# Opening the file and adding all the values to a list 
with open(args.i, 'r') as f:
    for line in f:
        cols = line.rstrip().split("\t")
        bed.append(cols)



    
    chr_name = ""
    count = 0  
    # Assigning variables to chromosome, start and start from the bed file 
    while count < len(bed):
        chrom, start, stop = bed[count][0], int(bed[count][1]), int(bed[count][2])
        chr_name = bed[count][0]
        interval = []
        # Comparing opening and closing intervals with the same chromosomes 
        # Assigning -1 to the interval-start as a tuple 
        # Assigning 1 to the interval-stop as a tuple and counting the occurences
        while count < len(bed) and bed[count][0] == chr_name:
            interval.append((int(bed[count][1]), -1))
            interval.append((int(bed[count][2]), 1))
            count += 1
        interval.sort()


        counts = 1
        for i in range(1, len(interval)):
            assert(interval[i - 1][0] <= interval[i][0])
            if interval[i - 1][0] != interval[i][0] and counts > 0:
                print(chr_name, interval[i - 1][0], interval[i][0], counts, sep='\t')
            if interval[i][1] == -1:
                counts += 1
            else:
                counts -= 1








