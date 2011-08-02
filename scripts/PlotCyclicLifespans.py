import sys,glob,operator
from ColumnDataFile import ColumnDataFile as CDF
import matplotlib.pyplot as plt
import numpy,Smoothing

colors = ['b','r']
color_choice = 0

def PlotSpans (files, axs):
	cdfs = [CDF(f) for f in files]
	data = [c[0] for c in cdfs]
	data = reduce(operator.add, data)

	hist,edges = numpy.histogram(data, range=(0.0,400.0), bins=200)

  	hist = Smoothing.window_smooth(hist)
	axs.plot(edges[:-1],hist,color=colors[color_choice])
  	color_choice = color_choice + 1

fig = plt.figure(num=1, facecolor='w', edgecolor='w', frameon=True)
axs = fig.add_subplot(111)

files = glob.glob('[1-5]/'+sys.argv[1]+'*')
PlotSpans(files,axs)

files = glob.glob('[6-9]/'+sys.argv[1]+'*')
files = files + glob.glob('10/'+sys.argv[1]+'*')
PlotSpans(files,axs)

plt.show()
#plt.bar([i-width/2 for i in range(len(new_bins[:-1]))], cold_histo, width, color='b', align='center')
