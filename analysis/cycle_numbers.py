from ColumnDataFile import ColumnDataFile as CDF
import numpy
import sys

cdf = CDF(sys.argv[1])
cdf = [numpy.array(cdf[c]) for c in cdf]
sums = [c.sum() for c in cdf]

print "Total = ", sums[0]
print "Single = ", sums[1]/sums[0]*100.
print "Double = ", sums[2]/sums[0]*100.
print "Type 1 triple = ", sums[3]/sums[0]*100.
print "Type 2 triple = ", sums[4]/sums[0]*100.
print "Other triple = ", sums[5]/sums[0]*100.
print "Total triple = ", (sums[3]+sums[4]+sums[5])/sums[0]*100.


