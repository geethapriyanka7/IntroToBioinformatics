#! /usr/bin/env python3
import sys
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--i", help="this is Input file")
parser.add_argument('-f', '--fold', type=int, default=70)
args = parser.parse_args()
num = args.fold
if args.i:
    Input1 = str(args.i)

def Fastqtofasta(fn):
    count = 0
    with open(fn, 'r') as fh:
        seqs = []

        for line in fh:

            if (re.search(pattern='\\+', string=line) is not None):
                record = {}
            if (re.search(pattern='\\?', string=line) is None) and (re.search(pattern='@', string=line) is not None):
                record = {}
                record['name'] = line.replace("@", ">").strip('\n')


            elif (re.search(pattern='\\?', string=line) is None) and (
                    re.search(pattern='[ATCGn]+', string=line) is not None):
                record["seq"] = line.strip("\n")
                if (len(re.findall(r'[^ATCGNatcgn]+', record["seq"])) != 0):
                    count = 1
                record["len"] = len(line.strip("\n"))
                seqs.append(record)
    return seqs, count


def GeneBanktofasta(fn):
    count = 0
    with open(fn, 'r') as fh:
        lines = []
        record = {}
        a = 0
        for line in fh:
            if a == 1:
                lines.append(line)
            if (line.strip() != ''):

                if (re.search(pattern='ACCESSION', string=line) is not None):
                    record["name"] = ">" + (line.split())[1].strip('\n')
                if (re.search(pattern='DEFINITION', string=line) is not None):
                    record["descr"] = (line.strip('\n').replace('DEFINITION', 'descr='))
                if (re.search(pattern='LOCUS', string=line) is not None):
                    record["len"] = line.split()[2].strip('\n')
                if (re.search(pattern='ORIGIN', string=line) is not None):
                    a = 1
                if (re.search(pattern='//', string=line) is not None):

                    seqs = ''
                    for i in range(1, len(lines) - 1):
                        seqs += ''.join(lines[i].split()[1:])
                    record["seq"] = seqs.upper().strip('\n')
                    if (len(re.findall(r'[^ATCGNatcgn]+', record["seq"])) != 0):
                        count = 1
    return [record], count


def MEGAtofasta(fn):
    count = 0
    with open(fn, 'r') as fh:
        lines = []
        header = []
        seqs = []
        for line in fh:
            lines.append(line)
        content_list = ("".join(lines[2:])).split("#")
        for each in content_list:
            info = each.split("\n")

            header.append(info[0])
            seqs.append("".join(info[1:]))
    header = header[1:]
    seqs = seqs[1:]
    if len(header) == 0:
        record = {}
        record["name"] = header[0].strip('\n')
        record["seq"] = seqs[0].strip('\n')
        record["len"] = len((seqs[0]).strip('\n'))
        seqs.append(record)
    else:

        for i in range(0, len(header)):

            record = {}
            record["name"] = header[i].strip('\n')
            record["seq"] = seqs[i].strip('\n')
            record["len"] = len((seqs[i]).strip('\n'))
            if (len(re.findall(r'[^ATCGNatcgn]+', seqs[i])) != 0):
                count = 1
            seqs.append(record)
    return [record], count


def EMBLtofasta(fn):
    count = 0
    with open(fn, 'r') as fh:
        lines = []
        record = {}
        a = 0
        for line in fh:
            if a == 1:
                lines.append(line)
            if (line.strip() != ''):

                if (re.search(pattern='ID', string=line) is not None):
                    record["name"] = ">" + (line.split())[1].strip('\n')
                if (re.search(pattern='DE  ', string=line) is not None):
                    record["descr"] = (line.strip('\n').replace('DE   ', 'descr='))
                if (re.search(pattern='SQ', string=line) is not None):
                    a = 1
                    record["len"] = line.split()[2].strip('\n')

                if (re.search(pattern='//', string=line) is not None):

                    seqs = ''
                    for i in range(1, len(lines) - 1):
                        seqs += ''.join(lines[i].split()[0:-1])
                    record["seq"] = seqs.upper().strip('\n')
                    if (len(re.findall(r'[^ATCGNatcgn]+', record["seq"])) != 0):
                        count = 1
    return [record], count

def samtofasta(fn):
    count = 0
    seqs=[]
    record = {}
    with open (fn, 'r') as fh:
        for line in fh:
            if (re.search(pattern = '@', string = line) is None):
                count = 0
                cols=line.rstrip().split("\t")
                #print(cols[0])
                for i in cols:
                    record["name"] = ( '>' + cols[0])
                    record["seq"] = (cols[9])
                seqs.append(record)
                count = 0
    return seqs, count

def vcftofasta(fn):
    sample=[]
    seqs = []
    record={}
    count = 0
    with open (fn, 'r') as fh:
        for line in fh:
            ref=[]
            alt=[]
            genetype=[]
            if line.startswith("#CHROM"):
                sample=line.strip("\n").split("\t")[9:]
                for i in sample:
                    record[i]=""
            elif line.startswith("##"):
                pass
            else:
                realgenetype=[]
                genetype_dict={}
                genetype=line.strip("\n").split("\t")[9:]
                ref=line.split("\t")[3]
                alt=line.split("\t")[4].split(",")
                for i in genetype:
                    if i[0] == 0:
                        realgenetype.append(ref)
                    else:
                        realgenetype.append(alt[int(i[0])-1])
                for i in range(0,len(sample)):
                    genetype_dict[sample[i]]=realgenetype[i]
                    pass
                for j in genetype_dict:
                    record[j]=record[j]+genetype_dict[j]
                    pass
        for i in sample:
            record["name"] = ">" + i
            record["seq"] = "".join(record.values())
        count = 0
        seqs.append(record)
    return [record], count

with open(Input1, "r") as input1:
    first_line = input1.readline()
    # print(first_line)
    match = re.search(pattern='@SQ', string=first_line)
    if (match is not None):
        print("Input file is sam")
        seqs, count = samtofasta(Input1)

        # print(seq)
        # writeFasta(Input1, fasta.out)
    else:
        match = re.search(pattern='ID', string=first_line)
        if (match is not None):
            seqs, count = EMBLtofasta(Input1)
            print("Input file is EMBL")
            # print(seq)
        else:
            match = re.search(pattern='LOCUS', string=first_line)
            if (match is not None):
                seqs, count = GeneBanktofasta(Input1)
                # print(seq)
                print("Input file is GeneBank")
            else:
                match = re.search(pattern='#MEGA', string=first_line)
                if (match is not None):
                    print("Input file is MEGA")
                    seqs, count = MEGAtofasta(Input1)
                    # print(seq)
                else:
                    match = re.search(pattern='@', string=first_line)
                    if (match is not None):
                        print("Input file is fastq")
                        seqs, count = Fastqtofasta(Input1)
                    else:
                        match = re.search(pattern='##', string=first_line)
                        if (match is not None):
                            print("Input file is vcf")
                            seqs, count = vcftofasta(Input1)
                        else:
                            print("Input file does not match with any format")

#print(seq)
filename = Input1.split(".")
if (count == 0):
    appendix = "fna"


else:
    appendix = "faa"
if filename[-1] == "fna" or filename[-1] == "faa":
    output = ".".join(filename)
    Output = open(output, "w")
elif len(filename) == 1:
    ouput = filename[0] + "." + appendix
    Output = open(output, "w")
else:
    filename[-1] = appendix
    ouput = output = ".".join(filename)
    Output = open(output, "w")

for record in seqs:
    Output.write(str(record['name']))
    Output.write("\n")

    n = 0
    for c in list(str(record['seq'])):
        Output.write(str(c))
        n += 1
        if n > num:
            n = 0
            Output.write("\n")
    Output.write("\n")