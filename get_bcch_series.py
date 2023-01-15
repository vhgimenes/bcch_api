"""
Author: Victor Gimenes
Date: 24/05/2022
Módulo responsável por extrair as séries de dados de Encuesta Economicas do Banco Central do Chile.
"""

#Importando módulos
from time import strftime
import requests
import pandas as pd
import xlwings as xw
from datetime import datetime

#Funções auxiliares
def get_user():
    return 'enter your user here!'

def get_password():
    return 'enter your password here!'

#Funções principais
def get_series_from_api(first_date: str, last_date: str, series_id: list):
    print('Iniciando aquisição dos dados da API do BCCch...')
    final_df = pd.DataFrame()
    for i in series_id:  
        url = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={get_user()}&pass={get_password()}&firstdate={first_date}&lastdate={last_date}&timeseries={i}&function=GetSeries"
        try:
            print(f'Realizando Request da série {i}...')
            response = requests.get(url)
            response = response.json()
            response = response["Series"]["Obs"]
            df = pd.DataFrame(response)
            df.columns = ['Data',i,'Status']
            df = df[['Data',i]]
            df['Data'] = pd.to_datetime(df['Data'])
            df.set_index('Data',inplace=True)
            print(f'Request da série {i} realizado com sucesso! \n')
            final_df = pd.concat([final_df,df],axis=1)
        except Exception as e:
            print(f'Error in request {i}: {e}. \n')
    print('Tabela final de dados montada com sucesso!\n')
    return final_df

