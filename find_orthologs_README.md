# Finding orthologous genes using BLAST

Identifying orthologous genes between different genomes is a very common task, and it’s one of the, perhaps in fact the absolute. There are a number of different ways of defining 
orthologous genes, we are going to do it in a very simple way: reciprocal best BLAST hits.    
Reciprocal  best  BLAST  hits  are  pairs  of  sequences  where  the  best  BLAST  hit  for  each sequence is the other sequence.
Consider you have a sequence A from species sA whose best hit in species sB is the sequence B.  A will be considered a reciprocal best hit of B if the best hit of B in species sA is A.

Example: when you BLAST the complete set of human coding sequences against the complete set of mouse coding sequences, the best hit for the human gene histone H3.1 is the mouse gene histone  H3.1  and  vice  versa.    These  two  genes  would  be  considered  reciprocal  best  hits  and orthologous.   Please do note that this is an overly simplistic way of defining orthologous.  If, for example, there had been a gene duplication event in mouse lineage yielding two copies of the histone H3 gene, then simply picking one as the ortholog for the human version would be a rather bad idea.
You will need the makeblastdb and the blast program.  You can get them by installing the NCBI toolkit located here ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST. Script will take in as arguments two sets of protein or nucleotide sequences, one from each genome.  
It should create a database from each using makeblastdb, query each set against the opposite database, and remove the databases files and any other temporary file that you created in the process.  From the results of the queries, it should find those sequence pairs which are reciprocal best hits and give them as output.

 Code: find_orthologs.py
 Output: Your output file with orthologous genes named find_ortholog.output
