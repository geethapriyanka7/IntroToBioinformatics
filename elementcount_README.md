# IntroToBioinformatics
The  objective  of  the  assignment  is  simple  –  given  a  set  of  coordinates represented in a BED file, find the number of times each coordinate occurs.  
As an example, consider the following BED file:
chr1 10 15
chr1 12 15
chr1 13 20
where  each  line  represents  a  genomic  element,  the  first  column  is  the chromosome, second column is the starting position of the element, and the third column is the ending position of the element.  
Please note 
1. Write the output to STDOUT
2. The  third  column  is  exclusive.I.e.,chr1 10 12 represents an element that starts at 10 and ends at 11.
3. The BED file may have more than 3 columns, but the first three will always represent chromosome, start, and stop.
Your script should be able to process the BED file and produce the following output:
chr1 10 12 1
chr1 12 13 2
chr1 13 15 3
chr1 15 20 1
where the last column is the coverage and represents the coverage of the coordinates for that row/element.
Please  ensure  that  your  script  produces  output  coordinates  that  are  non-overlapping.

Syntax: ./ elementCount.py [-h] -i <input file name>
Example usage:
./ elementCount.py -i input.bed
