#!/usr/bin/python3

import subprocess 
import argparse
import shlex

# Giving input file 1 , input file 2, output filename and sequence type using argparse commands
parser = argparse.ArgumentParser()
parser.add_argument("-i1", help = "Give input file 1.")
parser.add_argument("-i2", help = "Give input file 2.")
parser.add_argument("-o", help = "Name your output filename")
parser.add_argument("-t", help = "n for nucleotide sequence, p for protein sequence.")
args = parser.parse_args()

#Assigning the argument inputs to variables
input_1 = args.i1            
input_2 = args.i2
output = args.o
sequence_type = args.t

#making a temporary directory to store the databases and outputs for forward and reverse blast
make_dir = subprocess.call(shlex.split("mkdir 'temp'"))

#Building a function to get the blast hits for two sequences
def reciprocal_blast_hits(input_1, input_2, sequence_type):
# Using lists to compare the sequences and run blast      
    input1_1 = []                  #This list  stores the first index headers (index headers of input file 1)
    input1_2 = []                  #This list stores the second query headers (query headers of input file 2)
    input2_1 = []                  #This list stores the first index headers (db values of input file 2)
    input2_2 = []                  #This list stores the second query headers (query headers of input file 1)
    output_1 = []                  #This list is to store common headers in forward blast i.e inputfile 1 as index and inputfile2 as query
    output_2 = []                  #This list is to store common headers in reverse blast i.e inputfile 2 as index and inputfile1 as query 
    output_final = []              #Contains only reciprocal blast hits

    if sequence_type == "n":  #For nucleotide(n)

# This is forward blast for the two sequence files
        
        input1_1_db = "makeblastdb -in " + str(input_1) + " -dbtype nucl -out temp/db1"   #Creating db for inputfile1
        input1_1_db_subprocess = subprocess.check_output(input1_1_db.split())

        result_1 = "blastn -db temp/db1 -query " + str(input_2) + " -max_target_seqs 1 -max_hsps 1 -outfmt 6 -out temp/output_1" #Here query input is input2 and db is input1
        result_1_subprocess = subprocess.check_output(result_1.split())
        
#This is the reverse blast for the two sequence file inputs

        input2_2_db = "makeblastdb -in " + str(input_2) + " -dbtype nucl -out temp/db2"   #Creating db for inputfile2
        input2_2_db_subprocess = subprocess.check_output(input2_2_db.split())

        result_2 = "blastn -db temp/db2 -query " + str(input_1) + " -max_target_seqs 1 -max_hsps 1 -outfmt 6 -out temp/output_2" #Output for query = input1 and db = input2
        result_2_subprocess = subprocess.check_output(result_2.split())
    
    elif sequence_type == "p":       # for protein sequences
        # This is forward blast for the two sequence files
        
        input1_1_db = "makeblastdb -in " + str(input_1) + " -dbtype prot -out temp/db1"   #Creating db for inputfile1
        input1_1_db_subprocess = subprocess.check_output(input1_1_db.split())

        result_1 = "blastp -db temp/db1 -query " + str(input_2) + " -max_target_seqs 1 -max_hsps 1 -outfmt 6 -out temp/output_1" #Here query input is input2 and db is input1
        result_1_subprocess = subprocess.check_output(result_1.split())
        
        #This is the reverse blast for the two sequence file inputs

        input2_2_db = "makeblastdb -in " + str(input_2) + " -dbtype prot -out temp/db2"   #Creating db for inputfile2
        input2_2_db_subprocess = subprocess.check_output(input2_2_db.split())

        result_2 = "blastp -db temp/db2 -query " + str(input_1) + " -max_target_seqs 1 -max_hsps 1 -outfmt 6 -out temp/output_2" #Output for query = input1 and db = input2
        result_2_subprocess = subprocess.check_output(result_2.split())        
    
    else:
        print("wrong sequence type input")
        
    with open("temp/output_1") as f1:
         for line in f1.readlines():
             if line.startswith("lcl"):
                input1_1.append(line.split()[0])   # To store db values in the list         
             if line.startswith("lcl"):
                input1_2.append(line.split()[1])   # To store query headers in the list      

    for i,j in zip(input1_1,input1_2):
        output_1.append(i+"\t"+j+"\n")

    with open("temp/output_2") as f2:
         for line in f2.readlines():
             if line.startswith("lcl"):
                input2_1.append(line.split()[0])              # To store db values in the list 
             if line.startswith("lcl"):
                input2_2.append(line.split()[1])              # To store query headers in the list 

    for i,j in zip(input2_1,input2_2):
        output_2.append(j+"\t"+i+"\n")         #Inversing the list in order to find common things bw output_1 and output_2

    for x in output_1:                         #Checking common hits beween output_1 and output_2
        if x in output_2:
           output_final.append(x)                   
    
    return output_final

#Calling the function and adding the orthologs to the output file
output_list = reciprocal_blast_hits(input_1, input_2, sequence_type)
with open(output, 'w') as output_f:
    for ortholog_match in output_list:
        output_f.write(ortholog_match)

#Deleting the temporary directory created to save temporary outputs
del_dir = subprocess.call(shlex.split("rm -rf 'temp'"))

    
