import pandas as pd
import random
import csv
from datetime import datetime

HEADER = ['datum', 'domacin', 'gost', 'rezultat', 'brOsSetDomacin', 'brOsSetGost',
          'osBodDomacin', 'osBodGost', 'proRazBodUSet',
          'pobjednik', 'pobjednikDomacinIliGost',
          'omjProPobj',
          'proPobjDomacinNadGost',
          'brDaOdZadDomacin',
          'brDaOdZadGost',
          'omjSvukOsSet',
          'omjSvukOsSetDomacinProtGost',
          'omjSvukIzgSet',
          'omjSvukIzgSetDomacinProtGost',
          'omjSvukOsBod',
          'omjSvukOsBodDomacinProtGost',
          'omjSvukIzgBod',
          'omjSvukIzgBodDomacinProtGost']

EKIPE= ['OK MEDICINAR TRNJE', 'OK ROVINJ', 'MOK MARSONIA', 'OK ZADAR', 'OK SPLIT', 'MOK RIJEKA', 'OKM CENTROMETAL',
        'OK KITRO VARAŽDIN', 'MOK MURSA - OSIJEK', 'OK SISAK', 'OK RIBOLA KAŠTELA', 'HAOK MLADOST', 'OK GORICA']
brUtakmicepretSez = 14

def pobjedeEkipe(i):
    switcher ={
        'OK MEDICINAR TRNJE':4,
        'OK ROVINJ':3,
        'MOK MARSONIA':1,
        'OK ZADAR':2,
        'OK SPLIT':6,
        'MOK RIJEKA':11,
        'OKM CENTROMETAL':4,
        'OK KITRO VARAŽDIN':6,
        'MOK MURSA - OSIJEK':7,
        'OK SISAK':4,
        'OK RIBOLA KAŠTELA':11,
        'HAOK MLADOST':14,
        'OK GORICA':0
        }
    return switcher.get(i, "Invalid team name")

def Parovi():
    listaEkipa = EKIPE.copy()
    parovi = {}
    for ekipa1 in EKIPE:
        listaEkipa.remove(ekipa1)
        for ekipa2 in listaEkipa:
            brUtak = 2
            brPobjEk1 = 1
            if pobjedeEkipe(ekipa1) > pobjedeEkipe(ekipa2):
                brPobjEk1 = 2
            elif pobjedeEkipe(ekipa1) < pobjedeEkipe(ekipa2):
                brPobjEk1 = 0
            brOsSetEk1 = brPobjEk1 * 3 + brUtak - brPobjEk1
            brIzgSetEk1 = (brUtak - brPobjEk1) * 3 + brPobjEk1
            osBodEk1 = brOsSetEk1 * 25 + brIzgSetEk1 * random.randint(12, 23)
            izgBodEk1 = brOsSetEk1 * random.randint(12, 23) + brIzgSetEk1 * 25
            parovi[ekipa1 + '#' + ekipa2] = {
                                     'datumZadUtak': '2019-07-01',
                                     'brUtak':brUtak,
                                     'brPobjEk1':brPobjEk1,
                                     'brGubEk1':brUtak - brPobjEk1,
                                     'brOsSetEk1':brOsSetEk1,
                                     'brIzgSetEk1':brIzgSetEk1,
                                     'osBodEk1':osBodEk1,
                                     'izgBodEk1':izgBodEk1
                                    }
    return parovi



def podaciOEkipama():
    ekipe = {}
    for ekipa in EKIPE:
        brOsSet = 3*pobjedeEkipe(ekipa) + brUtakmicepretSez - pobjedeEkipe(ekipa)
        brIzgSet = (brUtakmicepretSez - pobjedeEkipe(ekipa))*3 + pobjedeEkipe(ekipa)
        brOsBod = brOsSet*25 + brIzgSet*random.randint(12, 23)
        brIzgBod = brOsSet*random.randint(12, 23) + brIzgSet*25
        ekipe[ekipa] = {
                       'datumZadUtak':'2019-07-01',
                       'brUtak':brUtakmicepretSez,
                       'brPobj':pobjedeEkipe(ekipa),
                       'brOsSet':brOsSet,
                       'brIzgSet':brIzgSet,
                       'osBod':brOsBod,
                       'izgBod':brIzgBod
                    }
    return ekipe



def run():
    f = open(r"utakmice\clean_data\test.csv", 'w', newline='', encoding='windows-1252')
    df = pd.read_csv(r"utakmice\ordered_classified_data\test.csv", encoding='windows-1252')
    writer = csv.writer(f)
    writer.writerow(HEADER)
    row = []

    ekipe = podaciOEkipama()
    parovi = Parovi()


    for i  in range(len(df)):
        for data in df.iloc[i]:
            row.append(data)

        if not df['domacin'][i] in EKIPE:
            continue
        if not df['gost'][i] in EKIPE:
            continue

        i1 = EKIPE.index(df['domacin'][i])
        i2 = EKIPE.index(df['gost'][i])

        datumUtk = datetime.strptime(df['datum'][i], "%Y-%m-%d")
        par = {}
        if i1 < i2:
            par = parovi[df['domacin'][i] + '#' + df['gost'][i]]
        else:
            par = parovi[df['gost'][i] + '#' + df['domacin'][i]]

        #'omjProPobj'
        domacinPobjede = ekipe[df['domacin'][i]]['brPobj']/ekipe[df['domacin'][i]]['brUtak']
        gostPobjede = ekipe[df['gost'][i]]['brPobj'] / ekipe[df['gost'][i]]['brUtak']
        if(gostPobjede == 0):
            row.append('100000')
        else:
            row.append(domacinPobjede/gostPobjede)

        #'proPobjDomacinNadGost'
        row.append(par['brPobjEk1']/par['brUtak'])

        #'brDaOdZadDomacin'
        domacinDatum = datetime.strptime(ekipe[df['domacin'][i]]['datumZadUtak'], "%Y-%m-%d")
        brojDana = datumUtk - domacinDatum
        row.append(brojDana.days)


        #'brDaOdZadGost'
        gostDatum = datetime.strptime(ekipe[df['gost'][i]]['datumZadUtak'], "%Y-%m-%d")
        brojDana = datumUtk - gostDatum
        row.append(brojDana.days)
        
        #'omjSvukOsSet'
        domacinOsvojeniSetovi = ekipe[df['domacin'][i]]['brOsSet']
        gostOsvojeniSetovi = ekipe[df['gost'][i]]['brOsSet']
        row.append(domacinOsvojeniSetovi/gostOsvojeniSetovi)

        #'omjSvukOsSetDomacinProtGost',
        row.append(par['brOsSetEk1'] / par['brIzgSetEk1'])

        #'omjSvukIzgSet',
        domacinIzgubljeniSetovi = ekipe[df['domacin'][i]]['brIzgSet']
        gostIzgubljeniSetovi = ekipe[df['gost'][i]]['brIzgSet']
        row.append(domacinIzgubljeniSetovi / gostIzgubljeniSetovi)

        #'omjSvukIzgSetDomacinProtGost',
        row.append(par['brIzgSetEk1'] / par['brOsSetEk1'])

        #'omjSvukOsBod',
        domacinosBod = ekipe[df['domacin'][i]]['osBod']
        gostosBod = ekipe[df['gost'][i]]['osBod']
        row.append(domacinosBod / gostosBod)

        #'omjSvukOsBodDomacinProtGost',
        row.append(par['osBodEk1'] / par['izgBodEk1'])

        #'omjSvukIzgBod',
        domacinizgBod = ekipe[df['domacin'][i]]['osBod']
        gostizgBod = ekipe[df['gost'][i]]['osBod']
        row.append(domacinizgBod / gostizgBod)

        #'omjSvukIzgBodDomacinProtGost'
        row.append(par['izgBodEk1'] / par['osBodEk1'])

        writer.writerow(row)
        
        #update podataka ekipe
        ekipe[df['domacin'][i]]['datumZadUtak'] = str(datumUtk).split(' ')[0]
        ekipe[df['gost'][i]]['datumZadUtak'] = str(datumUtk).split(' ')[0]
        
        ekipe[df['domacin'][i]]['brUtak'] += 1
        ekipe[df['gost'][i]]['brUtak'] += 1
        
        if df['pobjednikDomacinIliGost'][i] == 0:
            ekipe[df['domacin'][i]]['brPobj'] += 1
        else:
            ekipe[df['gost'][i]]['brPobj'] += 1

        ekipe[df['domacin'][i]]['brOsSet'] += df['brOsSetDomacin'][i]
        ekipe[df['gost'][i]]['brOsSet'] += df['brOsSetGost'][i]

        ekipe[df['domacin'][i]]['brIzgSet'] += df['brOsSetGost'][i]
        ekipe[df['gost'][i]]['brIzgSet'] += df['brOsSetDomacin'][i]

        ekipe[df['domacin'][i]]['osBod'] += df['osBodDomacin'][i]
        ekipe[df['gost'][i]]['osBod'] += df['osBodGost'][i]

        ekipe[df['domacin'][i]]['izgBod'] += df['osBodGost'][i]
        ekipe[df['gost'][i]]['izgBod'] += df['osBodDomacin'][i]

        # update podataka parovi
        par['datumZadUtak'] = str(datumUtk).split(' ')[0]

        par['brUtak'] += 1

        if df['pobjednikDomacinIliGost'][i] == 0:
            par['brPobjEk1'] += 1
        else:
            par['brGubEk1'] += 1

        if i1 < i2:
            par['brOsSetEk1'] += df['brOsSetDomacin'][i]
            par['brIzgSetEk1'] += df['brOsSetGost'][i]
        else:
            par['brOsSetEk1'] += df['brOsSetGost'][i]
            par['brIzgSetEk1'] += df['brOsSetDomacin'][i]

        if i1 < i2:
            par['osBodEk1'] += df['osBodDomacin'][i]
            par['izgBodEk1'] += df['osBodGost'][i]
        else:
            par['osBodEk1'] += df['osBodGost'][i]
            par['izgBodEk1'] += df['osBodDomacin'][i]
        row = []
    # close the file
    f.close()