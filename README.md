
Workflow for iCell8 data 
========================

This `snakemake` pipeline can be used to process scRNA-seq data generated using the ICELL8 system or similar plate-based (Smart-seq) technologies, provided there are no cell barcode sequences and no UMIs (for Smart-seq3, *e.g.* a different workflow has to be used). Cell barcodes (whitelist) for demultiplexing are taken from the well list files (`Barcode`). A single FASTQ file per plate or chip is demultiplexed to generate individual FASTQ files using [Flexbar](https://github.com/seqan/flexbar/wiki), one per cell barcode, which are then aligned, quantified, and converted to a CellRanger-like input format using [STARsolo](https://github.com/alexdobin/STAR/blob/master/docs/STARsolo.md#plate-based-smart-seq-scrna-seq).


Getting started
===============

## Input

- FASTQ and well list files
- Flexbar adapter sequences
- STAR index and annotations (GTF)

## Output

- FastQC (MultiQC) output
- Solo.out (containing features.tsv, barcodes.tsv, and matrix.mtx)


## Dependencies

The current pipeline is not installable. I use a generic conda environment (`snakemake`) that must minimally contain python, with numpy, pandas, and biopython (see `environment.txt`). Additional dependencies [FastqQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc), [MultiQC](https://multiqc.info), [Flexbar](https://github.com/seqan/flexbar), and [STAR](https://github.com/alexdobin/STAR) are currently handled via the environment modules.


## Usage

Edit `config.yml`, and 

```bash
snakemake --configfile ../config.yaml -j <num_cores> all --use-envmodules
```

or edit `config.json` and/or `runjob` to submit using [Slurm](https://slurm.schedmd.com/documentation.html)

```bash
sbatch runjob
```

## Notes

I had conflicting versions of `bio-perl` which could not be resolved in my environment, so I am currently using the system's `perl` executable `/usr/bin/perl` (hard coded).

Flexbar crashed systematically for samples with large number of files. This was resolved by increasing `ulimit -n 1048576`.

For MultiQC to work, one might have to export the following environment variables before:

```
export LC_ALL=C.UTF-8                                                                                                                                                   
export LANG=C.UTF-8
```

## Todo

Compare to Cogent NGS Analysis Pipeline (Takara Bio).



