#!/usr/bin/env perl
use v5.016;
use strict;
use warnings;

use autodie;

use open qw(:std :utf8);

use JSON::PP qw( encode_json );

sub tsv {
  my $filename = shift;

  # read the header (field names)
  open my $fp, '<:utf8', $filename;
  my $header = <$fp>;
  chomp $header;
  my @cols = split/\t/, $header;
  my $pri_col = shift @cols;

  # read every row and add to the list
  my %result;
  while (my $row = <$fp>) {
    chomp $row;
    my @r = split /\t/, $row;
    my $pri_r = shift @r;

    my %h;
    foreach my $i (0 .. $#cols) {
      if ($r[$i]) {
        $h{$cols[$i]} = $r[$i];
      }
    }

    die "Duplicate primary key $pri_r" if exists $result{$pri_r};
    $result{$pri_r} = \%h;
  }

  return \%result;
}

die "Usage: $0 roms.tsv pro.tsv" unless scalar @ARGV == 2;

my $roms = tsv($ARGV[0]);
my $pro = tsv($ARGV[1]);

# glue the two together
#  Stella PRO is md5-based,
#  ROMS folder is unique filenames
for my $filename (sort keys %$roms) {
  #say "---------------------------------------------------------------------";
  #say $filename;
  my $p = $pro->{$roms->{$filename}{md5}};
  if ($p) {
    $roms->{$filename}{image} = $p->{"cart.name"} . '.png';
    # check for enhancement possibility
    my $needs_fix = 0;
    foreach my $field (sort keys %$p) {
      next unless $field eq 'cart.url' or $field eq 'cart.note';
      if (! $roms->{$filename}{$field}) {
        $roms->{$filename}{$field} = $p->{$field};
        #say "Updated $field to $p->{$field}";
      } elsif ($roms->{$filename}{$field} ne $p->{$field}) {
        $needs_fix = 1;
      }
    }

    if ($needs_fix == 2) {
      # show a diff and offer some options
      foreach my $field (sort keys %$p) {
        if ($roms->{$filename}{$field} && $roms->{$filename}{$field} ne $p->{$field}) {
            say "$field: == R: " . $roms->{$filename}{$field} . "' <=> P: '" . $p->{$field} . "'";

redo:
              # ask user for input
              say "Keep (R)om, Keep (P)ro, (E)dit?";
              my $action = uc(<STDIN>); chomp $action;
#my $action = 'R';
              if ($action eq 'P') {
                $roms->{$filename}{$field} = $p;
              } elsif ($action eq 'R') {
                #nothing
              } elsif ($action eq 'E') {
                my $e = <STDIN>; chomp $e;
                $roms->{$filename}{$field} = $e;
              } else {
                goto redo;
              }
        }
      }
    }
  }
}

# regroup
my %groups;
for my $filename (sort keys %$roms) {
  my $g = $roms->{$filename}{group};
  if (! exists $groups{$g}) {
    $groups{$g} = [];
  }
  $roms->{$filename}{filename} = $filename;
  push @{$groups{$g}}, $roms->{$filename};
}

foreach my $group (sort keys %groups) {
  my $primary_count = 0;
  for my $game (@{$groups{$group}}) {
    if ($game->{primary}) { $primary_count ++; }
  }
  if ($primary_count != 1) {
    say STDERR "$group: $primary_count primarys";
  }
}

# dump
print encode_json(\%groups);
