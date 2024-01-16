import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.cloud.bigquery.client import Client


client = Client(project = 'fiap-tech-challenge-4')
dataset_id = 'tech_challenge_4'
table_id = 'petroleo_brent'


try:
    # obtencao de dados do Ipea
    url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        html_table = soup.find('table', {'id': 'grd_DXMainTable'})

        if html_table:
            # transforma a tabela HTML em DataFrame usando pandas
            df = pd.read_html(str(html_table),  header=0, thousands='', decimal=',')[0]

            df = df.rename(columns={'Data' : 'data', 'Preço - petróleo bruto - Brent (FOB)' : 'preco_petroleo_brent'})
            df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")

            try:
                query = "SELECT max(data) as data FROM `fiap-tech-challenge-4.tech_challenge_4.petroleo_brent`"

                query_job = client.query(query)
                rows = query_job.result()

                for row in rows:
                    max_date = row[0]

                table_ref = client.dataset(dataset_id).table(table_id)

                if not max_date:                    
                    job = client.load_table_from_dataframe(df, table_ref)
                    job.result()
                else:
                    # insere apenas os dias que nao estao contidos no banco de dados                                       
                    job = client.load_table_from_dataframe(df[df['data'] > max_date], table_ref)
                    job.result()

            except Exception as e:
                print(f'Ocorreu um erro ao obter os dados do Google BigQuery: {e}')

        else:
            print('Tabela não encontrada.')

    else:
        print(f'Erro na requisição. Status Code: {response.status_code}')

except Exception as e:
    print(f'Ocorreu um erro: {e}')