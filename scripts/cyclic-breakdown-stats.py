import sys
import glob
from ColumnDataFile import ColumnDataFile as CDF
import matplotlib.pyplot as plt
from pylab import *
import numpy
import operator
import PlotUtility


def ExtractCoords(files):
  	files = [open(f) for f in files]
  	lines = [f.readline().split() for f in files]
	map(lambda x: x.close(), files)

	data = [numpy.array([int(i) for i in l]) for l in lines]
	data = reduce(operator.add, data)
	return numpy.array(data)
	
#files_cold = glob.glob(sys.argv[1])
files_cold = glob.glob('[1-5]/'+sys.argv[1]+'*')
files_hot = glob.glob('[6-9]/'+sys.argv[1]+'*')
files_hot = files_hot + glob.glob('10/'+sys.argv[1]+'*')

data = ExtractCoords(files_cold)
totals = data[:2]
cycles = data[5:13]
print "Cold"
print totals
print cycles

#data = ExtractCoords(files_hot)
#totals = data[:2]
#cycles = data[5:13]
#print "Hot"
#print totals
#print cycles



