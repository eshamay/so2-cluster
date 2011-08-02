from ColumnDataFile import ColumnDataFile as CDF
from ColumnDataFile import CDFGroup as CGroup
import glob, sys, operator
from scipy import integrate

files_cold = glob.glob('[1-5]/'+sys.argv[1]+'*')
files_hot = glob.glob('[6-9]/'+sys.argv[1]+'*')
files_hot = files_hot + glob.glob('10/'+sys.argv[1]+'*')

group = CGroup(files_cold)
xi,yi = group.Reduce1D(1)

#yi = yi - 1.0
index = operator.indexOf(xi, 2.7)

val = integrate.trapz(yi[:index], xi[:index], dx=0.05)
print val
