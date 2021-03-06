#!/usr/bin/perl
use strict;
use warnings;

use Encode qw( decode FB_QUIET );

binmode STDIN, ':bytes';
binmode STDOUT, ':encoding(UTF-8)';

my $out;

while ( <> ) {
    $out = '';
    while ( length ) {
        # consume input string up to the first UTF-8 decode error
        $out .= decode( "utf-8", $_, FB_QUIET );
        # consume one character; all octets are valid Latin-1
        $out .= decode( "iso-8859-1", substr( $_, 0, 1 ), FB_QUIET ) if length;
    }
    print $out;
}
