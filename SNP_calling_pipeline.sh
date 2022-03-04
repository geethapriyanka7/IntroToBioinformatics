#!/bin/bash
# workflow to map working DNA sequence data  and obtain variant calling format
# Giving the required arguments and options
realign=0
index=0
gunzip=0
while getopts 'a:b:r:e:o:f:z:vhi:' rest
do 
case $rest in
a) reads1=$OPTARG;;
b) reads2=$OPTARG;;
r) ref=$OPTARG;;
e) realign=$OPTARG;;
o) output=$OPTARG;;
f) millsFile=$OPTARG;;
z) gunzip=$OPTARG;;
v) verbose=1;;
i) index=$OPTARG;;
h) echo "SNP Calling pipeline
-- requires input read pairs
-- requires a refernce file
-- Mapping the inputs with reference
-- sort the output and realign
-- variant calling 
-- obtaining vcf file is the last step
-- realign -e can be 0 or 1
-- index -i can be 0 or 1
-- gunzip -z the vcf file can be 0 or 1" && exit
esac
done

if [[ $verbose -eq 1 ]]
then 
echo "Reading the input pair files given for the pipeline"
fi
if [[ $reads1 == *.fq ]]
then echo "Input reads file - pair 1 is present "
else echo "Input reads file - pair 1 is missing" && exit
fi
if [[ $reads2 == *.fq ]]
then echo "Input reads file - pair 2 is present "
else echo "Input reads file - pair 2 is missing" && exit
fi
if [[ $verbose -eq 1 ]]
then
echo "Reading the reference genome file given for the pipeline"
echo "Preparing reference for mapping and map your reads to the reference"
fi
if [[  $ref == *.fa ]]  
then
echo "Reference genome file is present"
# Indexing the reference genome  
bwa index $ref
if [[ $verbose -eq 1 ]]
then 
echo "Indexing of reference genome is done"
echo "Mapping the inputs to the reference"
fi
# Mapping your input pair reads to the reference 
bwa mem -R '@RG\tID:foo\tSM:bar\tLB:library1' $ref $reads1 $reads2 > lane.sam
if [[ $verbose -eq 1 ]]
then 
echo "Mapping is done"
fi
# To eradicate an error at the sorting step
samtools faidx $ref
# To eradicate an error at the sorting step
samtools dict $ref -o chr17.dict
if [[ $verbose -eq 1 ]]
then 
echo "sorting sam and converting it to a bam file"
fi
# To overwrite the present files 
if [[ -f lane_fixmate.bam ]]
then
rm lane_fixmate.bam
fi
if [[ -f lane_sorted.bam ]]
then
rm lane_sorted.bam
fi
if [[ $verbose -eq 1 ]]
then 
echo "Running fixmate to remove noise"
fi
samtools fixmate -O bam lane.sam lane_fixmate.bam
mkdir temp
cd temp/
mkdir lane_temp
cd
else echo "reference genome is missing" && exit
fi
if [[ $verbose -eq 1 ]]
then 
echo "Sorting the filtered fixmate bam file"
fi
# sorting the output bam file 
samtools sort -O bam -o lane_sorted.bam -T ~/temp/lane_temp lane_fixmate.bam 
# Indexing the sorted bam file
if [[ $verbose -eq 1 ]]
then 
echo "Indexing the sorted bam file"
fi
samtools index ~/lane_sorted.bam
# performing improvement to reduce number of miscalls of INDELS
if [[ $verbose -eq 1 ]]
then 
echo "Improvement going on"
fi
if [[ $realign -eq 1 ]]
then
java -Xmx2g -jar ~/GenomeAnalysisTK.jar -T RealignerTargetCreator -R $ref -I ~/lane_sorted.bam -o lane.intervals -known $millsFile 
# This step compensates the covariantes from first improvement step and realigning the bam file from first step
java -Xmx4g -jar ~/GenomeAnalysisTK.jar -T IndelRealigner -R $ref -I ~/lane_sorted.bam -targetIntervals lane.intervals -known $millsFile -o lane_realigned.bam 
fi
if [[ $verbose -eq 1 ]]
then 
echo "Indexing the realigned file"
fi
if [[ $index -eq 1 ]]
then 
# Indexing the output bam file after the improvement
samtools index lane_realigned.bam
fi
# Variant calling
if [ -f *.vcf ]
then
echo " vcf file already exists"
echo "If you want to overwrite the file, press Y and If you want to continue with the same file, press N "
read free
if [[ $free == Y ]]
then 
rm *.vcf
else
echo "exiting the script"
exit 
fi
fi
if [[ $verbose -eq 1 ]]
then 
echo "Converting BAM file into a vcf file using bcftools"
fi
# Convert BAM file into genomic positions using bcftools
bcftools mpileup -Ou -f $ref lane_realigned.bam | bcftools call -vmO z -o $output
if [[ $verbose -eq 1 ]]
then 
echo "Improvement completed and vcf file is made"
fi
# Unzip the output vcf file 
if [[ $gunzip -eq 1 ]]
then 
echo "vcf is being unzipped"
gunzip $output
fi
if [[ $verbose -eq 1 ]]
then 
echo "VCF file has been created"
fi
