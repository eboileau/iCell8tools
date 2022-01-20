#! /usr/bin/env perl

use strict;
use Bio::SeqIO;
use Getopt::Long;

my ($READ, $SAMPLE, $OUT) = @ARGV;
my $filename = "${OUT}/${SAMPLE}_barcodes.fastq.gz";

open my $IN, '-|', 'gunzip', '-c', $READ;
open(FH, "|gzip -c > $filename") || die "Could not open output file!";

# print "filename: $READ\n";
# print "filename: $filename\n";

$| = 1;
while( my $header = <$IN> )
  {
    
    my $seq = <$IN>;
    my $spac = <$IN>;
    my $qual = <$IN>;

    $header=~/\:(\w+\+\w+)/;
    my $id=$1;

    $id=~s/\+//;
    chomp($id);
    print FH $header;
    print FH $id,"\n";
    print FH "+\n";
    print FH "E"x length($id),"\n";
    
  }

close(IN);
close(FH);
