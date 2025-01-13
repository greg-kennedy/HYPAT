#!/usr/bin/env perl
use v5.016;
use strict;
use warnings;

use autodie;

use open qw(:std :utf8);

use JSON::PP qw( decode_json );

sub parse_game {
  my $game = shift;

  # get cart name out
  my $title = $game->{Cart}{Name};

  ## Parses a "title" string into components
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

  $mfg =~ s/BitCorp/Bit Corporation/;
  $mfg =~ s/Parker Bros/Parker Brothers/;

  # (the above is wrong so here is some fixups)
  if ($aka) {
    if (! $year) {
      if ($aka =~ m/^\d\d\d\d(-.*)?$/) {
        $year = $aka;
        $aka = '';
      }
      elsif ($aka =~ m/^(\d\d)-(\d\d)-(\d\d\d\d)$/) {
        $year = "$3-$2-$1";
        $aka = '';
      }
    }
  }

  if (($game->{Cart}{Note} // '') =~ m/^AKA (.+)$/) {
    if (! $aka) {
      $aka = $1;
      $game->{Cart}{Note} = '';
    }
  }

  if ($group eq '') { $group = $name }
  $group =~ s/ - .+$//;

  # try to overlay cart.mfg onto mfg
  if ($game->{Cart}{Manufacturer}) {
    if (!$mfg || $game->{Cart}{Manufacturer} =~ m/$mfg/i) {
      $mfg = $game->{Cart}{Manufacturer};
      $game->{Cart}{Manufacturer} = '';
    } else {
      warn "eh " . $game->{Cart}{Manufacturer} . " vs " . $mfg;
    }
  } 

  # model no too
  if ($game->{Cart}{ModelNo}) {
    if (!$serial || $game->{Cart}{ModelNo} =~ m/$serial/i) {
      $serial = $game->{Cart}{ModelNo};
      $game->{Cart}{ModelNo} = '';
    } else {
      warn "eh " . $game->{Cart}{ModelNo} . " vs " . $serial;
    }
  } 

  say join("\t", map { $_ // '' } ($game->{Cart}{MD5}, $game->{Cart}{Name}, $game->{Cart}{Manufacturer}, $game->{Cart}{ModelNo}, $game->{Cart}{Note}, $game->{Cart}{Rarity}, $game->{Controller}{Left}, $game->{Cart}{Url}, $name, $aka, $beta, $year, $mfg, $serial, $proto, $region, $controller, $comp, $size, $disam, $multi));
}

## Converts a Stella .pro file into a .tsv file
die "Usage: $0 stella.pro" unless scalar @ARGV == 1;

open my $fh, '<:utf8', $ARGV[0];

# TSV header
say join("\t", "md5", "cart.name", "cart.mfg", "cart.modelno", "cart.note", "cart.rarity", "controller.left", "cart.url", "name", "aka", "beta", "year", "mfg", "serial", "proto", "region", "controller", "comp", "size", "disam", "multi");

my %game;
while (my $line = <$fh>) {
  chomp $line;

  if ($line eq '' && %game) {
    parse_game(\%game);
    %game = ();
  } elsif ($line =~ m/^f?"([^"]+)" "(.*)"$/) {
    my $path = $1;
    my $val = $2;

    if ($path eq 'Cart.Highscore') {
      $val =~ s/\\"/"/g;
      $val = decode_json($val);
    }

    my @p = split /\./, $path;
    my $g = \%game;
    while (scalar @p > 1) {
      my $f = shift @p;
      $g = \%{$g->{$f}};
    }
    $g->{$p[0]} = $val;
  }
}

parse_game(\%game);

