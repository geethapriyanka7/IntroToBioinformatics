# IntroToBioinformatics
This is a very common task in genome analysis.  Often, we want to find functional elements that overlap with other elements, e.g. transcription start sites contained in transposable  elements,  predicted  transcription  factor  binding  sites  within  DNase hypersensitivity sites, or even some set of genes or horizontally transferred regions.  
Maybe  you  found  some  peaks  in  your  ChIP-seq  data  and  you  want  to  see  if  those overlap with known enhancers, or perhaps you have a set of SNPs and you would like to know what genes they fall in.  If you do not know what those words mean, go look them up!
Comparing ALL coordinates of the first set versus ALL coordinates of the second set will work for small sets only. That method scales with the multiplication of the sizes of the two sets.  If you have 106 members in each set (not at all unrealistic) do you want to make 1012 comparisons?  You need to find a better way.
What the script does:
1. Take  in  two  files  that  contain  sets  of  coordinates  in  BED  format. You  can assume  that  the  contents  of  both  files  are  sorted  by  chromosome,  start  and stop.  Having the data sorted allows you to greatly speed up the process of the overlap.
2. Take in an option for the minimum percent overlap, i.e. percent of bases of any given member of the first set that must be in a member of the second set to be counted as overlapping.
3. Print to a file the members of the first set which overlap with the second set and meet the minimum overlap and other conditions specified.  Each overlap should only be printed once in this manner.
4. Allow an option to print both the member of the first set and the member of the  second  set  that  it  overlaps  with  on  the  same  line,  in  effect  ‘joining’  the rows.

Examples:
Overlap of the following two sets with a minimum of 100% overlap would yield one row.
Set 1:
chr1 1500 1750 1 0 +
chr1 4500 5000 2 0 +
chr1 8500 9500 3 0 +
Set 2:
chr1 1000 2000 a 0 -
chr1 3000 4000 b 0 -
chr1 9000 11000 c 0 -
Output:
chr1 1500 1750 1 0 +
If the joining option (from #4) was given:
chr1 1500 1750 1 0 + chr1 1000 2000 a 0 -
If the minimum overlap was 50% instead of 100% you would get two rows:
chr1 1500 1750 1 0 +
chr1 8500 9500 3 0 +
Notes:
The overlap of two coordinates can be calculated as MIN(stop_one, stop_two) – MAX(start_one, start_two)Anything greater than 0 is the number of overlapping bases, otherwise it indicates no overlap. 
Deliverables:
Run your script with: ./overlapBed.py -i1 TE.bed -i2 Intron.bed -m 80 -o output
Syntax: ./overlapBed.py  -i1  <Input  file  1>  -i2  <Input  file  2>  -m  <INT:  minimal overlap> [-j Optional: join the two entries] –o <Output file>
Example  command:  ./<gtusername>_overlapBed.py  -i1  TE.bed  -i2  Intron.bed  -m  50  -j  -o testOutput
This command finds overlaps between TE.bed and Intron.bed, prints out the pairs of overlapping entries from both bed files that have minimum percent overlap of 50%.
