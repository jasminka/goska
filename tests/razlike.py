import operator

from matplotlib import pyplot as plt
import deltalife


print "Racunam razlike"

di = deltalife.vse_razlike()

di_list = [(i, j, d) for (i, j), d in di.iteritems()]
di_list.sort(key=operator.itemgetter(2), reverse=True)

for i, j, d in di_list[:20]:
    print u"{:>6} {:>3} {:>3} {:<20} {:<20}".format(d, i, j, deltalife.id_ime(i), deltalife.id_ime(j))
print "\n...\n"
for i, j, d in di_list[-20:]:
    print u"{:.3f} {:>3} {:>3} {:<20} {:<20}".format(d, i, j, deltalife.id_ime(i), deltalife.id_ime(j))
print
print "max", max(di.values())
print "min", min(di.values())

plt.hist(di.values(), bins=50)
plt.savefig("razlike.pdf")


#print "Pisem v datoteko"
#with open("razlike.txt", "w") as f:
#    f.write("{}".format(di))

#print deltalife.normal_razl_meje('GOSTOTA', 6, 12)