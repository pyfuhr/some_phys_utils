# Recalculate reflection spectra
# Usage: python refl_calc.py al-refer al-exp exp1 exp2 exp3...

import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='calc reflection spectra')
parser.add_argument('al_ref', type=str, help='Al reference')
parser.add_argument('al_exp', type=str, help='Al experemental')
parser.add_argument('exps', type=str, nargs='+', help='List of experemntal')
args = parser.parse_args()

# load reference
ref = pd.read_csv(args.al_ref, header=None, names=['wv', 'val'], sep=';')
ref['val'] = ref['val'] / 100

# load al measurement
al_izm = pd.read_csv(args.al_exp, sep=' ', header=None, skiprows=1, names=['wv', 'v1', 'v2'], index_col=False)
al_izm['val'] = (al_izm['v1'] + al_izm['v2']) / 2

# recalculate al

from scipy.interpolate import interp1d
import numpy as np

x1, y1_0 = ref['wv'], ref['val']
x2 = al_izm['wv']

f = interp1d(x1, y1_0, kind='linear', fill_value="extrapolate")

y1 = f(x2)
y2 = al_izm['val']
coef = y1/y2

for sample_file in args.exps:
	smp_izm = pd.read_csv(sample_file, sep=' ', header=None, skiprows=1, names=['wv', 'v1', 'v2'], index_col=False)
	smp_izm['val'] = ((smp_izm['v1'] + smp_izm['v2']) / 2)*coef
	smp_izm[['wv', 'val']].to_csv(sample_file+'_recalc.csv')
	plt.plot(smp_izm['wv'], smp_izm['val'], label=sample_file)

plt.legend()
plt.show()
