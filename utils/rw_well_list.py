#! /usr/bin/env python3

import os
import argparse
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def _simple_fill(text, width=60):
    return '\n'.join(text[i:i+width] 
                        for i in range(0, len(text), width))


def _write_fasta_entry(out, header, seq, wrap=False):
    out.write(">")
    out.write(header)
    out.write("\n")

    if wrap:
        seq = _simple_fill(seq)

    out.write(seq)
    out.write("\n")
    

def write_fasta(seqs, filename, compress=True, wrap=True, progress_bar=False):

    if compress:
        import gzip
        out = gzip.open(filename, 'wt')
    else:
        out = open(filename, 'w')

    if progress_bar:
        import tqdm
        seq_iter = tqdm.tqdm(seqs, leave=True, file=sys.stdout)
    else:
        seq_iter = seqs

    for header, seq in seq_iter:
        _write_fasta_entry(out, header, seq, wrap)
        
    out.close()

    
def rc(s):
    from Bio.Seq import Seq
    return str(Seq(s).reverse_complement())


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Sort well list file and write barcode fasta.')

    parser.add_argument('well', help='The well list file.')
    parser.add_argument('sample', help='The sample name.')
    parser.add_argument('dirloc', help='The barcodes fasta (and well file) output directory')

    parser.add_argument('-rc', '--reverse-complememt', help='''Whether to reverse-complement 
                        the second barcode half or not. If not, well file is symlinked to 
                        the destination.''', action='store_true')

    args = parser.parse_args()
    
    src = args.well
    dst = os.path.join(args.dirloc, f"{args.sample}_WellList.TXT")
    
    well = pd.read_csv(src, sep='\t')
    well[['b1', 'b2']] = well['Barcode'].str.split('+', 1, expand=True)
    if args.reverse_complememt:
        colnames = well.columns
        well['b2'] = well['b2'].apply(rc)
        well['Barcode'] = well[['b1', 'b2']].agg('+'.join, axis=1)
        well = well[colnames]
        well.to_csv(dst, sep='\t')
    else:
        os.symlink(src, dst)

    # write barcodes
    all_seqs = [(b.replace('+', ''), b.replace('+', '')) for b in well['Barcode'].values]
    filename = os.path.join(args.dirloc, f"{args.sample}_barcodes.fa")
    write_fasta(all_seqs, filename, compress=False, wrap=True, progress_bar=False)


if __name__ == '__main__':
    main()
    
