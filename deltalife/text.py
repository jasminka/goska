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
         'PRIRAST': u'SKUPNI PRIRAST PREB.',
         'PADA': u'KOLIČINA PADAVIN',
         'REG_BREZPO': u'BREZPOSELNOST',
         'URA_BRUTO': u'BRUTO PLAČILO ZA URO DELA',
         'STOP_BREZP': u'STOP. BREZPOSELNOSTI',
         'NAKLON': u'NAKLON POVRŠJA',
         'DEL_TUJC': u'DELEŽ TUJCEV',
         'TEMP': u'POVP. TEMPERATURA',
         'AREA': u'POVRŠINA',
         'INDX_STAR': u'INDEKS STARANJA',
         'VISINA': u'NADMORSKA VIŠINA',
         'RUGG': u'RAZGIBANOST_POVRŠJA',
         'PET1': u'POKRAJINSKOEKOLOŠKA TIPIZACIJA',
         'PODJ': u'POVPREČNI KAPITAL PODJETJA',
         'REKA2': u'GOSTOTA REČNE MREŽE',
         'INDX_DELOV': u'INDEKS DELOVNE MIGRACIJE',
         'PRST': u'PRST',
         'RABA': u'RABA TAL'

}

IMENA_LONG = {
         'GOSTOTA': u'GOSTOTA POSELITVE (preb/km2)',
         'PRIRAST': u'SKUPNI PRIRAST PREBIVALSTVA (na 1000 prebivalcev)',
         'PADA': u'POVPREČNA LETNA KOLIČINA PADAVIN (mm)',
         'REG_BREZPO': u'REGISTRIRANA BREZPOSELNOST',
         'URA_BRUTO': u'BRUTO PLAČILO ZA URO DELA (€)',
         'STOP_BREZP': u'STOPNJA BREZPOSELNOSTI (%)',
         'NAKLON': u'POVPREČNI NAKLON (°)',
         'DEL_TUJC': u'DELEŽ TUJCEV (%)',
         'TEMP': u'POVPREČNA LETNA TEMPERATURA (°C)',
         'AREA': u'POVRŠINA',
         'INDX_STAR': u'INDEKS STARANJA PREBIVALSTVA',
         'VISINA': u'POVPREČNA NADMORSKA VIŠINA (m)',
         'RUGG': u'RAZGIBANOST_POVRŠJA',
         'PET1': u'POKRAJINSKOEKOLOŠKA TIPIZACIJA',
         'PODJ': u'POVPREČNI KAPITAL PODJETJA',
         'REKA2': u'GOSTOTA REČNE MREŽE (km/km2)',
         'INDX_DELOV': u'INDEKS DELOVNE MIGRACIJE (del. aktivni po občini del. mesta/del. aktivni po občini prebivališča)*100',
         'PRST': u'PRST',
         'PRST_EVTR': u'EVTRIČNA',
         'PRST_DIST': u'DISTRIČNA',
         'PRST_POKAR': u'POKARBONATNA',
         'PRST_RENDZ': u'RENDZINA',
         'PRST_GLEJ': u'GLEJ, PSEVDOGLEJ',
         'PRST_OBREC': u'OBREČNA',
         'PRST_KAMN': u'KAMNIŠČE',
         'RABA': u'RABA TAL',
         'gozd': u'GOZD',
         'vodne': u'VODNE POVRŠINE',
         'umet': u'UMETNE POVRŠINE',
         'kmet': u'KMETIJSKE POVRŠINE',

}


SKLOPI = {
    'PODNEBJE': {
        'ime': 'Podnebje',
        'kazalniki': ['TEMP','PADA']

    },
    'IZO_POV': {
        'ime': 'Izoblikovanost površja',
        'kazalniki': ['VISINA', 'NAKLON', 'REKA2']
    },
    'DEMOG': {
        'ime': 'Demografska struktura',
        'kazalniki': ['GOSTOTA', 'INDX_STAR', 'PRIRAST', 'DEL_TUJC']
    },
    'SOCIO': {
        'ime': 'Socialna struktura',
        'kazalniki': ['URA_BRUTO', 'STOP_BREZP']
    },
    'PRST_RAST': {
        'ime': 'Prst in rastlinstvo',
        'kazalniki': ['PRST', 'RABA']
    },
    'MIGRACIJE': {
        'ime': 'Migracije',
        'kazalniki': ['INDX_DELOV']
    },
    'ZAPOS': {
        'ime': 'Zaposlitvena struktura',
        'kazalniki': ['STOP_BREZP', 'PODJ']
    },





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
    'REKA2': [0, 0],
}

OPIS = [
    {
        'attribute': 'GOSTOTA',
        'template': u"Občina {o1} je {feature} poseljena kot občina {o2}. ",
        'template2': u"Obe občini sta približno enako gosto poseljeni. ",
        'features': {
            (-1000, -10): u"redkeje",
            #(-30, -10): u"nekoliko redkeje",
            (-10, 10): u"približno enako gosto",
            #(10, 30): u"nekoliko gosteje",
            (10, 1000): u"bolj gosto",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },
    {
        'attribute': 'INDX_DELOV',
        'template': u"Razmerje med delovno aktivnimi prebivalci, ki delajo v občini ter tistimi, ki prebivajo v njej je {feature}. ",
        'template2': u"V obe občini se na delo vozi približno enak delež prebivalcev. ",
        'features': {
            (-1000, -10): u"manjše",
            #(-30, -10): u"nekoliko manjše",
            (-10, 10): u"približno enako",
            #(10, 30): u"nekoliko večje",
            (10, 1000): u"večje",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'URA_BRUTO',
        'template': u"Plače v občini {o1} so {feature} kot v občini {o2}, ",
        'template2': u"V obeh občinah so plače približno enako visoke, ",
        'features': {
            (-1000, -10): u"nižje",
            #(-30, -10): u"nekoliko nižje",
            (-10, 10): u"približno enako visoke",
            #(10, 30): u"nekoliko višje",
            (10, 1000): u"višje",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'STOP_BREZP',
        'template': u" {feature} je stopnja brezposelnosti. ",
        'template2': u"  {} stopnja brezposelnosti. ",
        'features': {
            (-1000, -10): u"nižja",
            #(-30, -10): u"nekoliko nižja",
            (-10, 10): u"približno enaka",
            #(10, 30): u"nekoliko višja",
            (10, 1000): u"višja",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'DEL_TUJC',
        'template': u"Občina {o1} je narodnostno {feature} mešana kot občina {o2}. ",
        'template2': u" Narodnostna mešanost je v obeh občinah približno enaka. ",
        'features': {
            (-1000, -10): u"manj",
            #(-30, -10): u"nekoliko manj",
            (-10, 10): u"približno enako",
            #(10, 30): u"nekoliko bolj",
            (10, 1000): u"bolj",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },{
        'attribute': 'PRIRAST',
        'template': u"Rast prebivalstva je v občini {o1} {feature}. <br/><br/>",
        'template2': u"Imata približno enako rast prebivalstva.  <br/><br/>",
        'features': {
            (-1000, -10): u"manjša",
            #(-30, -10): u"nekoliko manjša",
            (-10, 10): u"približno enaka",
            #(10, 30): u"nekoliko manjša",
            (10, 1000): u"večja",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"družbene_značilnosti",
    },
    {
        'attribute': 'VISINA',
        'template': u"Občina {o1} je {feature} ležeča kot občina {o2}  ",
        'template2': u"Občini ležita na približno enakih nadmorskih višinah.",
        'features': {
            (-1000, -10): u"nižje",
            #(-45, -15): u"nekoliko nižje",
            (-10, 10): u"približno enako visoko",
            #(10, 30): u"nekoliko višje",
            (10, 1000): u"višje",
        },
        'choices': {
            (-1000, -15): u"nižja",
            (-15, 15): u"približno enaka",
            (15, 1000): u"višja",
        },
        'group': u"naravne_značilnosti",
    }, {
        'attribute': 'NAKLON',
        'template': u" in ima {feature} strmo površje. ",
        'template2': u"Sta približno enaki strmi. ",
        'features': {
            (-1000, -10): u"manj",
            #(-30, -10): u"nekoliko manj",
            (-10, 10): u"približno enako",
            #(10, 30): u"nekoliko bolj",
            (10, 1000): u"bolj",
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
        'template': u"V občini {o1} je povprečna letna temperatura {feature}, ",
        'template2': u"Imata približno enako povprečno letno temperaturo ",
        'features': {
            (10, 1000): u"nižja",
            #(10, 30): u"nekoliko nižja",
            (-10, 10): u"približno enako visoka",
            #(-10, -30): u"nekoliko višja",
            (-10, -1000): u"višja",
        },
        'choices': {
            (-1000, -15): u"nižja",
            (-15, 15): u"približno enaka",
            (15, 1000): u"višja"
        },
        'group': u"naravne_značilnosti",
    },{
        'attribute': 'PADA',
        'template': u"povprečna količina padavin je {feature}. ",
        'template2': u"V količini padavin se ne razlikujeta. ",
        'features': {
            (-10, -1000): u"nižja",
            #(-30, -10): u"nekoliko nižja",
            (-10, 10): u"približno enaka",
            #(10, 30): u"nekoliko višja",
            (10, 1000): u"višja",
        },
        'choices': {
            (-1000, -15): u"manjšo",
            (-15, 15): u"skoraj enako",
            (15, 1000): u"večjo"
        },
        'group': u"naravne_značilnosti",
    },{
        'attribute': 'REKA2',
        'template': u" Rečna mreža je v občini {o1} {feature}. "+ u'<br/>' + u'<br/>',
        'template2': u"Gostota rečne mreže je v obeh občinah približno enaka. " u'<br/>' + u'<br/>',
        'features': {
            (-1000, -10): u"redkejša",
            #(-30, -10): u"nekoliko redkejša",
            (-10, 10): u"približno enako gosta",
            #(10, 30): u"nekoliko bolj gosta",
            (10, 1000): u"bolj gosta",
        },
        'choices': {
            (-1000, -15): u"manjši",
            (-15, 15): u"skoraj enak",
            (15, 1000): u"večji"
        },
        'group':  u"naravne_značilnosti",
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

OBCINE = {
    u'CERKLJE NA GORENJSKEM': u'Cerklje na Gorenjskem',
    u'ČRNA NA KOROŠKEM': u'Črna na Koroškem',
    u'DOBROVA - POLHOV GRADEC': u'Dobrova - Polhov Gradec',
    u'DOL PRI LJUBLJANI': u'Dol pri Ljubljani',
    u'GORENJA VAS - POLJANE': u'Gorenja vas - Poljane',
    u'GORNJI GRAD': u'Gornji Grad',
    u'GORNJI PETROVCI': u'Gornji Petrovci',
    u'IVANČNA GORICA': u'Ivančna Gorica',
    u'IZOLA/ISOLA': u'Izola/Isola',
    u'LOŠKI POTOK': u'Loški Potok',
    u'MORAVSKE TOPLICE': u'Moravske Toplice',
    u'MURSKA SOBOTA': u'Murska Sobota',
    u'NOVA GORICA': u'Nova Gorica',
    u'RAČE - FRAM': u'Rače - Fram',
    u'RADLJE OB DRAVI': u'Radlje ob Dravi',
    u'RAVNE NA KOROŠKEM': u'Ravne ne Koroškem',
    u'ROGAŠKA SLATINA': u'Rogaka Slatina',
    u'SLOVENJ GRADEC': u'Slovenj Gradec',
    u'SLOVENJSKA BISTRICA': u'Slovenska Bistrica',
    u'SLOVENJSKE KONJICE': u'Slovenjske Konjice',
    u'SVETI JURIJ': u'Sveti Jurij',
    u'ŠKOFJA LOKA': u'Škofja Loka',
    u'ŠMARJE PRI JELŠAH': u'Šmarje pri Jelšah',
    u'ŠMARTNO OB PAKI': u'Šmartno ob Paki',
    u'VELIKE LAŠČE': u'Velike Lašče',
    u'ZAGORJE OB SAVI': u'Zagorje ob Savi',
    u'HRPELJE - KOZINA': u'Hrpelje - Kozina',
    u'ILIRSKA BISTRICA': u'Ilirska Bistrica',
    u'KOPER/CAPODISTRIA': u'Koper/Capodistria',
    u'KRANJSKA GORA': u'Kranjska Gora',
    u'LENDAVA/LENDVA': u'Lendava/Lendva',
    u'MIREN - KOSTANJEVICA': u'Miren - Kostanjevica',
    u'NOVO MESTO': u'Novo Mesto',
    u'PIRAN/PIRANO': u'Piran/Pirano',
    u'BISTRICA OB SOTLI': u'Bistrica ob Sotli',
    u'DOBROVNIK/DOBRONAK': u'Dobrovnik/Dobronak',
    u'DOLENJSKE TOPLICE': u'Dolenkse Toplice',
    u'HOČE - SLIVNICA': u'Hoče - Slivnica',
    u'HODOŠ/HODOS': u'Hodoš/Hodos',
    u'LOVRENC NA POHORJU': u'Lovrenc na Pohorju',
    u'MIRNA PEČ': u'Mirna Peč',
    u'SELNICA OB DRAVI': u'Selnica ob Dravi',
    u'ŠEMPETER - VRTOJBA': u'Šempeter - Vrtojba',
    u'TRNOVSKA VAS': u'Trnovska Vas',
    u'MIKLAVŽ NA DRAVSKEM POLJU': u'Miklavž na Dravskem polju',
    u'RIBNICA NA POHORJU': u'Ribnica na Pohorju',
    u'SVETA ANA': u'Sveta Ana',
    u'SVETI ANDRAŽ V SLOV. GORICAH': u'Svet Andraž v Slov. goricah',
    u'VELIKA POLANA': u'Velika Polana',
    u'ŠMARTNO PRI LITIJI': u'Šmartno pri Litiji',
    u'SREDIŠČE OB DRAVI': u'Središče ob Dravi',
    u'SVETA TROJICA V SLOV. GORICAH': u'Sveta Trojica v Slov. goricah',
    u'SVETI TOMAŽ': u'Svet Tomaž',
    u'ŠMARJEŠKE TOPLICE': u'Šmarješke Toplice',
    u'KOSTANJEVICA NA KRKI': u'Kostanjevica na Krki',
    u'MOKRONOG - TREBELNO': u'Mokronog - Trebelno',
    u'RENČE - VOGRSKO': u'Renče - Vogrsko',
    u'LOG - DRAGOMER': u'Log - Dragomer',
    u'REČICA OB SAVINJI': u'Rečica ob Savinji',
    u'SVETI JURIJ V SLOV. GORICAH': u'Sveti Jurij v Slov. goricah',
}

MULTI = {
    u"PRST" : [
        u'PRST_EVTR',
        u'PRST_DIST',
        u'PRST_POKAR',
        u'PRST_RENDZ',
        u'PRST_GLEJ',
        u'PRST_OBREC',
        u'PRST_KAMN',
    ],
    u'RABA' : [
        u'gozd',
        u'kmet',
        u'vodne',
        u'umet',
    ],
}

DELITEV = {
    u'družbene_značilnosti' : ('PRIRAST', 'DEL_TUJC', 'GOSTOTA', 'INDX_DELOV', 'URA_BRUTO', 'STOP_BREZP'),
    u'naravne_značilnosti': ('TEMP', 'PADA', 'NAKLON', 'VISINA', 'REKA2', 'PRST', 'RABA'),
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
        if hasattr(feat, 'attributeMap'):
            attr_vals = feat.attributeMap() # key = field index, value = QgsFeatureAttribute
        else:
            # QGis 2.+
            attr_vals = feat.attributes()

        attr_names = dict((val, key) for key, val in life.get_attr_dict(feat).iteritems())
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
                    vals.append(unicode(val.toPyObject(), layers.ENCODING))

        imena_obcin.append(unicode(attr_vals[1].toPyObject(), layers.ENCODING))
        id.append(int(unicode(attr_vals[0].toPyObject(), layers.ENCODING)))
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
    for iddd, name in zip(idd, imena_obcin):
        if id == iddd:
            return name
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
            return vrednosti[ndx][i], ime_atr[i], idd[ndx]
print vrednost_atributa(12, 'REKA2')

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
    elif ods > 0 and ods < 15:
        odg = u"Občini sta podobni."
    elif ods >= 15 and ods < 35:
        odg = u"Občini sta različni."
    #elif ods >= 35:

    return odg

def get_obcine():
    obcine = []
    ids, obcine, _, _ = get_layer_data(layer_name='OBCINE')
    return [{"id": a, "ime": b} for a, b in zip(ids, obcine)]

def lepo_ime(o):
    if o in OBCINE:
        return OBCINE[o]

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
print normal_razl('REKA2', 065, 061)

def skupna_razlika(id1, id2, meje=True):
    dic_razl = {}
    dic = DELITEV
    m = 0
    max_spremenlj = ''
    for skupina, d in dic.iteritems():
        dic_razl[skupina] = {}
        for spremenlj in d:
            if spremenlj != 'PRST' and meje is True:
                z = normal_razl_meje(spremenlj, id1, id2)[2]
            elif spremenlj != 'PRST'and meje is not True:
                z = normal_razl(spremenlj, id1, id2)[2]
            else:
                break
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

def attr_mean_brez(atr):
    mean = sum(vrednost_atributa_vse_obcine(atr))/ len(vrednost_atributa_vse_obcine(atr))
    vse_vrednosti = vrednost_atributa_vse_obcine(atr)
    v_min =  min(vse_vrednosti)
    v_max = max(vse_vrednosti)
    norm_mean = (mean - v_min)/(v_max - v_min) * (100-0) + 0

    return norm_mean

def multi_bar(id1, id2, dict):
    type = {}

    count1 = 0
    count2 = 0

    for a in dict:
        ids = {}
        print a
        val1, atr_name1, mun1 = vrednost_atributa(id1, a)
        val2, atr_name2, mun2 = vrednost_atributa(id2, a)
        ids[mun1] = val1
        print "val", val1
        count1 += val1 if val1 else 0
        count2 += val2 if val2 else 0
        ids[mun2] = val2
        a = IMENA_LONG[a]
        type[a] = ids
    if count1 < 100:
        ostalo = {id1: 100 - count1}
    else:
        ostalo = {id1: 0}
    type['OSTALO'] = ostalo
    if count2 < 100:
        ostalo[id2] = 100 - count2
    else:
        ostalo[id2] = 0

    print 'type', type
    return type

def opis(id1, id2, meje=True):
    if meje is True:
        vsota, dic_skup, dic_razl, max_spremenlj = skupna_razlika(id1, id2)
    else:
        vsota, dic_skup, dic_razl, max_spremenlj = skupna_razlika(id1, id2, meje=False)

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
        })

        if meje is True:
            for k, v in val.iteritems():
                minval, maxval = min_max_obcini(k)
                items.append({
                    'id': k,
                    'attribute': IMENA[k].lower(),
                    'attribute_long':IMENA_LONG[k].lower(),
                    'value': v,
                    'o1': normal_razl_meje(k, id1, id2)[0],
                    'o1_real': vrednost_atributa(id1, k)[0],
                    'o1_name': id_ime(id1),
                    'o2': normal_razl_meje(k, id1, id2)[1],
                    'o2_real': vrednost_atributa(id2, k)[0],
                    'o2_name': id_ime(id2),
                    'mean': attr_mean(k),
                    'min': minval,
                    'max': maxval,
                })
        else:
            for k, v in val.iteritems():
                vals = vrednost_atributa_vse_obcine_tup(k)
                items.append({
                    'id': k,
                    'attribute': IMENA[k].lower(),
                    'attribute_long':IMENA_LONG[k].lower(),
                    'value': v,
                    'o1': normal_razl(k, id1, id2)[0],
                    'o1_real': vrednost_atributa(id1, k)[0],
                    'o1_name': id_ime(id1),
                    'o2': normal_razl(k, id1, id2)[1],
                    'o2_real': vrednost_atributa(id2, k)[0],
                    'o2_name': id_ime(id2),
                    'mean': sum(zip(*vals)[1]) / len(vals),
                    'min': min(vals, key=itemgetter(1))[1],
                    'min_name': id_ime(min(vals, key=itemgetter(1))[0]),
                    'max': max(vals, key=itemgetter(1))[1],
                    'max_name': id_ime(max(vals, key=itemgetter(1))[0])
                })

        for s, v in MULTI.items():
            if s in DELITEV[sklj]:
                items.append({
                    'id': s,
                    'attribute': IMENA[s].lower(),
                    'attribute_long':IMENA_LONG[s].lower(),
                    'multi': multi_bar(id1, id2, v),
                    'o1': id1,
                    'o1_name': id_ime(id1),
                    'o2': id2,
                    'o2_name': id_ime(id2),
                    'value': -1
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
            template2 = o['template2']
            raz = dic_razl[group][attribute]
            v1 = vrednost_atributa(id1, attribute)
            v2 = vrednost_atributa(id2, attribute)
            if v2 > v1:
                raz = -raz
            for (fr, to), feature in features.iteritems():
                #if -10 < raz <= 10:
                    #opis += template2
                    #break
                if attribute == 'INDX_DELOV':
                    if v1[0] <= 100 and v2[0] <= 100:
                        template = u'Iz obeh občin se več ljudi, kot imata delovno aktivnih prebivalcev, vozi na delo drugam. '
                    if v1[0] >= 100 and v2[0] >= 100:
                        template = u'V obe občini se na delo vozi več ljudi, kot imata delovno aktivnih prebivalcev. '
                    if v1[0] > 100 and v2[0] < 100:
                        template = u'V občino {o1} se na delo vozi več ljudi, kot ima delovno aktivnih prebivalcev, v občini {o2} pa je ravno obratno. '
                    if v1[0] < 100 and v2[0] > 100:
                        template = u'Iz občine {o2} se več ljudi vozi na delo drugam, kot ima delovno aktivnih prebivalcev.'

                if fr < raz <= to:
                    opis += template.format(o1=o1, o2=o2, feature=feature, v1=v1[0])
                    break
                    #+ '[{0}] '.format(raz)
    print 'maax', max_spremenlj

    skloni = {u"družbene značilnosti": u"družbenogeografskih značilnosti", u"naravne značilnosti": u"naravnogeografskih značilnosti" }
    if max(dic_skup.itervalues()) - min(dic_skup.itervalues()) > 10:
        vec_razl, _ = max(dic_skup.iteritems(), key=itemgetter(1))
        vec_razl = vec_razl.replace("_", " ",).strip()
        vec_razl = u"Največ razlik je na področju {0}. ".format(skloni[vec_razl])
    else:
        vec_razl = u" "

    if max_spremenlj in IMENA:
        max_spremenlj = u"Občini se najbolj razlikujeta v spremenljivki {0}.".format(IMENA_LONG[max_spremenlj].lower().split(" (")[0])
    else:
        max_spremenlj = ""



    povzetek = u"{0} {1}".format( vec_razl, max_spremenlj)
    print 'k', k2
    return povzetek, opis, k2 # k2 je seznam slovarjev

def vse_razlike(limit=None):
    id, imena_obcin, ime_atr, vrednosti = get_layer_data()

    if not limit:
        limit = len(id)

    return dict(((id[i], id[j]), skupna_razlika(id[i], id[j])[0]) for i in range(len(id))[:limit] for j in range(i))


def min_max_obcini(atr):
    t = vrednost_atributa_vse_obcine_tup(atr)
    minimum = t[0][1]
    maximum = t[0][1]
    for id, v in t:
        if v >= MEJE[atr][0] and v < minimum:
            minimum = v
    for id, v in t:
        if v <= MEJE[atr][1] and v > maximum:
            maximum = v
    return minimum, maximum
