from ColumnDataFile import ColumnDataFile as CDF
import matplotlib.pyplot as plt
from pylab import *
import Smoothing
import sys,numpy,itertools,operator,glob

from scipy import *
import PlotUtility

# groups the signal into 0s and 1s and returns the length of the groups
def CutUpCycleBits(data):
	# now cut up the data into chunks and get their lengths
	for k,g in itertools.groupby(data):
  		# if on then print the cycle life
		if k: yield len(list(g))
  		# if off... print the break life
		#if not k: print len(list(g))

# returns a list with the length of the on or off times of the signal in the given file
def getLifespan(file,axs=None):

	cdf = CDF(file)
	# raw data
	data = cdf[0]

	# smooth out the data and digitize above a certain threshold
	smooth = Smoothing.window_smooth(numpy.array(data), window_len=40, window='blackman')
	smooth = smooth - 0.18
	new_data = numpy.ceil(smooth)
  	smooth = smooth + 0.18

	if axs:
		axs.plot(data[1200:2800], linewidth=2.5, color='k', linestyle=':', alpha=0.7, label=r'$C(t)$')
		axs.plot(smooth[1200:2800], linewidth=2.0, color='r', linestyle='-', alpha=0.7, label=r'$C_s(t)$')
		axs.plot(new_data[1200:2800], linewidth=3.5, color='g', linestyle='-', alpha=0.8, label=r'$f(t)$')

  	return [c for c in CutUpCycleBits(new_data)]

bns = arange(0,16000,1000)
width=0.35


def PlotCycleBits(files,hot=None):
	lives = [getLifespan(f) for f in files]
	lives = reduce(operator.add,lives)

	total = len(lives)
	histo, edges = numpy.histogram (lives, bins=bns)
	histo = histo * 100.0 / total

	if hot:
		plt.bar([i+width/2 for i in range(len(bns))[:-1]], histo, width, color='r', align='center')
	else:
		plt.bar([i-width/2 for i in range(len(bns))[:-1]], histo, width, color='b', align='center')


fig = plt.figure(num=1, facecolor='w', edgecolor='w', frameon=True)
axs = fig.add_subplot(1,1,1)

files_cold = glob.glob('[1-5]/so2.cyclic-SO-lifespan.dat')

getLifespan (sys.argv[1],axs)
files_hot = glob.glob('[6-9]/so2.cyclic-SO-lifespan.dat')
files_hot = files_hot + glob.glob('10/so2.cyclic-SO-lifespan.dat')



#PlotCycleBits(files_cold)
#PlotCycleBits(files_hot,True)

xlabel (r'Time', fontsize=46)
axs.set_ylim(-0.1,1.2)
#ylabel ('', fontsize=46)
#xticks (arange(len(bns)), bns/1000, fontsize=32)
xticks ([])
yticks ([0,1],['No Cycle','Cycle'],fontsize=32)


PlotUtility.ShowLegend(axs)
fig.subplots_adjust(top=0.96, bottom=0.15,left=0.3,right=0.96)
#plt.savefig('analysis/cycle-debouncing.png',dpi=90)
plt.show()
