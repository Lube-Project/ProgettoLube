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
        supporto = {}
        lista = []
        for index, row in df.iterrows():
            paolo = {"nome": row[0], "latitudine": row[1], "longitudine": row[2]}
            lista.append(paolo)
            # dictionary[row[0]] = {"Latitudine": row[1], "Longitudine": row[2]}
            # dictionary.update({"nome": row[0], "latitudine": row[1], "longitudine": row[2]})
        # print(lista)
        pino = []
        for x in lista:
            if str(x['nome']) == 'nan' or str(x['latitudine']) == 'nan' or str(x['longitudine']) == 'nan':
                pino.append(x)
        print(pino)
        for x in pino:
            lista.remove(x)
        print(lista)
        # pulizia chiavi nan
        # for key, value in dictionary.items():
        # if str(key) == 'nan':
        # pino.append(key)
        # for x, y in value.items():
        # if str(y) == 'nan':
        # pino.append(key)
        # pino = list(dict.fromkeys(pino))
        # for x in pino:
        # dictionary.pop(x)

        # print(dictionary)
        return lista

    def load_store_details_name(self, name):
        col = "INSEGNA/NOME NEGOZIO"
        df = pd.read_excel('ELENCO 500 STORE (sit+social).xlsx',
                           sheet_name='Foglio1')  # can also index sheet by name or fetch all sheets
        obj = df.loc[df[col] == name]
        dict = obj.dropna(axis=1).to_dict()
        pino = {}
        for key, value in dict.items():
            for x, y in value.items():
                pino[key] = y
        return pino
