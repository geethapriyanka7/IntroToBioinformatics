# IntroToBioinformatics
FASTA is generally acknowledged to be the greatest format ever.  Therefore, we will be writing a script to convert any file into a FASTA file with the same name, but with .fna or .faa extension, depending on whether or not it contains nucleic acid or amino acid sequences.  
It should accept the following file types:
Format Example description
EMBL, FASTQ, GenBank, MEGA, SAM, VCF. Identify the key formats using Google.
Guessing whether the input sequence is protein or nucleotide is imperfect, but an easy (and correct) assumption is to assume that a DNA sequence only contains the character set: [ACGTNacgtn].
You script should be invoked like this: ./all2fasta.py -i a_file.gbk
This  will  produce  a  file  called  a_file.fna  if  a_file.gbk  has  DNA  in  it  or  a_file.faa  if 
a_file.gbk had an amino acid sequence.

Syntax: 
./ all2fasta.py [-f FOLD] -i <input file name>
The optional argument that can be provided to all2fasta.py is -f that specifies the line fold,  i.e.,  after how many bases should a  new line be inserted.  The default value should be 70. This option will have no effect on the sequence description line.
Example usage: 
# this will print 70 bases per line
./ all2fasta.py -i gb.in
# this will print 20 bases per line
./all2fasta.py -f 20 -i gb.in
Additional instructions:
Format Description – SAM file:
Format has this basic structure:
Header
@SQ SN:sequence_name LN:987
@PG ID:bwa PN:bwa VN:0.7.17-r1198-dirty CL:bwa 
mem -t 4 ...
Reads
BIOL7200:113:000000000-GTECH:1:1101:15700:1335 77 *
0 ...
BIOL7200:113:000000000-GTECH:1:1101:15700:1335 141 *
0 ...
The actual data fields (SN, LN, ID, VN, CL) can change from file to file but, for 
the purpose of this assignment, assume that all SAM files will:
1. Have a header present (lines starting with @)
2. The header will always come before the reads data
3. The headers will have at minimum  @SQ  and  @PG.    It can have more 
fields (e.g., @HD) and @SQ and @PG may not be the first two lines.  I.e., 
this is also a valid structure:
@HD VN:1.6 SO:coordinate
@SQ SN:ref LN:45
@PN bwa
@PG ID:bwa ...
The reads will have a minimum of 11 columns.  Columns 12 and onwards are optional and program-specific.  Each column will be tab-separated.
How do you make a FASTA file out of this?
Taking the first two lines from the sample.sam file:
The FASTA format will be:
>line1_column1
line1_column_10
>line2_column1
line2_column_10
So, for this example, the FASTA file will be (assuming fold value of 50 bases):
>BIOL7200:113:000000000-GTECH:1:1101:15700:1335
ATTTTGTTTCTATTGCTTCAGTCACACACGAGAATACTCTGCGCTATGTA
AATCAATTCCGCTTTGACAACCAGCATAATTTAAAACTGGCTCGTCAGAT
AAGTGAAGTAAAGTATGTCAATAATTCGTGGATAGCTTATGATGTGAAAC
AAACTGAATTTGCAGAGGATCATACCAAAGCCTATCATTTCGATACCTTG
CCGTGGGATGTGCCAGTGAAACCGGAAATTC
>BIOL7200:113:000000000-GTECH:1:1101:15700:1335
TGTTGCTCACGTAAATAGCGGTTCAATTCATGTAAAGTCATTTCATCCGG
ATTGGTGCCCGTAATTTTAAGAATTTCCGGTTTCACTGGCACATCCCACG
GCAAGGTATCGAAATGATAGGCTTTGGTATGATCCTCTGCAAATTCAGTT
TGTTTCACATCATAAGCTATCCACGAATTATTGACATACTTTACTTCACT
TATCTGACGAGCCAGTTTTAAATTATGCTGG
Format Description – VCF file:
Here is a simplified overview:
##fileformat=VCFv4.2
## ...
#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT sample1 sample2 sample3
...
NC_01234 32 . C A 0 . AB=0;... GT:DP:...1:310:... 0:310:... 1:193:...
...
NC_01234 42 . G T,A 0 . AB=0;... GT:DP:...1:266:... 2:288:... 0:237:...
...
NC_01234 69 . GGG GCC 918.101 . AB=0;... GT:DP:...1:280:... 1:290:... 1:280:...
...
The key points to remember here are:
1. A VCF file will start with header lines
2. The header will have multiple sections
3. The first line in the header will be ##fileformat=VCFv...
4. The last line will be #CHROM...
5. A VCF file will have at least 10 columns: 9 columns describing the variant, and columns 10 and onwards describing the presence of the variant in the different samples
6. Columns 10 and onwards are the samples
7. Each column is separated by tabs
8. Columns 10 and onwards contain the structure described in column 9 (FORMAT).  
9. Columns 4 (REF) and 5 (ALT) describe the base(s) that is present in the samples
10. REF base is denoted by 0, ALT bases are denoted as 1, 2, 3, etc.  The first ALT base is 1, the second ALT base is 2, and so on.
How do you make a FASTA file out of this?
Going with this small example:##fileformat=VCFv4.2
## ...
#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT sample1 sample2 sample3
...
NC_01234 32 . C A 0 . AB=0;... GT:DP:...1:310:... 0:310:... 1:193:...
...
NC_01234 42 . G T,A 0 . AB=0;... GT:DP:...1:266:... 2:288:... 0:237:...
...
NC_01234 69 . GGG GCC 918.101 . AB=0;... GT:DP:...1:280:... 1:290:... 0:280:...
...
The FASTA file will be:
>NC_01234
CGGGG
>sample1
ATGCC
>sample2
CAGCC
>sample3
AGGGG
Note that we are expecting you to also add the reference sequence 
(NC_01234).
