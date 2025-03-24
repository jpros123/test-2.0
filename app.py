import streamlit as st
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid
import requests
import zipfile
import matplotlib.pyplot as plt

# Interface com Streamlit
st.title("Fundos de Investimentos")

# Configuração de exibição do pandas
pd.options.display.float_format = '{:.4f}'.format

# Entrada do usuário para ano e mês
ano = "2025"
mes = "03"

# URL para download dos dados
url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip'

# Download do arquivo
download = requests.get(url)

with open(f"inf_diario_fi_{ano}{mes}.zip", "wb") as arquivo_cvm:
    arquivo_cvm.write(download.content)

# Extração do arquivo ZIP
arquivo_zip = zipfile.ZipFile(f"inf_diario_fi_{ano}{mes}.zip")
dados_fundos = pd.read_csv(arquivo_zip.open(arquivo_zip.namelist()[0]), sep=";", encoding='ISO-8859-1')

# Leitura dos dados de cadastro
dados_cadastro = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', 
                             sep=";", encoding='ISO-8859-1')
dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']].drop_duplicates()

# Filtragem por datas no início e fim do mês
data_inicio_mes = (dados_fundos['DT_COMPTC'].sort_values(ascending=True).unique())[0]
data_fim_mes = (dados_fundos['DT_COMPTC'].sort_values(ascending=True).unique())[-1]
dados_fundos_filtrado = dados_fundos[(dados_fundos['DT_COMPTC'].isin([data_inicio_mes, data_fim_mes]))]



# Sidebar para entrada de dados e filtros
st.sidebar.title("Previnorte")
st.sidebar.image("imagens/273731962_442203134141407_7743180946701135051_n.png")
st.sidebar.subheader("Pesquisar Fundos")
opcao_pesquisa = st.sidebar.selectbox("Escolha o tipo de pesquisa:", ["CNPJ", "Nome"])
termo_pesquisa = st.sidebar.text_input("Digite o termo de pesquisa:")

if termo_pesquisa:
    if opcao_pesquisa == "CNPJ":
        resultados = dados_cadastro[dados_cadastro['CNPJ_FUNDO'].str.contains(termo_pesquisa, na=False)]
    else:
        resultados = dados_cadastro[dados_cadastro['DENOM_SOCIAL'].str.contains(termo_pesquisa, na=False)]
    
    if not resultados.empty:
        st.write("Resultados da Pesquisa:")
        st.dataframe(resultados)
    else:
        st.write("Nenhum resultado encontrado.")
  


# Exibição dos dados filtrados por data
st.subheader("Dados Filtrados por Data")
st.write(f"Início do mês: {data_inicio_mes}, Fim do mês: {data_fim_mes}")
st.dataframe(dados_cadastro)
st.dataframe(dados_fundos)