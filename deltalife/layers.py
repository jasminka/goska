# -*- coding: utf-8 -*-
import os
import platform

import PyQt4.QtCore
import qgis.core as qc

ENCODING = u'windows-1250'
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
QGIS_DATA = os.path.join(PATH, "..", "..", "data", "obcine")
if 'QGIS_DATA' in os.environ:
    QGIS_DATA = os.environ['QGIS_DATA']
print "loading {}".format(os.path.join(QGIS_DATA, "Obcine.shp"))
VECTOR_LAYERS = {
    "OBCINE": os.path.join(QGIS_DATA, "Obcine.shp"),
}

QGIS_PREFIX = r"C:\Program Files (x86)\Quantum GIS Lisboa\apps\qgis"
if 'QGIS_PREFIX' in os.environ:
    QGIS_PREFIX = os.environ['QGIS_PREFIX']

if 'QGIS_PLUGINS' in os.environ:
    for f in os.listdir(os.environ['QGIS_PLUGINS']):
        PyQt4.QtCore.QLibrary(os.path.join(os.environ['QGIS_PLUGINS'], f)).load()

print 'QGIS_PREFIX:', QGIS_PREFIX
qc.QgsApplication.setPrefixPath(QGIS_PREFIX, True)
qc.QgsApplication.initQgis()


def get_geometry(feat):
    geom = feat.geometry()
    res = ''
    # show some information about the feature
    if geom.type() == qc.QGis.Point:
        x = geom.asPoint()
        res += "Point: %s\n" % str(x)
    elif geom.type() == qc.QGis.Line:
        x = geom.asPolyline()
        res += "Line: %d points\n" % len(x)
    elif geom.type() == qc.QGis.Polygon:
        x = geom.asPolygon()
        numPts = 0
        for ring in x:
            numPts += len(ring)
        res += "Polygon: %d rings with %d points\n" % (len(x), numPts)
    else:
        res += "Unknown\n"

    return res


def get_attributes(feat):
    # fetch map of attributes
    attrs = feat.attributeMap()

    # attrs is a dictionary: key = field index, value = QgsFeatureAttribute
    # show all attributes and their values
    vals = []

    for key, val in attrs.iteritems(): # zanka, ki gre čez ključe in vrednosti slovarja
        if val.type() == PyQt4.QtCore.QVariant.String:
            vals.append(unicode(val.toPyObject(), ENCODING))
        else:
            vals.append(val.toPyObject())

    return "Feature attributes: %s\n" % ", ".join(map(str, vals))


class DLife(object):
    def __init__(self):
        self.layers = {}
        self.provider = None

    def get_layer(self, layer_name):
        # Ustvari vektorski qg objekt "layer" in spatial index. Doda ju v slovar "layers"
        if not layer_name in self.layers:
            print 'Loading:', VECTOR_LAYERS[layer_name]
            layer = qc.QgsVectorLayer(VECTOR_LAYERS[layer_name], layer_name, "ogr")
            print 'Is valid:', layer.isValid()
            print layer.dataProvider().encoding()
            if platform.system() == 'Windows':
                layer.setProviderEncoding(ENCODING)
                layer.dataProvider().setEncoding(ENCODING)
            print layer.dataProvider().encoding()
            self.provider = layer.dataProvider()

            feat = qc.QgsFeature()
            index = qc.QgsSpatialIndex() # create a spatial index

            if hasattr(layer, 'getFeatures'):
                # QGis 2.+
                for feat in layer.getFeatures():
                    index.insertFeature(feat)
            else:
                all_attrs = self.provider.attributeIndexes()
                self.provider.select(all_attrs)
                while self.provider.nextFeature(feat):
                    index.insertFeature(feat)

            self.layers[layer_name] = (layer, index)

        return self.layers[layer_name]

    def nearest_feature(self, layer_name, x, y):
        # Funkcija vrne izbrani element (občino) na sloju.
        layer, index = self.get_layer(layer_name)
        inter = index.intersects(qc.QgsRectangle(x, y, x, y))
        for id in inter:
            feat = qc.QgsFeature()
            if hasattr(layer, 'featureAtId'):
                layer.featureAtId(id, feat, True, True)
                if feat.geometry().contains(qc.QgsPoint(x, y)):
                    return feat
            else:
                # QGis 2.+
                exist = layer.getFeatures(qc.QgsFeatureRequest().setFilterFid(id)).nextFeature(feat)
                if exist and feat.geometry().contains(qc.QgsPoint(x, y)):
                    return feat

        return None

    def get_attribute(self, feat, name):
        # Funkcija vrne vrednost iz tabele za podano obcino (feat) in atribut (name).
        ndx = self.provider.fieldNameIndex(name)

        if hasattr(feat, 'attributeMap'):
            val = feat.attributeMap()[ndx]
        else:
            # QGis 2.+
            val = feat.attributes()[ndx]

        if val.type() == PyQt4.QtCore.QVariant.String:
            return unicode(val.toPyObject(), ENCODING)
        else:
            return val.toPyObject()

    def get_attr_dict(self, feat):
        # Funkcija vrne slover atributov za obcine. Kljuc je ime stolpca.
        dict = self.provider.fieldNameMap()
        return dict

    def features(self, layer_name):
        feat = qc.QgsFeature()
        layer, index = self.get_layer(layer_name)

        if hasattr(layer, 'getFeatures'):
            # QGis 2.+
            for feat in layer.getFeatures():
                yield feat
        else:
            provider = layer.dataProvider()
            all_attrs = provider.attributeIndexes()
            provider.select(all_attrs)
            while provider.nextFeature(feat):
                yield feat

    def load_raster(self, fileName, x, y):
        fileName = "C:\Users\Jasmina\Dropbox\Documents\Faks\Diploma\kam\home\deltalife\data\dmnv_100\dmnv100\w001001.adf"
        fileInfo = PyQt4.QtCore.QFileInfo(fileName)
        baseName = fileInfo.baseName()
        rlayer = qc.QgsRasterLayer(fileName, baseName)
        if not rlayer.isValid():
            print "Layer failed to load!"
        res, ident = rlayer.identify(qc.QgsPoint(x, y))
        for (k, v) in ident.iteritems():
            str(k), ":", str(v)

            return str(v)

            #qc.QgsMapLayerRegistry.instance().addMapLayer(fileName)
            #qc.QgsMapLayerRegistry.instance().removeMapLayer(raster)
