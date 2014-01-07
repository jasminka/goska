# -*- coding: utf-8 -*-
import random
import time
import numpy as np
import scipy as sp
from operator import itemgetter, attrgetter

import layers


life = layers.DLife()
layer_data = None
IMENA = {'GOSTOTA': u'GOSTOTA POSELITVE',
         'PRIRAST': u'SKUPNI PRIRAST',
         'PADA': u'POVPREČNA LETNA KOLIČINA PADAVIN',
         'REG_BREZPO': u'REGISTRIRANA BREZPOSELNOST',
         'URA_BRUTO': u'BRUTO PLAČILO ZA URA DELA',
         'STOP_BREZP': u'STOPNJA BREZPOSELNOSTI',
         'NAKLON': u'POVPREČEN NAKLON',
         'DEL_TUJC': u'DELEŽ TUJCEV',
         'TEMP': u'POVPREČNA LETNA TEMPERATURA',
         'AREA': u'POVRŠINA',
         'INDX_STAR': u'INDEKS STARANJA PREBIVALSTVA',
         'VISINA': u'POVPREČNA NADMORSKA VIŠINA',
         'RUGG': u'RAZGIBANOST_POVRŠJA',
         'PET1': u'POKRAJINSKOEKOLOŠKA TIPIZACIJA',
         'PODJ': u'POVPREČNI KAPITAL PODJETJA',
         'REKA2': u'VODNATOST',
         'INDX_DELOV': u'INDEKS DELOVNE MIGRACIJE',
         'INDX_STAR': u'INDEKS STARANJA',
}
# meje so izracunane na podlagi formule za iskanje statisticnih osamelcev (Q1 - 1.5*IQR, Q3 + 1.5*IQR), Q1 (1.kvartil), Q3 (tretji kvartil), IQR (intervartilna razlika) so bili izracunani v SPSS-u.
MEJE = {
    'GOSTOTA': [46.1 - 1.5 * 85.4, 131.5 + 1.5 * 85.4],
    'PRIRAST': [-6.3 - 1.5 * 12.5, 6.2 + 1.5 * 12.5],
    'PADA': [1145 - 1.5 * 452, 1597 + 1.5 * 452],
    'REG_BREZPO': [9.7 - 1.5 * 4.4, 14.1 + 1.5 * 4.4],
    'POV_VEL': [25.9 - 1.5 * 3, 28.9 + 1.5 * 3],
    'URA_BRUTO': [7.55 - 1.5 * 0.85, 8.4 + 1.5 * 0.85],
    'STOP_BREZP': [9.8 - 1.5 * 4.3, 14.1 + 1.5 * 4.3],
    'NAKLON': [5 - 1.5 * 8.3, 13.3 + 1.5 * 8.3],
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
        'template': u"Povprečna nadmorska višina v občini {o1} je {feature} kot v občini {o2}. ",
        'features': {
            (-1000, -30): u"precej nižja",
            (-45, -15): u"nekoliko nižja",
            (-10, 10): u"približno enaka",
            (10, 30): u"nekoliko višja",
            (30, 1000): u"precej višja",
        },
        'choices': {
            (-1000, -15): u"nižja",
            (-15, 15): u"približno enaka",
            (15, 1000): u"višja",
        },
        'group': u"naravne_značilnosti",
    }, {
        'attribute': 'NAKLON',
        'template': u"Občina {o1} ima {feature} povprečni naklon površja. ",
        'features': {
            (-1000, -30): u"precej manjši",
            (-30, -10): u"nekoliko manjši",
            (-10, 10): u"približno enak v obeh občinah ",
            (10, 30): u"nekoliko večji",
            (30, 1000): u"precej večji",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"približno enak",
            (15, 1000): u"večji"
        },
        'group':  u"naravne_značilnosti",
    },  {
        'attribute': 'PODN',
        'template': u"Občina {o1} ima {v1}, občina {o2} pa {v2}. ",
    },{
        'attribute': 'TEMP',
        'template': u"V občini {o1} je povprečna letna temperatura {feature} kot v občini {o2}. ",
        'features': {
            (-30, -1000): u"veliko nižja",
            (-10, -30): u"nekoliko nižja",
            (-10, 10): u"približno enaka",
            (10, 30): u"nekoliko višja",
            (30, 1000): u"veliko višja",
        },
        'choices': {
            (-1000, -15): u"nižja",
            (-15, 15): u"približno enaka",
            (15, 1000): u"višja"
        },
        'group': u"naravne_značilnosti",
    }, {
        'attribute': 'PADA',
        'template': u"Povprečno prejme {feature} količino padavin kot {o2}. ",
        'features': {
            (-30, -1000): u"precej manj",
            (-30, -10): u"nekoliko manjšo",
            (-10, 10): u"približno enako",
            (10, 30): u"nekoliko večjo",
            (30, 1000): u"precej večjo",
        },
        'choices': {
            (-1000, -15): u"manjšo",
            (-15, 15): u"skoraj enako",
            (15, 1000): u"večjo"
        },
        'group': u"naravne_značilnosti",
    },{
        'attribute': 'REKA2',
        'template': u"Občina {o1} je {feature}. "+ u'<br/>' + u'<br/>',
        'features': {
            (-1000, -30): u"precej manj vodnata",
            (-30, -10): u"nekoliko manj vodnata",
            (-10, 10): u"približno enako vodnata",
            (10, 30): u"nekoliko bolj vodnata",
            (30, 1000): u"precej bolj vodnata",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"naravne_značilnosti",
    },{
        'attribute': 'GOSTOTA',
        'template': u"Gostota prebivalstva je v občini {o1} {feature}. ",
        'features': {
            (-1000, -30): u"precej manjša",
            (-30, -10): u"nekoliko manjša",
            (-10, 10): u"približno enaka",
            (10, 30): u"nekoliko večja",
            (30, 1000): u"precej večja",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'PRIRAST',
        'template': u"Skupni prirastek prebivalstva je v občini {o1} {feature}. ",
        'features': {
            (-1000, -30): u"precej manjši",
            (-30, -10): u"nekoliko manjši",
            (-10, 10): u"približno enak",
            (10, 30): u"nekoliko večji",
            (30, 1000): u"precej večji",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'DEL_TUJC',
        'template': u"Delež tujcev je v občini {o1} {feature}. ",
        'features': {
            (-1000, -30): u"precej manjši",
            (-30, -10): u"nekoliko manjši",
            (-10, 10): u"približno enak",
            (10, 30): u"nekoliko večji",
            (30, 1000): u"precej večji",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'STOP_BREZP',
        'template': u"Stopnja brezposelnosti je v občini {o1} {feature}. ",
        'features': {
            (-1000, -30): u"precej manjša",
            (-30, -10): u"nekoliko manjša",
            (-10, 10): u"približno enaka",
            (10, 30): u"nekoliko večja",
            (30, 1000): u"precej večja",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'URA_BRUTO',
        'template': u"Bruto plačilo za uro dela je v občini {o1} {feature}. ",
        'features': {
            (-1000, -30): u"precej manjše",
            (-30, -10): u"nekoliko manjše",
            (-10, 10): u"približno enako",
            (10, 30): u"nekoliko večje",
            (30, 1000): u"precej večje",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'INDX_DELOV',
        'template': u"Indeks delovne migracije je v občini {o1} {feature}. ",
        'features': {
            (-1000, -30): u"precej manjši",
            (-30, -10): u"nekoliko manjši",
            (-10, 10): u"približno enak",
            (10, 30): u"nekoliko večji",
            (30, 1000): u"precej večji",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
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
                vals.append(float(val.toPyObject()))
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

def vrednost_atributa_vse_obcine_tup(atribut): #vrne seznam tuple-ov (id, vrednost) sortirane po vrednosti atributa
    s = []
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    for v in vrednosti:
        s.append(v[ime_atr.index(atribut)])
    return sorted(zip(id, s),key=itemgetter(1))

def vrednost_atributa_vse_obcine(atribut): #vrne sortiran seznam vrednosti atributa za vse obcine
    s = []
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    for v in vrednosti:
        s.append(v[ime_atr.index(atribut)])
    return sorted(s)

def id_ime(id): #vrne ime obcine za poljuben id
    idd, imena_obcin, ime_atr, vrednosti = get_layer_data()
    for iddd, ime in zip(idd, imena_obcin):
        if id == iddd:
            return ime
    return None

def katera_obcina(x, y):
    id = life.get_attribute(life.nearest_feature("OBCINE",x,y),"ID")
    ime = life.get_attribute(life.nearest_feature("OBCINE",x,y),"IME")
    return id, ime

def vrednost_atributa(id, atribut): # za zeljeno obcino in atribut izpise vrednost
    idd, imena_obcin, ime_atr, vrednosti = get_layer_data()
    ndx = idd.index(id) #ndx uvedemo, ker id-iji niso shranjeni po vrstnem redu
    for i, ime in enumerate(ime_atr):
        if ime == atribut:
            return vrednosti[ndx][i], ime_atr[i], imena_obcin[ndx]

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


def kako_narazen(atribut, id1, id2, smeja, zmeja):
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()
    ndx1 = id.index(id1)
    ndx2 = id.index(id2)
    for i, ime in enumerate(ime_atr):
        if ime == atribut:
            v1 = vrednosti[ndx1][i]
            v2 = vrednosti[ndx2][i]
            break
    obcina1 = imena_obcin[ndx1]
    obcina2 = imena_obcin[ndx2]
    ods = (abs(v1 - v2)) * 100 / abs(zmeja - smeja)
    if ods > 250:
      ods = 250
    #if ods >= 100:
        #ods = 100
    return  ods

def pretvori(ods):
    odg = None
    if ods < 0:
        odg = u"Nekaj ne bo vredu."
    elif ods == 0:
        odg = u"Ni razlike."
    elif ods > 0 and ods < 20:
        odg = u"Občini sta si precej podobni."
    elif ods >= 20 and ods < 40:
        odg = u"Občini sta nekoliko različni."
    elif ods >= 40:
        odg = u"Občini sta precej različni."
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

def normal_razl_meje(atr, id1, id2):
    v1, _, _ = vrednost_atributa(id1, atr)
    v2, _, _= vrednost_atributa(id2, atr)
    vse_vrednosti = vrednost_atributa_vse_obcine(atr)
    v_min =  min(vse_vrednosti)
    v_max = max(vse_vrednosti)
    if atr in MEJE:
         if MEJE[atr][0] > v_min:
            for vrednost in vse_vrednosti:
                if v_min >= MEJE[atr][0]:
                    v_min = vrednost #v_min je spodnja meja, smeja ze spada med vrednosti, ki jih upostevamo
                    break
            else:
                v_min = MEJE[atr][0]
         elif MEJE[atr][0] < v_max:
            for vrednost in vse_vrednosti[::-1]:
                if v_max <= MEJE[atr][1]:
                    v_max = vrednost #v_max je zgornja meja
                    break
            else:
                v_max = MEJE[atr][1]
    if v1 >= v_max:
        vi1 = 100
    elif v1 <= v_min:
        vi1 = 0
    else:
        vi1 = (v1 - v_min)/(v_max - v_min) * (100-0) + 0
    if v2 <= v_min:
        vi2 = 0
    elif v2 >= v_max:
        vi2 = 100
    else:
        vi2 = (v2 - v_min)/(v_max - v_min) * (100-0) + 0
    #print vi1, vi2
    return vi1, vi2, abs(vi1 - vi2)

def normal_razl(atr, id1, id2):
    v1, _, _ = vrednost_atributa(id1, atr)
    v2, _, _= vrednost_atributa(id2, atr)
    vse_vrednosti = vrednost_atributa_vse_obcine(atr)
    v_min =  min(vse_vrednosti)
    v_max = max(vse_vrednosti)
    vi1 = (v1 - v_min)/(v_max - v_min) * (100-0) + 0
    vi2 = (v2 - v_min)/(v_max - v_min) * (100-0) + 0
    #print vi1, vi2
    return vi1, vi2, abs(vi1 - vi2)

def skupna_razlika(id1, id2):
    dic_razl = {}
    dic = {
        u'družbene_značilnosti' : {'PRIRAST', 'DEL_TUJC', 'GOSTOTA', 'INDX_DELOV', 'URA_BRUTO', 'STOP_BREZP'},
        u'naravne_značilnosti': {'TEMP', 'PADA', 'NAKLON', 'VISINA', 'REKA2'},
    }
    m = 0
    max_spremenlj = ''
    for skupina, d in dic.iteritems():
        dic_razl[skupina] = {}
        for spremenlj in d:
            z = normal_razl_meje(spremenlj, id1, id2)[2]
            dic_razl[skupina][spremenlj] = z
            if z > m:
                m = z
                max_spremenlj = spremenlj
    dic_skup = {}
    vsota = 0
    for a, b in dic_razl.iteritems():
        print 'a', type(a)
        skupine = sum(c for c in b.itervalues())
        dic_skup[a] = skupine / len(b)
        print dic_skup
        vsota += dic_skup[a]

    return vsota / 2, dic_skup, dic_razl, max_spremenlj

def attr_mean(atr):
    mean = sum(vrednost_atributa_vse_obcine(atr))/ len(vrednost_atributa_vse_obcine(atr))
    vse_vrednosti = vrednost_atributa_vse_obcine(atr)
    v_min =  min(vse_vrednosti)
    v_max = max(vse_vrednosti)
    if atr in MEJE:
         if MEJE[atr][0] > v_min:
            for vrednost in vse_vrednosti:
                if v_min >= MEJE[atr][0]:
                    v_min = vrednost #v_min je spodnja meja, smeja ze spada med vrednosti, ki jih upostevamo
                    break
            else:
                v_min = MEJE[atr][0]
         elif MEJE[atr][0] < v_max:
            for vrednost in vse_vrednosti[::-1]:
                if v_max <= MEJE[atr][1]:
                    v_max = vrednost #v_max je zgornja meja
                    break
            else:
                v_max = MEJE[atr][1]
    if mean >= v_max:
        norm_mean = 100
    elif mean <= v_min:
        norm_mean = 0
    else:
        norm_mean = (mean - v_min)/(v_max - v_min) * (100-0) + 0

    return norm_mean

def opis(id1, id2):
    vsota, dic_skup, dic_razl, max_spremenlj = skupna_razlika(id1, id2)

    k2 = []
    for skl, val in dic_razl.iteritems():
        sklj = skl
        skl = skl.replace("_", " ").strip()
        skl = skl[0].upper() + skl[1:]
        items = []
        k2.append({
            'group': skl,
            'value': dic_skup[sklj],
            'attributes': items,
            'o1': 20,
            'o2': 40,
            'mean': 30,
        });
        for k, v in val.iteritems():
            items.append({
                'attribute': IMENA[k].lower(),
                'value': v,
                'o1': normal_razl_meje(k, id1, id2)[0],
                'o2': normal_razl_meje(k, id1, id2)[1],
                'mean': attr_mean(k),
            })
        items.sort(key=itemgetter('value'), reverse=True)
    k2.sort(key=itemgetter('value'), reverse=True)

    o1 = lepo_ime(id_ime(id1))
    o2 = lepo_ime(id_ime(id2))
    opis = u''
    for o in OPIS:
        if 'features' in o:
            attribute = o['attribute']
            template = o['template']
            features = o['features']
            group = o['group']
            #print group
            raz = dic_razl[group][attribute]
            v1 = vrednost_atributa(id1, attribute)
            v2 = vrednost_atributa(id2, attribute)
            if v2 > v1:
                raz = -raz
            for (fr, to), feature in features.iteritems():
                if fr < raz <= to:
                    break
            #print attribute, raz,'v', v1, v2
            opis += template.format(o1=o1, o2=o2, feature=feature, v1=v1[0]) \
                    #+ '[{}] '.format(raz)
    print 'maax', max_spremenlj

    skloni = {u"družbene značilnosti": u"družbenih značilnosti", u"naravne značilnosti": u"naravnih značilnosti" }
    if max(dic_skup.itervalues()) - min(dic_skup.itervalues()) > 10:
        vec_razl, _ = max(dic_skup.iteritems(), key=itemgetter(1))
        vec_razl = vec_razl.replace("_", " ",).strip()
        vec_razl = u"Največ razlik je na področju {}. ".format(skloni[vec_razl])
    else:
        vec_razl = u"Stopnja razlikovanja na naravnogeografskem in družbenogeografskem področju je približno enaka. "

    if max_spremenlj in IMENA:
        max_spremenlj = u"Najbolj se razlikujeta v spremenljivki {}. ".format(IMENA[max_spremenlj].lower())
    else:
        max_spremenlj = ""

    povzetek = u"{} {}".format(pretvori(vsota), vec_razl)
    return povzetek, opis, k2

def vse_razlike(limit=None):
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()

    if not limit:
        limit = len(id)

    return {(id[i], id[j]): skupna_razlika(id[i], id[j])[0] for i in range(len(id))[:limit] for j in range(i)}


