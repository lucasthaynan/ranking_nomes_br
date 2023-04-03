print("teste")# importando .csv com dados de nome e região de cada estado
import requests
import pandas as pd
import json
from tqdm import tqdm 
from json.decoder import JSONDecodeError
import urllib.parse

# importando .csv com dados de nome e região de cada estado
info_ufs = pd.read_csv('dados_estados.csv')

# para evitar erro 403 (sem autorização)
session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})

# raspando dados de registros totais por uf
resposta_estados = session.get('https://transparencia.registrocivil.org.br/api/record/birth', headers=headers)
resposta_estados = resposta_estados.json()

# Dados por município

resposta_municipios = session.get('https://transparencia.registrocivil.org.br/api/cities')
resposta_municipios = resposta_municipios.json()


df_municipios = pd.DataFrame()

for item in tqdm(resposta_municipios['cities']):
    try:
        municipio_encode = urllib.parse.quote(item['name'])        
        uf_busca = item['uf']     
        resposta = session.get(f'https://transparencia.registrocivil.org.br/api/record/all-name?start_date=2021-01-01&end_date=2021-12-31&translate=1&state={uf_busca}&city={municipio_encode}')

        resposta = resposta.json()
        df_resposta = pd.DataFrame(resposta['data'])
        df_resposta['uf'] = uf_busca
        df_resposta['municipio'] = item['name']
        df_resposta['ano'] = 2021
        df_resposta.index = df_resposta.index + 1
        #display(df_resposta)
        df_municipios = df_municipios.append(df_resposta)

    except json.decoder.JSONDecodeError:
        print(item['name']) 
        print(item['uf'])
        print(resposta.status_code)
        print("String could not be converted to JSON")
        continue  
         
total_municipios = len(df_municipios.groupby('municipio').sum())
print(f"Total de municipios coletados: {total_municipios}")

df_municipios.to_csv('nomes_mais_registrados_municipios_2022.csv')
