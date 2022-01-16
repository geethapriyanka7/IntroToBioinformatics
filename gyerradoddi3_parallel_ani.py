#!/usr/bin/env python3
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i1", help="Input Bed file 1", required = True)
parser.add_argument("-i2", help="Input Bed file 2", required = True)
parser.add_argument("-m", help = "Minimun overlap to be shown", required = True)
parser.add_argument("-j", "--join", help = "Compare files", action="store_true")
parser.add_argument("-o", help = "Output file", required = True)
args = parser.parse_args()