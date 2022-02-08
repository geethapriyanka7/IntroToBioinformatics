# IntroToBioinformatics
This is an example of another complex problem that has a rather simple solution. NW algorithm is a classical bioinformatics algorithm designed to obtain optimal global alignment for a given pair of sequences.  The algorithm falls under the class of dynamic programming which in simple language is theclass of algorithm that work by breaking a problem into subproblems, solving each subproblem and joining the solutions to reach the global solution.
The algorithm can be divided into three steps:
1. Initialization: Construction of the matrix with the two sequences as each axis and selection of a suitable scoring system.  For simplicity, let’s have three types of scores:
a. Match = +1
b. Mismatch = -1
c. Gap = -1
2. Matrix filling: Filling the matrix based on the scoring system.  This occurs one row at a time, starting from the topmost row.  Each cell in the matrix derives the value from the adjacent cells located to the left, top-left or on top of the current cell.  The match score is added or gap/mismatch penalty is subtracted from these adjacent cells and the maximum value is carried over to the current cell (Figure 1).
3. Backtracking: Once the matrix has been filled up, backtracking is done to compute the optimal alignment(s).  The backtracking step starts from the very last cell filled in the matrix (the bottom-right cell) and proceeds to the first cell filled in matrix (the cell with 0 in the upper left corner of the matrices in Figure 1).  This backtrack path is computed by moving through  the  adjacent  cells  (cells  to  the  left,  top-left  and  on  top  of  the current  cell)  with  the  maximum  score  such  that  the  path  has  the maximum total score (Figure 2).  If multiple paths exist, then all of them are  considered  to  be  the  optimal  paths.    This  path  is  converted  to  an alignment by the following rule: the path moves diagonally to the left if there is a match or if the maximum score of the adjacent cells is present in the diagonal left cell.  If either of these are true, the two corresponding characters from each sequence are aligned together. When the maximum  score  is  obtained  by  moving  horizontally,  then  a  gap  is introduced in the sequence on the vertical axis, and if the path moves vertically,  then  a  gap  is  introduced  in  the  sequence  on  the  horizontal axis.
Backtracking rules:
1. Always  take  the  diagonal  when  the  diagonal  is  either  (1)  the  highest score or (2) tied for highest score
2. If the diagonal is not the highest score, take the "Up" if it is either (1) the highest score or (2) tied for highest score.
3. Take the "Left" if the diagonal and “Up” are not the highest

Syntax: ./ nwAlign.py <input FASTA file 1> <input FASTA file 2>
Example usage: ./ nwAlign.py seq1_nw.fa seq2_nw.fa
seq1.fa contains:
>seq1_nw.fa
ATTGCC
seq2.fa contains:
>seq2_nw.fa
AGTCC
Output format:
ATTGCC
|*| ||
AGT-CC
Alignment score: 2
“|” represents a match
“*”represents a mismatch

