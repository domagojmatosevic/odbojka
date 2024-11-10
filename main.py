import pandas as pd
import csv
import poredak
import doradaPodataka

MJESECI = ['siječnja', 'veljače', 'ožujka', 'travnja', 'svibnja', 'lipnja', 'srpnja', 'kolovoza', 'rujna', 'listopada', 'studenog','prosinca']
HEADER = ['datum', 'domacin', 'gost', 'rezultat', 'brOsSetDomacin', 'brOsSetGost',
          'osBodDomacin', 'osBodGost', 'proRazBodUSet', 'pobjednik', 'pobjednikDomacinIliGost']


if __name__ == "__main__":

    f = open(r"utakmice/unordered_classified_data/test.csv", 'w', newline='',
             encoding='windows-1252')
    writer = csv.writer(f)
    writer.writerow(HEADER)
    row = []

    df = pd.read_csv(r"utakmice\scraped_data\test.csv")

    # datumi spremljeni u obliku: Vrijeme početka: subota, 19. rujna 2020. u 17,00
    datum = df['datum']

    # bodovi osvojeni u setovima i ukupan broj osvojenih bodova spremljeni u obliku: "1. set: 15:25
    #      2. set: 24:26
    #      3. set: 25:23
    #      4. set: 25:23
    #      5. set: 15:12
    #      ukupno: 104:109"
    bodovi = df['bodovi']

    # imena ekipa koje su igrale utakmicu spremljene u obliku:OK ZADAR – OK SISAK
    # prva ekipa je domacin, a druga je gost
    ekipe = df['link']
    for i in range(len(datum)):
        # oblik koji treba biti: Vrijeme početka: subota, 19. rujna 2020. u 17,00
        if type(datum[i]) == float or datum[i].split(' ')[0] != 'Vrijeme':
            continue

        # datum se mijenja u novi oblik(npr. subota, 19. rujna 2020. u 17,00 -> 19-09-2020)
        for redni in range(len(MJESECI)):
            if MJESECI[redni] == datum[i].split(', ')[1].split(' u')[0].split(' ')[1]:
                # zapis datuma
                s = datum[i].split(', ')[1].split(' u')[0].replace(MJESECI[redni], str(redni+1)+'.').replace('. ','-').replace('.', '')
                row.append(s.split('-')[2] + "-" + s.split('-')[1] + "-" + s.split('-')[0])

        # zapis domacina
        row.append(ekipe[i].split(' – ')[0].strip().replace("OK MLADOST RIBOLA KAŠTELA", "OK RIBOLA KAŠTELA"))
        # zapis gosta
        row.append(ekipe[i].split(' – ')[1].strip().replace("OK MLADOST RIBOLA KAŠTELA", "OK RIBOLA KAŠTELA"))

        # izracun broja osvojenih setova svake ekipe i razlike
        setD = 0
        setG = 0
        for n in bodovi[i].split('\n'):
            if 'set' in n:
                d = int(n.split('set: ')[1].split(':')[0])
                g = int(n.split('set: ')[1].split(':')[1])
                if d > g:
                    setD = setD + 1
                else:
                    setG = setG + 1

        # zapis rezultata
        row.append(' ' + str(setD) + '-' + str(setG))

        # zapis osvojenih setova domacina
        row.append(setD)

        # zapis osvojenih setova gosta
        row.append(setG)

        # zapis osvojenih bodova domacina
        row.append(bodovi[i].split('ukupno: ')[1].split(':')[0])

        # zapis osvojenih bodova gosta
        row.append(bodovi[i].split('ukupno: ')[1].split(':')[1])

        # izracun razlike osvojenih bodova podijeljenih s ukupnim brojem setova
        razlika = int(bodovi[i].split('ukupno: ')[1].split(':')[0]) - int(bodovi[i].split('ukupno: ')[1].split(':')[1])

        # zapis razlika
        row.append(razlika / (setD + setG))

        if setD > setG:
            # zapis imena domacina u pobjednik
            row.append(ekipe[i].split(' – ')[0].strip().replace("OK MLADOST RIBOLA KAŠTELA", "OK RIBOLA KAŠTELA"))
            # zapis pobjednikDomacinIliGost
            row.append(0)
        else:
            # zapis imena gosta u pobjednik
            row.append(ekipe[i].split(' – ')[1].strip().replace("OK MLADOST RIBOLA KAŠTELA", "OK RIBOLA KAŠTELA"))
            # zapis pobjednikDomacinIliGost
            row.append(1)

        # zapis utakmice u datoteku s podacima
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            print(row)
            print(setD)
            print(setG)
            row = []
        row = []

    # close the file
    f.close()
    poredak.run()
    doradaPodataka.run()


