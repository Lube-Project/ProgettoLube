import pandas as pd


# METODO per ottenere la lista dei siti da analizzare
def loadsiti():
    df = pd.read_excel('filename.xlsm', sheetname=0)  # can also index sheet by name or fetch all sheets
    mylist = df['column name'].tolist()
    return mylist
