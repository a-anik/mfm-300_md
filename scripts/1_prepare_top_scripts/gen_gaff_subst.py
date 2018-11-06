#!/usr/bin/env python

import argparse
import numpy as np
from collections import defaultdict

cal = 4.184
angs = 0.1

def ascending(t):
    x = tuple(t)
    if x[::-1] < x:
        x = x[::-1]
    return x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates file with GAFF->GROMACS substitutions')
    parser.add_argument('frcmod', help='frcmod file with all parameters')
    args = parser.parse_args()

    sect = None
    with open(args.frcmod, 'r') as inpf:
        for line in inpf:
            f = line.split()
            if len(f) == 1 and f[0] == f[0].upper():
                sect = f[0]
                continue
            elif len(f) == 0 or not sect:
                continue
            if sect == 'NONBON':
                print('s/nb@{:2s}@/{:10.6f} {:10.6f}/'.format(f[0], float(f[1])*2**(-1./6)*2*angs, float(f[2])*cal))
            elif sect == 'BOND':
                key = line[:5]
                val = line[5:].split()
                print('s/b@{}@/{:10.5f} {:12.3f}/'.format(key, float(val[1])*angs, float(val[0])*2*cal/angs**2))
            elif sect == 'ANGLE':
                key = line[:8]
                val = line[8:].split()
                print('s/a@{}@/{:10.2f} {:12.3f}/'.format(key, float(val[1]), float(val[0])*2*cal))
            elif sect == 'DIHE':
                key = line[:11]
                key = '-'.join(ascending(key.split('-')))
                val = line[11:].split()
                print('s/d@{}@/{:10.2f} {:12.3f} {:5d}/'.format(key, float(val[2]), float(val[1])/float(val[0])*cal, int(float(val[3]))))
            elif sect == 'IMPROPER':
                key = line[:11]
                val = line[11:].split()
                print('s/i@{}@/{:10.2f} {:12.4f} {:5d}/'.format(key, float(val[1]), float(val[0])*cal, int(float(val[2]))))
