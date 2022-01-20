#! /usr/bin/env python3

import os
import argparse
import logging
import glob

import pandas as pd

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Sort well list file and write barcode fasta.')

    parser.add_argument('well', help='The well list file.')
    parser.add_argument('sample', help='The sample name.')
    parser.add_argument('dirloc', help='The data output directory')
    parser.add_argument('fastqs', help='The flexbar output directory')
    
    args = parser.parse_args()
    
    src = args.well
    dst = os.path.join(args.dirloc, f"{args.sample}_manifest.txt")
    
    well = pd.read_csv(src, sep='\t')
    barcodes = [b.replace('+', '') for b in well['Barcode'].values]
    
    all_files = glob.glob(os.path.join(args.fastqs, '*fastq.gz'))
    
    with open(dst, 'w') as f:
        for b in barcodes:
            filen = [os.path.basename(x) for x in all_files if b in os.path.basename(x)]
            f.write(f"{filen[0]}\t-\t{b}\n")
        
        
if __name__ == '__main__':
    main()
    
