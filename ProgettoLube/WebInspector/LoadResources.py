import pandas as pd
import json


class LoadResources:

    # METODO per ottenere la lista dei siti da analizzare
    def load_name_resellers(self):
        df = pd.read_excel('ELENCO 500 STORE (sit+social).xlsx',
                           sheet_name='Foglio1')  # can also index sheet by name or fetch all sheets
        mydict = df.to_dict()
        lista = list(mydict['INSEGNA/NOME NEGOZIO'].values())
        lista = [x for x in lista if str(x) != 'nan']
        lista = sorted(lista)
        return lista

    ############################# MAPPA ##########################################################à
    def load_store_positions(self):
        columns = ['INSEGNA/NOME NEGOZIO', 'LATITUDINE', 'LONGITUDINE']
        df = pd.read_excel('ELENCO 500 STORE (sit+social).xlsx', sheet_name='Foglio1', usecols=columns)
        dictionary = {}
        #lista = []
        for index, row in df.iterrows():
            dictionary[row[0]] = {"Latitudine": row[1], "Longitudine": row[2]}
        pino = []
        # pulizia chiavi nan
        for key, value in dictionary.items():
            if str(key) == 'nan':
                pino.append(key)
            for x,y in value.items():
                if str(y) == 'nan':
                    pino.append(key)
        pino = list(dict.fromkeys(pino))
        for x in pino:
            dictionary.pop(x)
        return dictionary

############################# MAPPA ##########################################################à
# TODO: al fronty nei dettagli di un sito gli si passa il dict ricqvato sopra cosi ha tutto di quel sito
