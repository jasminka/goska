# -*- coding: utf-8 -*-
from operator import itemgetter, attrgetter
import numpy as np
import scipy as sp
from scipy import stats
import PyQt4
import random
import layers


life = layers.DLife()
layer_data = None

# meje so izracunane na podlagi formule za iskanje statisticnih osamelcev (Q1 - 1.5*IQR, Q3 + 1.5*IQR), Q1 (1.kvartil), Q3 (tretji kvartil), IQR (intervartilna razlika) so bili izracunani v SPSS-u.
MEJE = {
    'GOSTOTA': [46.1 - 1.5 * 85.4, 131.5 + 1.5 * 85.4],
    'PRIRAST': [-6.3 - 1.5 * 12.5, 6.2 + 1.5 * 12.5],
    'PADA': [1145 - 1.5 * 452, 1597 + 1.5 * 452],
    'REG_BREZPO': [9.7 - 1.5 * 4.4, 14.1 + 1.5 * 4.4],
    'POV_VEL': [25.9 - 1.5 * 3, 28.9 + 1.5 * 3],
    'URA_BRUTO': [7.55 - 1.5 * 0.85, 8.4 + 1.5 * 0.85],
    'STOP_BREZP': [9.8 - 1.5 * 4.3, 14.1 + 1.5 * 4.3],
    'NAKLON1': [5 - 1.5 * 8.3, 13.3 + 1.5 * 8.3],
    'DEL_TUJC': [1 - 1.5 * 2.7, 3.7 + 1.5 * 2.7],
    'TEMP': [8.2 - 1.5 * 1.5, 9.7 + 1.5 * 1.5],
    'AREA': [36.3 - 1.5 * 81.2, 117.5 + 1.5 * 81.2],
    'INDX_STAR': [100.7 - 1.5 * 33.2, 133.9 + 1.5 * 33.2],
    'POV_STAR': [41 - 1.5 * 2.2, 43.2 + 1.5 * 2.2],
    'ST_PREB': [2874 - 1.5 * 7404, 10278 + 1.5 * 7404],
    'INDX_DELOV': [41 - 1.5 * 39.6, 80.6 + 1.5 * 39.6],
    'VISINA': [268 - 1.5 * 356, 624 + 1.5 * 356],
    'RUGG': [27.6 - 1.5 * 39.3, 66.9 + 1.5 * 39.3],
    'PET1': [2 - 1.5 * 2, 4 + 1.5 * 2],
    'PODJ': [9 - 1.5 * 17, 26 + 1.5 * 17],
    'REKA2': [14.1 - 1.5 * 9.9, 24.0 + 1.5 * 9.9],
}

OPIS = [
    {
        'attribute': 'VISINA',
        'template': u"Povprečna nadmorska višina v občini {o1} je {v1} metrov in je {feature} kot v občini {o2}. ",
        'features': {
            ( -45, -100): u"precej nižja",
            (-45, -15): u"nekoliko nižja",
            (-15, 15): u"približno enaka",
            (15, 45): u"nekoliko višja",
            (45, 100): u"precej višja",
        },
        'choices': {
            (-1000, 15): u"nižja",
            (-15, 15): u"približno enaka",
            (15, 1000): u"višja",
        },
    }, {
        'attribute': 'NAKLON1',
        'template': u"Povprečni naklon površja je {feature}. ",
        'features': {
            ( -45, -100): u"precej manjši",
            (-45, -15): u"nekoliko manjši",
            (-15, 15): u"približno enak",
            (15, 45): u"nekoliko večji",
            (45, 100): u"precej večji",
        },
        'choices': {
            (-1000, 15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        }
    }, {
        'attribute': 'TEMP',
        'template': u"Letna povprečna temperatura v občini {o1} je {feature}. ",
        'features': {
            ( -45, -100): u"precej nižja",
            (-45, -15): u"nekoliko nižja",
            (-15, 15): u"približno enaka",
            (15, 45): u"nekoliko višja",
            (45, 100): u"precej višja",
        },
        'choices': {
            (-1000, 15): u"nižja",
            (-15, 15): u"skoraj enaka",
            (15, 1000): u"višja"
        }
    }, {
        'attribute': 'PADA',
        'template': u"Količina padavin v letnem povprečju je {feature}. ",
        'features': {
            ( -45, -100): u"precej manjša",
            (-45, -15): u"nekoliko manjša",
            (-15, 15): u"približno enaka",
            (15, 45): u"nekoliko večja",
            (45, 100): u"precej večja",
        },
        'choices': {
            (-1000, 15): u"manjša",
            (-15, 15): u"skoraj enaka",
            (15, 1000): u"večja"
        }
    }, {
        'attribute': 'PODN',
        'template': u"Podnebje v {o1} je {v1}. Kakšno je v občini {o2}? ",
    },
    {
        'attribute': 'PRIRAST',
        'template': u"Skupni prirastek prebivalstva je v občini {o1} {feature}. ",
        'features': {
            ( -45, -100): u"precej manjši",
            (-45, -15): u"nekoliko manjši",
            (-15, 15): u"približno enak",
            (15, 45): u"nekoliko večji",
            (45, 100): u"precej večji",
        },
        'choices': {
            (-1000, 15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        }
    },
]

PET = {
    1: u'je visokogorje',
    2: u'so širše rečne doline v visokogorju, hribovju in krasu',
    3: u'so visoke kraške planote in hribovja v karbonatnih kamninah',
    4: u'so hribovja v pretežno nekarbonatnih kamninah',
    5: u'so medgorske kotline',
    6: u'je gričevje v nekarbonatnem delu Slovenije',
    7: u'so ravnine in širše doline v gričevju notranjega dela Slovenije',
    8: u'so kraška polja in podolja',
    9: u'je nizki kras Notranjske in Dolenjske',
    10: u'je nizki kras bele krajine',
    11: u'je kras in podgorski kras',
    12: u'je gričevje v primorskem delu Slovenije',
    13: u'so širše doline in obalne ravnice v primorskem delu Slovenije',
}
PODN = {
    33: u'zmerno celinsko podnebje vzhodne Slovenije (subpanonsko)',
    32: u'zmerno celinsko podnebje osrednje Slovenije',
    31: u'zmerno celinsko podnebje zahodne in južne Slovenije (predgorsko)',
    22: u'gorsko podnebje nižjega gorskega sveta',
    21: u'gorsko podnebje višjega gorskega sveta',
    12: u'zaledno submediteransko podnebje',
    11: u'obalno submediteransko podnebje',
}

def get_layer_data(layer_name='OBCINE'):
    """Seznam vseh atributov za vse obcine."""
    global layer_data
    if layer_data:
        return layer_data

    vrednosti = []
    imena_obcin = []
    id = []
    imena_atributov = []
    for feat in life.features(layer_name): # Gre cez vse featurje (obcine) na sloju
        attr_vals = feat.attributeMap() # key = field index, value = QgsFeatureAttribute
        attr_names = {val: key for key, val in life.get_attr_dict(feat).iteritems()}
        vals = []
        columns = sorted(attr_names.iterkeys())[2:]

        for key in columns:
            val = attr_vals[key] # za vsako obcino izpise vrednosti za vse atribute

            try:
                vals.append(int(val.toPyObject()))
            except:
                try:
                    vals.append(float(val.toPyObject()))
                except:
                    vals.append(unicode(val.toPyObject(), 'windows-1250'))

        imena_obcin.append(unicode(attr_vals[1].toPyObject(), 'windows-1250'))
        id.append(int(unicode(attr_vals[0].toPyObject(), 'windows-1250')))
        vrednosti.append(vals)

    for col in columns:
        imena_atributov.append(str(unicode(attr_names[col])))

    layer_data = (id, imena_obcin, imena_atributov, vrednosti)
    return layer_data


def katera_obcina(x1, y1):
    feat = life.nearest_feature("OBCINE", x1, y1)
    if not feat:
        return -1, ''
    return int(life.get_attribute(feat, "ID")), life.get_attribute(feat, "IME")


def vrednost_atributa_obe_tocki(ime_atributa, x1, y1, x2, y2): #vrne id in vrednosti zeljenega atributa
    obcina1 = []
    obcina2 = []
    feat = life.nearest_feature("OBCINE", x1, y1)
    obcina1.append(int(life.get_attribute(feat, "ID")))
    obcina1.append(str(life.get_attribute(feat, "IME")))
    obcina1.append(float(life.get_attribute(feat, ime_atributa)))
    feat = life.nearest_feature("OBCINE", x2, y2)
    obcina2.append(int(life.get_attribute(feat, "ID")))
    obcina2.append(str(life.get_attribute(feat, "IME")))
    obcina2.append(float(life.get_attribute(feat, ime_atributa)))
    return obcina1, obcina2


def vrednost_atributa_vse_obcine_tup(atribut): #vrne tuple (id, vrednost) sortirane po vrednosti atributa
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    return sorted(zip(id, vrednosti[ime_atr.index(atribut)]), key=itemgetter(1))


def vrednost_atributa_vse_obcine(atribut):
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    return vrednosti[:, ime_atr.index(atribut)]


def id_ime(id): #vrne ime obcine za poljuben id
    idd, imena_obcin, ime_atr, vrednosti = get_layer_data()
    for iddd, ime in zip(idd, imena_obcin):
        if id == iddd:
            a = ime
    return a


def vrednost_atributa(id, atribut): # za zeljeno obcino in atribut izpise vrednost
    idd, imena_obcin, ime_atr, vrednosti = get_layer_data()
    ndx = idd.index(id) #ndx uvedemo, ker id-iji niso shranjeni po vrstnem redu
    for i, ime in enumerate(ime_atr):
        if ime == atribut:
            return vrednosti[ndx][i], ime_atr[i], imena_obcin[ndx]


def std(atribut):
    sez = []
    for tup in vrednost_atributa_vse_obcine_tup(atribut):
        sez.append(tup[1])
    return np.std(sez)


def kako_narazen_delez(atribut, id1,
                       id2): #vrne delez obcin, katerih vrednosti za poljuben atribut lezijo med izbranima obcinama
    sortiran = sorted(vrednost_atributa_vse_obcine_tup(atribut),
                      key=itemgetter(1)) #Dobimo seznam tuplov (id, vrednost atributa)
    i = 0
    for id, vrednost in sortiran:
        if id == id1:
            ord1 = i #vrstni red vrednosti atributa izmed vseh obcin
            vr1 = vrednost #vrednost atributa
            l1 = [id1, vr1]
        elif id == id2:
            ord2 = i #vrstni red druge obcine
            vr2 = vrednost #vrednost atributa
            l2 = [id2, vr2]
        i += 1
    razlika = (float((abs(ord1 - ord2)) - 1) / float(len(sortiran) + 1)) * 100 #koliko % obcin je vmes
    return l1, l2, razlika, ord1 - 1, ord2 - 1


def kako_narazen_std(atribut, id1, id2): #vrne kvocient razlike med vrednostima in std
    return abs(vrednost_atributa(id1, atribut)[0] - vrednost_atributa(id2, atribut)[0]) / std(atribut)


def kako_narazen_z_scores(atribut, id1, id2): #vrne razliko med dvema z-vrednostima
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    sez = (zip(id, vrednosti[:, ime_atr.index(atribut)]))
    seznam = []
    for i, e in enumerate(sez):
        seznam.append(e[1])

    sez_z = sp.stats.zscore(seznam)
    z1 = sez_z[id1 - 1]
    z2 = sez_z[id2 - 1]
    if z1 < 0 or z2 < 0:
        a = abs(z1) + abs(z2)
    else:
        a = abs(z1 - z2)

    return z1, z2, a


def kako_narazen(atribut, id1, id2, smeja, zmeja):
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    print 'zmeja', smeja, 'smeja', zmeja, type(smeja), type(zmeja)
    ndx1 = id.index(id1)
    ndx2 = id.index(id2)
    for i, ime in enumerate(ime_atr):
        if ime == atribut:
            v1 = vrednosti[ndx1][i]
            v2 = vrednosti[ndx2][i]
            break
    print 'vrednosti', v1, v2, type(v1), type(v2)
    obcina1 = imena_obcin[ndx1]
    obcina2 = imena_obcin[ndx2]

    ods = (abs(v1 - v2)) * 100 / abs(zmeja - smeja)
    print ods
    #if ods >= 100:
        #ods = 100

    return ods


def pretvori(ods):
    odg = None
    if ods < 0:
        odg = "Nekaj ne bo vredu."
    elif ods == 0:
        odg = "Ni razlike."
    elif ods > 0 and ods < 35:
        odg = "Občini sta si precej podobni."
    elif ods >= 35 and ods < 65:
        odg = "Razlike so!"
    elif ods >= 65:
        odg = "Občini sta precej različni."


    return odg


def get_obcine():
    obcine = []
    ids, obcine, _, _ = get_layer_data(layer_name='OBCINE')

    return [{"id": a, "ime": b} for a, b in zip(ids, obcine)]


def lepo_ime(o):
    o = o[0].upper() + o[1:].lower()
    if '/' in o:
        o = o[:o.find('/')]
    return o


def razlike(id1, id2):
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()

    dictx, atributi = {}, {}
    for ime in ime_atr:
        print ime_atr.index(ime)
        dictx[ime] = vrednosti[ime_atr.index(ime)]  # slovar vrenosti atributov
        atributi[ime] = vrednost_atributa_vse_obcine_tup(ime)  #atributi vsebuje imena atributov in tuple (id, vrednost)

    #ustvarimo slovar atributi_meje, vsebuje mejne vrednosti atributov. Meje so znotraj intervala, ki ga obravnavamo
    atributi_meje = {}
    for ime_atributa, vrednosti in atributi.iteritems():
        if ime_atributa in MEJE:
            for vrednost in vrednosti:
                if vrednost[1] >= MEJE[ime_atributa][0]:
                    smeja = vrednost[1] #smeja je spodnja meja, smeja ze spada med vrednosti, ki jih upostevamo
                    break
                else:
                    smeja = MEJE[ime_atributa][0]
            for vrednost in vrednosti[::-1]:

                if vrednost[1] <= MEJE[ime_atributa][1]:
                    zmeja = vrednost[1] #zmeja je zgornja meja
                    break
                else:
                    zmeja = MEJE[ime_atributa][1]
            atributi_meje[ime_atributa] = [smeja, zmeja]

    print atributi_meje

    #dic vsebuje atribute, ki so bili uporabljeni v modelu po vsebinskih sklopih
    dic = {
        'prebivalstvo': ('PRIRAST', 'DEL_TUJC', 'GOSTOTA', 'INDX_STAR', 'INDX_DELOV', 'URA_BRUTO', 'STOP_BREZP', ),
        'razvitost': (),
        'kakovost_okolja': (),
        'naravne_znacilnosti': ('TEMP', 'PADA', 'NAKLON1', 'VISINA', 'REKA2'),
    }

    #d vsebuje imena vsebinskih sklopov in pripadajoco povprecno razliko v odstotkih
    razlika_sklopi = {}
    razlika_atributi = {}
    vsota = 0
    for sklop, kazalniki in dic.iteritems():
        s = []
        if dic[sklop]:
            for kazalnik in kazalniki:
                razlika_sklopi[sklop] = s
                smeja = atributi_meje[kazalnik][0]
                zmeja = atributi_meje[kazalnik][1]
                odpakiraj = kako_narazen(kazalnik, id1, id2, smeja, zmeja)
                razlika_atributi[kazalnik] = odpakiraj
                s.append(odpakiraj)
                print s
                print 'kaz', kazalnik, 'kako', kako_narazen(kazalnik, id1, id2, smeja, zmeja)

            razlika_sklopi[sklop] = np.mean(s)
            vsota += razlika_sklopi[sklop]
    print razlika_sklopi
    print len(razlika_sklopi)
    print vsota
    print vsota/len(razlika_sklopi)
    kazalniki = "<table>\n        <tr><th style=\"width: 150px;\"></th><th style=\"width: 80px; text-align: right;\">%</th></tr>\n"
    for skl, val  in razlika_sklopi.iteritems():
        vall =  dic[skl]
        skl = skl.replace("_", " ").strip()
        skl = skl[0].upper() + skl[1:]
        kazalniki += "        <tr><td>{}</td><td style=\"text-align: right;\">{:.2f}</td></tr>\n".format(skl, val)
        for v in vall:
            sub_skl = v.replace("_", " ").strip()
            sub_skl = sub_skl[0] + sub_skl[1:].lower()
            kazalniki += "<tr style=\"font-size: 0.9em;\"><td>&nbsp;&nbsp;{}</td><td style=\"text-align: right;\">{:.2f}</td></tr>\n".format(sub_skl, razlika_atributi[v])
    kazalniki += "</table>\n"





    o1 = lepo_ime(id_ime(id1))
    o2 = lepo_ime(id_ime(id2))
    f1 = feature1=PET[vrednost_atributa(id1, "PET")[0]]
    f2 = feature2=PET[vrednost_atributa(id2, "PET")[0]]
    if f1 != f2:
        opis = u"Najbolj pogost pokrajinski tip v občini {o1} {feature1}, v občini {o2} pa {feature2}. Jih znaš poimenovati? ".format(
        o1=o1, o2=o2, feature1=feature1, feature2=feature2)
    else:
        opis = u"Najbolj pogost tip površja v obeh občinah {feature1}. Poznaš poimensko? ".format(
        feature1=feature1)

    #print vrednost_atributa(id1, "PODN")[0]
    #f1 = feature1=PODN[vrednost_atributa(id1, "PODN")[0]]
    #f2 = feature2=PODN[vrednost_atributa(id2, "PODN")[0]]
    #
    #if f1 != f2:
    #    opis = u"Najbolj pogost pokrajinski tip v občini {o1} {feature1}, v občini {o2} pa {feature2}. ".format(
    #    o1=o1, o2=o2, feature1=feature1, feature2=feature2)
    #else:
    #    opis = u"V obeh občinah {feature1} najbolj pogost tip površja. ".format(
    #    feature1=feature1)

    for o in OPIS:
        if 'features' in o:
            attribute = o['attribute']
            template = o['template']
            features = o['features']
            choices = o['choices']
            raz = razlika_atributi[attribute]

            v1 = vrednost_atributa(id1, attribute)
            v2 = vrednost_atributa(id2, attribute)
            if v2 > v1:
                raz = -raz

            if random.random() > .5:
                for (fr, to), feature in features.iteritems():
                    if fr < raz <= to:
                        break
                    else:
                        print "Nekaj je zelo narobe. Vrednost za {} ne ustreza nobenemu intervalu.".format(attribute)
            else:
                feature = u'<select><option></option>'
                for (fr, to), choice in choices.iteritems():
                    feature += u'<option>{}</option>'.format(choice)
                feature += u'</select>'
            opis += template.format(o1=o1, o2=o2, feature=feature, v1=v1[0]) + '[{}] '.format(raz)
        else:
            attribute = o['attribute']
            template = o['template']
            v1 = vrednost_atributa(id1, attribute)
            v2 = vrednost_atributa(id2, attribute)
            opis += template.format(o1=o1, o2=o2, v1=v1[0])

    return pretvori(vsota / len(razlika_sklopi)), opis, kazalniki
