
import pandas as pd
pd.set_option("display.max_colwidth", 150)
#pd.options.display.float_format = '{:.2f}'.format

""">Funções que buscam dados no site da CVM e retornam um DataFrame Pandas:

"""

def busca_informes_cvm(ano, mes):
  url = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{:02d}{:02d}.csv'.format(ano,mes)
  return pd.read_csv(url, sep=';')

def busca_cadastro_cvm():
  url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
  return pd.read_csv(url, sep=';', encoding='ISO-8859-1')

""">Buscando dados no site da CVM"""

informes_diarios = busca_informes_cvm(2021,9)

informes_diarios

cadastro_cvm = busca_cadastro_cvm()

cadastro_cvm

cadastro_cvm

"""###Manipulando os dados da CVM

>Definindo filtros para os Fundos de Investimento
"""

minimo_cotistas = 100

""">Manipulando os dados e aplicando filtros"""

fundos = informes_diarios[informes_diarios['NR_COTST'] >= minimo_cotistas].pivot(index='DT_COMPTC', columns='CNPJ_FUNDO', values=['VL_TOTAL',	'VL_QUOTA',	'VL_PATRIM_LIQ',	'CAPTC_DIA',	'RESG_DIA'])

fundos

""">Normalizando os dados de cotas para efeitos comparativos"""

cotas_normalizadas = fundos['VL_QUOTA'] / fundos['VL_QUOTA'].iloc[0]

cotas_normalizadas

"""###Fundos de Investimento com os melhores desempenhos em Abril de 2020"""

melhores = pd.DataFrame()
melhores['retorno(%)'] = (cotas_normalizadas.iloc[-1].sort_values(ascending=False)[:5] - 1) * 100
melhores

""">Buscando dados dos Fundos de Investimento pelo CNPJ"""

for cnpj in melhores.index:
  fundo = cadastro_cvm[cadastro_cvm['CNPJ_FUNDO'] == cnpj]
  melhores.at[cnpj, 'Fundo de Investimento'] = fundo['DENOM_SOCIAL'].values[0]
  melhores.at[cnpj, 'Classe'] = fundo['CLASSE'].values[0]
  melhores.at[cnpj, 'PL'] = fundo['VL_PATRIM_LIQ'].values[0]

melhores

"""###Fundos de Investimento com os piores desempenhos em Abril de 2020"""

piores = pd.DataFrame()
piores['retorno(%)'] = (cotas_normalizadas.iloc[-1].sort_values(ascending=True)[:5] - 1) * 100
piores

""">Buscando dados dos Fundos de Investimento pelo CNPJ"""

for cnpj in piores.index:
  fundo = cadastro_cvm[cadastro_cvm['CNPJ_FUNDO'] == cnpj]
  piores.at[cnpj, 'Fundo de Investimento'] = fundo['DENOM_SOCIAL'].values[0]
  piores.at[cnpj, 'Classe'] = fundo['CLASSE'].values[0]
  piores.at[cnpj, 'PL'] = fundo['VL_PATRIM_LIQ'].values[0]

piores

