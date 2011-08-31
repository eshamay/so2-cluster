import sys,operator
import thread as threading
import numpy
import matplotlib.pyplot as plt
from pylab import *


CYCLE_TYPES = ['single','double','triple','quadruple','triple-A','triple-B']
HARTREE2KCAL = 627.509

def ParseLine(line):
	line = line.split(',')
	line = map(lambda x: x.split(':')[1],line)
	#return (int(line[0]), CYCLE_TYPES.index(line[1].strip()), float(line[3])*HARTREE2KCAL)
	return (int(line[0]), CYCLE_TYPES.index(line[1].strip()), float(line[3]))

def ParseFile(file):
	dat = [ParseLine(line) for line in file.readlines()]
	return dat

def LoadFile():
	file = open(sys.argv[1], 'r')
	data = ParseFile(file)
	file.close()
	return data

isCold = lambda x: x[0] < 6
isHot = lambda x: x[0] > 5

isSingle = lambda x: x[1] == 0
isDouble = lambda x: x[1] == 1
isTriple = lambda x: x[1] in [2,4,5]
isQuadruple = lambda x: x[1] == 3
cycle_type_preds = [isSingle,isDouble,isTriple,isQuadruple]

def Energies(data):
	return map(operator.itemgetter(2),data)

def energyStats(energies):
	return (numpy.mean(energies), numpy.std(energies))


class EnergyData:
	def loadData(self,data):
		self.data = data
	def calcStats(self):
		print "calcing stats"
		self.stats = energyStats(Energies(data));

def loadEnergyData(data_class,energy_data,pred):
	data_class.loadData(filter(pred,energy_data))
	data_class.calcStats()
	return;

def PlotEnergyStats(data,axs):

	cold = filter(isCold,data)

	single = EnergyData() 
	double = EnergyData()
	triple = EnergyData()

	threading.start_new_thread(loadEnergyData,(single,cold,isSingle))
	threading.start_new_thread(loadEnergyData,(double,cold,isDouble))
	threading.start_new_thread(loadEnergyData,(triple,cold,isTriple))
	
	for thread in threading.enumerate():
		if thread is not threading.currentThread():
			thread.join()

	print single.stats
	print double.stats
	print triple.stats

data = LoadFile()
data = filter (isCold, filter (isDouble, data))
data = zip(*data)[2]
#print data



fig = plt.figure(num=1, facecolor='w', edgecolor='w', frameon=True)
axs = fig.add_subplot(111)
axs.plot(range(len(data)), data)
plt.show()


#PlotEnergyStats(data,axs)



#xlabel ('Cycle Type', fontsize=46)
#xticks ([0,1,2,3], ['Single', 'Double', 'Triple', 'Quadruple'], fontsize=32)

#ylabel (r'Energy / $\frac{kcal}{mol}$', fontsize=46)
#yticks (fontsize=32)
