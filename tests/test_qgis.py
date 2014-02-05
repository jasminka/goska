from qgis.core import *

QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
QgsApplication.initQgis()

providers = QgsProviderRegistry.instance().providerList()
print "Providers:"
for provider in providers:
    print provider
print
print QgsApplication.showSettings()

#l = QgsVectorLayer('/Users/jasmina/Dropbox/Documents/Faks/Diploma/data/obcine/Obcine.shp', 'obcine', 'ogr')
l = QgsVectorLayer('/Users/miha/work/fun/goska/data/obcine/Obcine.shp', 'obcine', 'ogr')

print l.isValid()
