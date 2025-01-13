#!/usr/bin/env perl
use v5.016;
use strict;
use warnings;

use autodie;

use open qw(:std :utf8);

use Encode qw( decode_utf8 );
use Digest::MD5;

die "Usage: $0 ROMS" unless scalar @ARGV == 1;

# get the roms from the ROMS folder
my @roms = do {
  opendir my $dir, $ARGV[0];
  grep(/\.bin$/i, readdir $dir);
};

# TSV header
say join("\t", "filename", "filesize", "md5", "group", "primary", "name", "alt", "aka", "beta", "year", "mfg", "serial", "proto", "region", "controller", "comp", "size", "disam", "multi");

foreach my $filename (@roms) {
  # get the md5 of the file
  $filename = decode_utf8($filename);

  open my $fh, '<:raw', $ARGV[0] . '/' . $filename;
  # get filesize
  my $filesize = -s $fh;
  my $md5 = Digest::MD5->new->addfile($fh)->hexdigest;
  close $fh;

  # parse title into game components
  my $title = $filename;

  my $primary = '';
  if ($title =~ m/ ~\.bin$/) {
    $primary = 1;
    $title =~ s/ ~\.bin$//;
  } else {
    $title =~ s/\.bin$//;
  }

  my $disam = '';
  if ($title =~ m/ \[(.+)\]$/) {
    $disam = $1;
    $title =~ s/ \[.+\]$//;
  }
  my $proto = '';
  if ($title =~ m/ \(Prototype\)/) {
    $proto = 1;
    $title =~ s/ \(Prototype\)//;
  }
  my $region = '';
  if ($title =~ m/ \((PAL|SECAM)\)/) {
    $region = $1;
    $title =~ s/ \($region\)//;
  }
  my $size = '';
  if ($title =~ m/ \((\d+K)\)/) {
    $size = $1;
    $title =~ s/ \($size\)//;
    chop $size;
  }

  my $beta = '';
  my $group = '';
  if ($title =~ m/ \(AKA ([^)]+)\)/) {
    $group = $1;
    $title =~ s/ \(AKA $group\)//;
  }
  elsif ($title =~ m/ \(([^)]+) Beta\)/) {
    $group = $1;
    $beta = 'Beta';
    $title =~ s/ \($group Beta\)//;
  }

  my $controller = '';
  if ($title =~ m/ \((Paddle|Kid's Controller|Keyboard Controller|Driving Controller|Track & Field Controller|Mindlink Controller|Kid Vid Voice Module|Joyboard|Booster Grip|Light Gun|Dual Control Module|Video Touch Pad|TRON Joystick|Bike Trainer)\)/) {
    $controller = $1;
    $title =~ s/ \($controller\)//;
  }

  my $comp = '';
  if ($title =~ m/ \((32 in 1|Double-Game Package|Supergames 8 in 1|4 Game in One|2600 Screen Search Console|Canal 3 - Intellivision|\d of \d)\)/) {
    $comp = $1;
    $title =~ s/ \($comp\)//;
  }

  if ($title =~ m/ \((Hack|Preview)\)/) {
    $beta = $1;
    $title =~ s/ \($beta\)//;
  }
  my ($name, $aka, $year, $mfg, $serial, $multi) = ('', '', '', '', '', '', '', '', '', '', '', '', '');

  # the remaining components must be parsed right-to-left
  #  generally: Name (etc) (AKA) (year) (mfg) (serial)
  if ($title =~ m/^(.+) \(([^)]+)\) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\) \(([^)]+)\) \((\d\d?)\) \(([^)]+)\)$/) {
    ($name, $aka, $year, $mfg, $multi, $serial) = ($1, $2, $3, $4, $5, $6);
  } elsif ($title =~ m/^(.+) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\) \(([^)]+)\) \((\d\d?)\) \(([^)]+)\)$/) {
    ($name, $year, $mfg, $multi, $serial) = ($1, $2, $3, $4, $5);
  } elsif ($title =~ m/^(.+) \(([^)]+)\) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\) \(([^)]+)\) \(([^)]+)\)$/) {
    ($name, $aka, $year, $mfg, $serial) = ($1, $2, $3, $4, $5);
  } elsif ($title =~ m/^(.+) \(([^)]+)\) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\) \(([^)]+)\)$/) {
    ($name, $aka, $year, $mfg) = ($1, $2, $3, $4);
  } elsif ($title =~ m/^(.+) \(([^)]+)\) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\)$/) {
    ($name, $aka, $year) = ($1, $2, $3);
  } elsif ($title =~ m/^(.+) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\) \(([^)]+)\) \(([^)]+)\)$/) {
    ($name, $year, $mfg, $serial) = ($1, $2, $3, $4);
  } elsif ($title =~ m/^(.+) \((19\d\d|\d\d-[X\d][X\d]-1?9?\d\d)\) \(([^)]+)\)$/) {
    ($name, $year, $mfg) = ($1, $2, $3);
  } elsif ($title =~ m/^(.+) \(([^)]+)\) \(([^)]+)\) \(([^)]+)\)$/) {
    ($name, $aka, $mfg, $serial) = ($1, $2, $3, $4);
  } elsif ($title =~ m/^(.+) \(([^)]+)\) \(([^)]+)\)$/) {
    ($name, $aka, $mfg) = ($1, $2, $3);
  } elsif ($title =~ m/^(.+) \(([^)]+)\)$/) {
    ($name, $mfg) = ($1, $2);
  } else {
    $name = $title;
  }

  # also sometimes they try to cram an AKA in there
  my $alt = '';
  if ($name =~ m/ - (.+)$/) {
    $alt = $1;
    $name =~ s/ - $alt//;
  }

  if ($group eq '') { $group = $name }
  $group =~ s/ - .+$//;

  # append or replace size info
  say join("\t", $filename, $filesize, $md5, $group, $primary, $name, $alt, $aka, $beta, $year, $mfg, $serial, $proto, $region, $controller, $comp, $size, $disam, $multi);
}
