import pandas as pd


class LoadResources:

    # METODO per ottenere la lista dei siti da analizzare
    def load_name_resellers(self):
        df = pd.read_excel('ELENCO 500 STORE (sit+social).xlsx', sheet_name='Foglio1')  # can also index sheet by name or fetch all sheets
        mydict = df.to_dict()
        lista = list(mydict['INSEGNA/NOME NEGOZIO'].values())
        lista = [x for x in lista if str(x) != 'nan']
        lista = sorted(lista)
        return lista

#TODO: al fronty nei dettagli di un sito gli si passa il dict ricqvato sopra cosi ha tutto di quel sito