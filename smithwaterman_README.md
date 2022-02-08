# IntroToBioinformatics
The  Smith-Waterman  algorithm  is  a  variant  of  Needleman-Wunsch  that  is applicable for local alignments.  The differences between the algorithms are:
1. There are no negative values within the matrix.  If subtracting a gap penalty or mismatch score results in a negative value, the value for the cell becomes 0.
2. The traceback starts with the cell with the highest value and ends when a 0 valued cell is encountered during the traceback.

The scoring scheme is +3 for match, -3 for mismatch and -2 for gap.  Notice the lack of negative values and the traceback path starting from the middle of the matrix.
Syntax: ./ swAlign.py <input FASTA file 1> <input FASTA file 2>
Example usage: ./swAlign.py seq1_sw.fa seq2_sw.fa
seq1.fa contains:
>seq1_sw.fa
TGTTACGG
seq2_sw.fa contains:
>seq2_sw.fa
GGTTGACTA
Output format:
GTT-AC
||| ||
GTTGAC
Alignment score: 1
