import pandas as pd
import csv

HEADER = ['datum', 'domacin', 'gost', 'rezultat', 'brOsSetDomacin', 'brOsSetGost',
          'osBodDomacin', 'osBodGost', 'proRazBodUSet', 'pobjednik', 'pobjednikDomacinIliGost']

def run():

    f = open(r"utakmice/ordered_classified_data/test.csv", 'w', newline='',
             encoding='windows-1252')
    df = pd.read_csv(r"utakmice\unordered_classified_data\test.csv", encoding='windows-1252')
    df["datum"] = pd.to_datetime(df["datum"]).dt.date
    df = df.sort_values(by="datum")

    writer = csv.writer(f)
    writer.writerow(HEADER)

    for i in range(len(df)):
        writer.writerow(df.iloc[i])

    f.close()