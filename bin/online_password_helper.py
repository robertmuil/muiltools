#!/usr/bin/env python
"""
Simple script to simplify inputting complicated password to a website
that requires only part of the password (e.g. hartlinkonline portal)

DO NOT put password on command-line as it will be saved in terminal history.
Instead pass it on stdin once running.
"""

pwstr = ''
while True:
    inp = raw_input('Password [{}]: '.format(pwstr))
    if (inp is not None) and (len(inp) > 0):
        pwstr = inp
    pwnums = raw_input('which characters? ')
    try:
        pwix = [int(x) for x in pwnums.split(',')]
        for ii in pwix:
            print '{:01d}:\t{}'.format(ii, pwstr[ii-1])
    except IndexError:
        pass
