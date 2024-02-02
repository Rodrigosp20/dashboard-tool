import time
import numpy as np
import pandas as pd
import plotly.express as px  # pip install plotly
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import math

# pip install openpyxl

# python -m streamlit run teste.py

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏡",
    layout="wide",
)

hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''

st.markdown(hide_img_fs, unsafe_allow_html=True)


##############################DEMONSTRAÇÃO E RESULTADOS###############################

def EBITDA_calc(col): 
    return round(st.session_state.df_demo_resultados.loc[0:4,col].sum()+st.session_state.df_demo_resultados.loc[13:14,col].sum()-(st.session_state.df_demo_resultados.loc[5:12,col].sum()+st.session_state.df_demo_resultados.loc[16,col].sum()),2)

def EBIT_calc(col):
    return round(st.session_state.df_demo_resultados.loc[18,col]-st.session_state.df_demo_resultados.loc[19:20,col].sum(), 2)
    
def result_antes_impostos_calc(col):
    return round(st.session_state.df_demo_resultados.loc[21:22,col].sum()-st.session_state.df_demo_resultados.loc[23,col].sum(), 2)
    
def result_liquido_calc(col):
    return round(st.session_state.df_demo_resultados.loc[24,col]-st.session_state.df_demo_resultados.loc[25,col], 2)    
    
def autofinanciamento_calc(col):
    return st.session_state.df_demo_resultados.loc[26:26,col].sum()+st.session_state.df_demo_resultados.loc[19:20,col].sum()+st.session_state.df_demo_resultados.loc[13:13,col].sum()+st.session_state.df_demo_resultados.loc[8:11,col].sum()
    
def vbp_calc(col):
    return st.session_state.df_demo_resultados.loc[0:1,col].sum()+st.session_state.df_demo_resultados.loc[3:4,col].sum()
    
def vab_calc(col):
    return st.session_state.df_demo_resultados.loc[30:30,col].sum()-st.session_state.df_demo_resultados.loc[5:6,col].sum()
    
def calc_demo_resultados_df():  
    for year in st.session_state.df_demo_resultados.columns[1:]:
        st.session_state.df_demo_resultados.at[18,year] = EBITDA_calc(year)
        st.session_state.df_demo_resultados.at[21,year] = EBIT_calc(year)
        st.session_state.df_demo_resultados.at[24,year] = result_antes_impostos_calc(year)
        st.session_state.df_demo_resultados.at[26,year] = result_liquido_calc(year)
        st.session_state.df_demo_resultados.at[29,year] = autofinanciamento_calc(year)
        st.session_state.df_demo_resultados.at[30,year] = vbp_calc(year)
        st.session_state.df_demo_resultados.at[31,year] = vab_calc(year)
    return st.session_state.df_demo_resultados
    
##############################BALANÇO###############################
def ativo_nao_corrent_calc(col):
    return round(st.session_state.df_balanco.loc[1:11,col].sum() ,2)
    
def ativo_corrent_calc(col):
    return round(st.session_state.df_balanco.loc[13:25,col].sum() ,2)
    
def total_ativo_calc(col):
    return round(st.session_state.df_balanco.loc[0:0,col].sum()+st.session_state.df_balanco.loc[12:12,col].sum() ,2)
    
def total_capital_proprio(col):
    return round(st.session_state.df_balanco.loc[28:40,col].sum() ,2)
    
def passivo_nao_corrente(col):
    return round(st.session_state.df_balanco.loc[44:48,col].sum() ,2)
    
def passivo_corrente(col):
    return st.session_state.df_balanco.loc[50:60,col].sum()
    
def total_passivo(col):
    return round(st.session_state.df_balanco.loc[43:43,col].sum()+st.session_state.df_balanco.loc[49:49,col].sum() ,2)
    
def total_capital_proprio_mais_passivo(col):
    return round(st.session_state.df_balanco.loc[61:61,col].sum()+st.session_state.df_balanco.loc[41:41,col].sum() ,2)

def calc_balanco_df():
    for year in st.session_state.df_balanco.columns[1:]:
        st.session_state.df_balanco.at[0,year] = ativo_nao_corrent_calc(year)
        st.session_state.df_balanco.at[12,year] = ativo_corrent_calc(year)
        st.session_state.df_balanco.at[26,year] = total_ativo_calc(year)
        st.session_state.df_balanco.at[41,year] = total_capital_proprio(year)
        st.session_state.df_balanco.at[43,year] = passivo_nao_corrente(year)
        st.session_state.df_balanco.at[49,year] = passivo_corrente(year)
        st.session_state.df_balanco.at[61,year] = total_passivo(year)
        st.session_state.df_balanco.at[62,year] = total_capital_proprio_mais_passivo(year)
    return st.session_state.df_balanco
##############################INDICADORES############################
def margem_operacional(col):
    return (st.session_state.df_demo_resultados.loc[18,col] / st.session_state.df_demo_resultados.loc[0,col])

def margem_bruta(col):
    return (st.session_state.df_demo_resultados.loc[0,col]-st.session_state.df_demo_resultados.loc[5,col])/st.session_state.df_demo_resultados.loc[0,col]
    
def margem_liquida(col):
    return st.session_state.df_demo_resultados.loc[26,col]/st.session_state.df_demo_resultados.loc[0,col]
    
def nivel_valor_acrescentado(col):
    return st.session_state.df_demo_resultados.loc[31,col]/st.session_state.df_demo_resultados.loc[30,col]
    
def rentabilidade_ativo(col):
    return st.session_state.df_demo_resultados.loc[26,col]/st.session_state.df_balanco.loc[26,col]
  
def turnover_ativo(col):
    return st.session_state.df_demo_resultados.loc[0,col]/st.session_state.df_balanco.loc[26,col]
    
def rh_volume_negocios(col):
    return st.session_state.df_demo_resultados.loc[7,col]/st.session_state.df_demo_resultados.loc[0,col]
    
def fse_volume_negocios(col):
    return st.session_state.df_demo_resultados.loc[6,col]/st.session_state.df_demo_resultados.loc[0,col]
    
def cmvmc_volume_negocios(col):
    return st.session_state.df_demo_resultados.loc[5,col]/st.session_state.df_demo_resultados.loc[0,col]
    
def custos_volume_negocios(col):
    return (st.session_state.df_demo_resultados.loc[5,col]+st.session_state.df_demo_resultados.loc[6,col]+st.session_state.df_demo_resultados.loc[7,col])/st.session_state.df_demo_resultados.loc[0,col]

def prazo_medio_pagamentos(col):
    return (st.session_state.df_balanco.loc[50,col] / ((st.session_state.df_demo_resultados.loc[5,col]+st.session_state.df_demo_resultados.loc[6,col]) * 1.23)) * 365
    
def prazo_medio_recebimentos(col):
    return (st.session_state.df_balanco.loc[15,col] / (st.session_state.df_demo_resultados.loc[0,col]*1.23))*365
    
def valor_gerado_rh(col):
    return st.session_state.df_demo_resultados.loc[31,col]/st.session_state.df_demo_resultados.loc[32,col]
    
# def taxa_exportacao(col):
    # return 

def liquidez_geral(col):
    return st.session_state.df_balanco.loc[12,col]/st.session_state.df_balanco.loc[49,col]
    
def liquidez_reduzida(col):
    return (st.session_state.df_balanco.loc[12,col]-st.session_state.df_balanco.loc[13,col])/st.session_state.df_balanco.loc[49,col]
    
def liquidez_imediata(col):
    return st.session_state.df_balanco.loc[25,col]/st.session_state.df_balanco.loc[49,col]
    
def autonomia_financeira(col):
    return st.session_state.df_balanco.loc[41,col]/st.session_state.df_balanco.loc[26,col]
    
def endividamento(col):
    return st.session_state.df_balanco.loc[61,col]/st.session_state.df_balanco.loc[26,col]
    
def solvabilidade(col):
    return st.session_state.df_balanco.loc[26,col]/st.session_state.df_balanco.loc[61,col]
    
def alavancagem_financeira(col):
    return (st.session_state.df_balanco.loc[45,col]+st.session_state.df_balanco.loc[54,col])/(st.session_state.df_balanco.loc[41,col]+st.session_state.df_balanco.loc[45,col]+st.session_state.df_balanco.loc[54,col])
    
def rentabilidade_capital_investido(col):
    return (st.session_state.df_demo_resultados.loc[21,col]-st.session_state.df_demo_resultados.loc[25,col])/st.session_state.df_balanco.loc[26,col]

def rentabilidade_capital_proprio(col):
    return st.session_state.df_demo_resultados.loc[26,col]/st.session_state.df_balanco.loc[41,col]
    
def calc_indicadores_df():
    for year in st.session_state.df_indicadores.columns[2:]:
        st.session_state.df_indicadores.at[1,year] = margem_operacional(year)
        st.session_state.df_indicadores.at[2,year] = margem_bruta(year)
        st.session_state.df_indicadores.at[3,year] = margem_liquida(year)
        st.session_state.df_indicadores.at[4,year] = nivel_valor_acrescentado(year)
        st.session_state.df_indicadores.at[5,year] = rentabilidade_ativo(year)
        
        st.session_state.df_indicadores.at[7,year] = turnover_ativo(year)
        st.session_state.df_indicadores.at[8,year] = rh_volume_negocios(year)
        st.session_state.df_indicadores.at[9,year] = fse_volume_negocios(year)
        st.session_state.df_indicadores.at[10,year] = cmvmc_volume_negocios(year)
        st.session_state.df_indicadores.at[11,year] = custos_volume_negocios(year)
        st.session_state.df_indicadores.at[12,year] = prazo_medio_pagamentos(year)
        st.session_state.df_indicadores.at[13,year] = prazo_medio_recebimentos(year)
        st.session_state.df_indicadores.at[14,year] = valor_gerado_rh(year)
        #st.session_state.df_indicadores.at[15,year] = taxa_exportacao(year)
        st.session_state.df_indicadores.at[17,year] = liquidez_geral(year)
        st.session_state.df_indicadores.at[18,year] = liquidez_reduzida(year)
        st.session_state.df_indicadores.at[19,year] = liquidez_imediata(year)
        st.session_state.df_indicadores.at[21,year] = autonomia_financeira(year)
        st.session_state.df_indicadores.at[22,year] = endividamento(year)
        st.session_state.df_indicadores.at[23,year] = solvabilidade(year)
        st.session_state.df_indicadores.at[24,year] = alavancagem_financeira(year)
        st.session_state.df_indicadores.at[26,year] = rentabilidade_capital_investido(year)
        st.session_state.df_indicadores.at[27,year] = rentabilidade_capital_proprio(year)
    return st.session_state.df_indicadores
    
##############################DADOS DO SETOR#########################
def create_dados_setor_df():
    df_dados_setor = pd.DataFrame()
    df_dados_setor['Rúbricas'] = ['Volume de Negócios', 'EBITDA', 'CMVMC','Gastos com Pessoal','FSE', 'Resultados Líquidos', 'Ativo', 'Passivo',
    'Capital próprio', 'Ativo corrente', 'Passivo corrente', 'Fornecedores', 'Clientes', 'Inventários', 'Caixa e depósitos bancários',
    'Financiamentos obtidos', 'Imposto', 'Taxa de VAB na CAE', 'Prazo médio de pagamentos', 'Prazo médio de recebimentos', 'EBIT', 
    'Número de pessoas ao serviço', 'Valor acrescentado bruto (VAB)', 'Taxa de exportação', 'VAB em percentagem da produção']
    
    for year in st.session_state.df_todas_dimen.columns[1:]:
        
        df_dados_setor[int(year.split()[0])] = 0
    
    return df_dados_setor

def create_quartis_df():
    df_quartis = pd.DataFrame()
    df_quartis['Indicadores'] = ['Liquidez geral','Liquidez geral','Liquidez geral',
    'Liquidez reduzida','Liquidez reduzida','Liquidez reduzida',
    'Autonomia financeira','Autonomia financeira', 'Autonomia financeira',
    'Alavancagem financeira', 'Alavancagem financeira', 'Alavancagem financeira',
    'Margem EBITDA em percentagem dos rendimentos','Margem EBITDA em percentagem dos rendimentos','Margem EBITDA em percentagem dos rendimentos',
    'Rentabilidade do Capital Próprio','Rentabilidade do Capital Próprio','Rentabilidade do Capital Próprio']
    df_quartis['Quartil'] = ['Quartil 1','Mediana','Quartil 3','Quartil 1','Mediana','Quartil 3','Quartil 1','Mediana',
    'Quartil 3','Quartil 1','Mediana','Quartil 3','Quartil 1','Mediana','Quartil 3','Quartil 1','Mediana','Quartil 3',]
    
    for year in st.session_state.df_dimen_aplicavel.columns[1:]:
        df_quartis[year.split()[0]] = 0
    
    return df_quartis
    
    
##############################COMPARAÇÃO############################

def create_comparacao_df():
    st.session_state.df_comparacao = pd.DataFrame()
    
    st.session_state.df_comparacao['Indicador'] = ['Rentabilidade do Negócio','Margem Operacional','Margem Operacional','Margem Operacional',
    'Margem Bruta','Margem Bruta','Margem Bruta', 'Margem Líquida', 'Margem Líquida', 'Margem Líquida',
    'Nível de Valor Acrescentado','Nível de Valor Acrescentado','Nível de Valor Acrescentado','Rentabilidade do Ativo',
    'Rentabilidade do Ativo','Rentabilidade do Ativo', 'Operacionais', 'Turnover do Ativo', 'Turnover do Ativo', 'Turnover do Ativo',
    '% Rh no Volume de Negócios','% Rh no Volume de Negócios', '% Rh no Volume de Negócios', '% FSE no Volume de Negócios',
    '% FSE no Volume de Negócios','% FSE no Volume de Negócios', '% CMVMC / Volume de negócios', '% CMVMC / Volume de negócios',
    '% CMVMC / Volume de negócios', '% Custos no Volume de Negócios','% Custos no Volume de Negócios','% Custos no Volume de Negócios',
    'Prazo Médio de Pagamentos','Prazo Médio de Pagamentos','Prazo Médio de Pagamentos', 'Prazo Médio de Recebimentos', 'Prazo Médio de Recebimentos',
    'Prazo Médio de Recebimentos', 'Valor gerado por RH', 'Valor gerado por RH', 'Valor gerado por RH', 'Taxa de Exportação', 'Taxa de Exportação',
    'Taxa de Exportação', 'Liquidez', 'Liquidez Geral', 'Liquidez Geral', 'Liquidez Geral', 'Liquidez Reduzida', 'Liquidez Reduzida', 'Liquidez Reduzida',
    'Liquidez imediata', 'Liquidez imediata', 'Liquidez imediata', 'Financeiros', 'Autonomia Financeira', 'Autonomia Financeira', 'Autonomia Financeira',
    'Endividamento', 'Endividamento', 'Endividamento', 'Solvabilidade', 'Solvabilidade', 'Solvabilidade', 'Alavancagem Financeira', 'Alavancagem Financeira',
    'Alavancagem Financeira', 'Retorno', 'Rentabilidade do Capital Investido', 'Rentabilidade do Capital Investido', 'Rentabilidade do Capital Investido',
    'Rentabilidade do Capital Próprio', 'Rentabilidade do Capital Próprio', 'Rentabilidade do Capital Próprio']
    
    st.session_state.df_comparacao['Fórmula de Cálculo'] = [None,'EBITDA/Volume de Negócios', 'EBITDA/Volume de Negócios', 'EBITDA/Volume de Negócios',
    '(Volume de Negócios-CMVMC)/Volume de Negócios', '(Volume de Negócios-CMVMC)/Volume de Negócios', '(Volume de Negócios-CMVMC)/Volume de Negócios',
    'Resultados Líquidos / Volume de Negócios', 'Resultados Líquidos / Volume de Negócios', 'Resultados Líquidos / Volume de Negócios',
    'VAB/VBP x 100', 'VAB/VBP x 100', 'VAB/VBP x 100', 'Resultados Líquidos / Ativo', 'Resultados Líquidos / Ativo', 'Resultados Líquidos / Ativo',
    None, 'Volume de negócios/ Ativo', 'Volume de negócios/ Ativo', 'Volume de negócios/ Ativo', 'Gastos com pessoal / Volume de Negócios', 
    'Gastos com pessoal / Volume de Negócios', 'Gastos com pessoal / Volume de Negócios', 'FSE / Voluma de Negócios', 'FSE / Voluma de Negócios',
    'FSE / Voluma de Negócios', 'CMVMC / Volume de Negócios', 'CMVMC / Volume de Negócios', 'CMVMC / Volume de Negócios', '(CMVMC + FSE + Gastos com Pessoal) / Volume de Negócios',
    '(CMVMC + FSE + Gastos com Pessoal) / Volume de Negócios', '(CMVMC + FSE + Gastos com Pessoal) / Volume de Negócios', '(Fornecedores / (Compras x (1+Tx IVA)) x 365',
    '(Fornecedores / (Compras x (1+Tx IVA)) x 365', '(Fornecedores / (Compras x (1+Tx IVA)) x 365', 'Clientes / ((Vendas x (1+tx . IVA)) x 365', 'Clientes / ((Vendas x (1+tx . IVA)) x 365',
    'Clientes / ((Vendas x (1+tx . IVA)) x 365', 'VAB / N.º de Recursos Humanos', 'VAB / N.º de Recursos Humanos', 'VAB / N.º de Recursos Humanos',
    'Volume de Negócios Internacioal / Volume de Negócios', 'Volume de Negócios Internacioal / Volume de Negócios', 'Volume de Negócios Internacioal / Volume de Negócios',
    None, 'Ativo Corrente / Passivo Corrente', 'Ativo Corrente / Passivo Corrente', 'Ativo Corrente / Passivo Corrente', '(Ativo corrente - Inventários) / Passivo Corrente',
    '(Ativo corrente - Inventários) / Passivo Corrente', '(Ativo corrente - Inventários) / Passivo Corrente', 'Caixa e Depósitos Bancários / Passivo Corrente',
    'Caixa e Depósitos Bancários / Passivo Corrente', 'Caixa e Depósitos Bancários / Passivo Corrente', None,'Capital Próprio/Ativo', 'Capital Próprio/Ativo', 'Capital Próprio/Ativo',
    'Passivo/Ativo', 'Passivo/Ativo', 'Passivo/Ativo', 'Ativo/Passivo', 'Ativo/Passivo', 'Ativo/Passivo', 'Financiamento Obtido / (CP+Financiamentos Obtidos)', 'Financiamento Obtido / (CP+Financiamentos Obtidos)',
    'Financiamento Obtido / (CP+Financiamentos Obtidos)', None, '(Ebit - Imposto) / Ativo', '(Ebit - Imposto) / Ativo', '(Ebit - Imposto) / Ativo',
    'Resultado Líquido / Capital Próprio', 'Resultado Líquido / Capital Próprio', 'Resultado Líquido / Capital Próprio']
    
     
    st.session_state.df_comparacao['Entidade'] = [None, 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice'
    , 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', None, 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice'
    , 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice'
    , 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', None, 'Empresa','Média do Setor','Índice'
    , 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', None, 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice'
    , 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice', None, 'Empresa','Média do Setor','Índice', 'Empresa','Média do Setor','Índice'] 
     
    for year in st.session_state.df_demo_resultados.columns[1:]:
        st.session_state.df_comparacao[year] = 0
    
    return st.session_state.df_comparacao
    
    
def fill_comparacao_df():
    rows_empresa= [1,4,7,10,13,17,20,23,26,29,32,35,38,41,45,48,51,55,58,61,64,68,71]
    
    
    
    for year in st.session_state.df_comparacao.columns[3:]:
        st.session_state.df_comparacao.at[2,year] = st.session_state.df_dados_setor_todas.loc[1,year] / st.session_state.df_dados_setor_todas.loc[0,year]
        st.session_state.df_comparacao.at[5,year] = (st.session_state.df_dados_setor_todas.loc[0,year] - st.session_state.df_dados_setor_todas.loc[2,year]) / st.session_state.df_dados_setor_todas.loc[0,year]
        st.session_state.df_comparacao.at[8,year] = st.session_state.df_dados_setor_todas.loc[5,year] / st.session_state.df_dados_setor_todas.loc[0,year]
        st.session_state.df_comparacao.at[11,year] = st.session_state.df_dados_setor_todas.loc[24,year] / 100
        st.session_state.df_comparacao.at[14,year] = st.session_state.df_dados_setor_todas.loc[5,year] / st.session_state.df_dados_setor_todas.loc[6,year]
        st.session_state.df_comparacao.at[18,year] = st.session_state.df_dados_setor_todas.loc[0,year] / st.session_state.df_dados_setor_todas.loc[6,year]
        st.session_state.df_comparacao.at[21,year] = st.session_state.df_dados_setor_todas.loc[3,year] / st.session_state.df_dados_setor_todas.loc[0,year]
        st.session_state.df_comparacao.at[24,year] = st.session_state.df_dados_setor_todas.loc[4,year] / st.session_state.df_dados_setor_todas.loc[0,year]       
        st.session_state.df_comparacao.at[27,year] = st.session_state.df_dados_setor_todas.loc[2,year] / st.session_state.df_dados_setor_todas.loc[0,year]
        st.session_state.df_comparacao.at[30,year] = (st.session_state.df_dados_setor_todas.loc[2,year]+st.session_state.df_dados_setor_todas.loc[3,year]+st.session_state.df_dados_setor_todas.loc[4,year]) / st.session_state.df_dados_setor_todas.loc[0,year]
        st.session_state.df_comparacao.at[33,year] = st.session_state.df_dados_setor_todas.loc[18,year]
        st.session_state.df_comparacao.at[36,year] = st.session_state.df_dados_setor_todas.loc[19,year]
        st.session_state.df_comparacao.at[39,year] = st.session_state.df_dados_setor_todas.loc[22,year] / st.session_state.df_dados_setor_todas.loc[21,year]
        st.session_state.df_comparacao.at[42,year] = st.session_state.df_dados_setor_todas.loc[23,year] 
        st.session_state.df_comparacao.at[46,year] = st.session_state.df_dados_setor_todas.loc[9,year] / st.session_state.df_dados_setor_todas.loc[10,year]
        st.session_state.df_comparacao.at[49,year] = (st.session_state.df_dados_setor_todas.loc[9,year]-st.session_state.df_dados_setor_todas.loc[13,year]) / st.session_state.df_dados_setor_todas.loc[10,year]
        st.session_state.df_comparacao.at[52,year] = st.session_state.df_dados_setor_todas.loc[14,year] / st.session_state.df_dados_setor_todas.loc[10,year]
        st.session_state.df_comparacao.at[56,year] = st.session_state.df_dados_setor_todas.loc[8,year] / st.session_state.df_dados_setor_todas.loc[6,year]
        st.session_state.df_comparacao.at[59,year] = st.session_state.df_dados_setor_todas.loc[7,year] / st.session_state.df_dados_setor_todas.loc[6,year]  
        st.session_state.df_comparacao.at[62,year] = st.session_state.df_dados_setor_todas.loc[6,year] / st.session_state.df_dados_setor_todas.loc[7,year] 
        st.session_state.df_comparacao.at[65,year] = (st.session_state.df_dados_setor_todas.loc[8,year]+st.session_state.df_dados_setor_todas.loc[15,year]) / st.session_state.df_dados_setor_todas.loc[15,year]
        st.session_state.df_comparacao.at[69,year] = (st.session_state.df_dados_setor_todas.loc[20,year]-st.session_state.df_dados_setor_todas.loc[16,year]) / st.session_state.df_dados_setor_todas.loc[6,year]
        st.session_state.df_comparacao.at[72,year] = st.session_state.df_dados_setor_todas.loc[5,year] / st.session_state.df_dados_setor_todas.loc[8,year]
  
        for row in rows_empresa:
            
            st.session_state.df_comparacao.at[row, year] = st.session_state.df_indicadores[st.session_state.df_indicadores['Indicador'] == st.session_state.df_comparacao.at[row, 'Indicador']][year].iloc[0]
            st.session_state.df_comparacao.at[row+2,year] = st.session_state.df_comparacao.at[row,year] / st.session_state.df_comparacao.at[row+1,year] * 100
            
        
    return st.session_state.df_comparacao
 

def normalizar_info_setor(file_path):
    infos_setor = pd.read_excel(file_path, sheet_name = "Portugal", header = 9, usecols="D:K")

    nome_setor = pd.read_excel(file_path, sheet_name = "Portugal", header = 1).iloc[0,3]
    dimensao = pd.read_excel(file_path, sheet_name = "Portugal", header = 1).iloc[2,3]

    #parse da coluna total
    infos_setor["Total"] = infos_setor["Total"].astype("str")
    infos_setor["Total"] = infos_setor["Total"].str.replace(" ", "")
    infos_setor["Total"] = pd.to_numeric(infos_setor["Total"], errors = "coerce")

    #parse da coluna valor médio
    infos_setor["Valor Médio"] = infos_setor["Valor Médio"].astype("str")
    infos_setor["Valor Médio"] = infos_setor["Valor Médio"].str.replace(" ", "")
    infos_setor["Valor Médio"] = pd.to_numeric(infos_setor["Valor Médio"], errors ="coerce")

    #Ajuste unidade de medida da coluna total
    infos_setor["Total"] = np.where(infos_setor["Unidade de Medida"] == "Milhares de euros ", infos_setor["Total"] * 10**3, infos_setor["Total"])

    #Ajuste unidade de medida da coluna valor médio
    infos_setor["Valor Médio"] = np.where(infos_setor["Unidade de Medida"] == "Milhares de euros ", infos_setor["Valor Médio"] * 10**3, infos_setor["Valor Médio"])


    infos_setor = infos_setor.drop(columns = "Unidade de Medida")

    #gera tabela transposta

    pivot_setor = pd.pivot_table(infos_setor, index =  "Rubrica", columns = "Ano")
    pivot_setor = pivot_setor.swaplevel(axis = 1)


    #ordena o índice primeiro de acordo com o ano, depois de cordo com a medida

    index_to_be = list()
    for i in range(2017, infos_setor["Ano"].max() + 1):
        for j in ["Quartil 1", "Mediana", "Quartil 3", "Valor Médio", "Total"]:
            index_to_be.append((i,j))

            
    new_index = pd.MultiIndex.from_tuples(index_to_be)

    pivot_ordered = pd.DataFrame(pivot_setor, columns = new_index)

    pivot_ordered.columns = [" ".join((str(i),str(j))) for i,j in pivot_ordered.columns.values]

    #substitui os nomes das rúbricas utilizadas pelo banco de portugal para a nomenclatura utilizada internamente

    nomes_substituir = {"Vendas e serviços prestados" : "Volume de Negócios",
     "Resultado antes de depreciações, gastos de financiamento e impostos (EBITDA)" :"EBITDA",
     "Custo das mercadorias vendidas e das matérias consumidas" : "CMVMC", 
     "Fornecimentos e serviços externos": "FSE",
     "Resultado líquido do período" : "Resultados Líquidos",
     "Inventários e ativos biológicos consumíveis": "Inventários",
     "Imposto sobre o rendimento do período" : "Imposto",
     "Gastos com o pessoal" : "Gastos com Pessoal",
     "Resultado antes de gastos de financiamento e impostos (EBIT)" : "EBIT",
     "EBITDA em percentagem do volume de negócios ":"Margem Operacional",
     "Margem líquida em percentagem dos rendimentos" : "Margem líquida",
     "Rendibilidade do ativo": "Rentabilidade do ativo",
     "Rendibilidade dos capitais próprios": "Rentabilidade do Capital Próprio"}
       
          
    for i in nomes_substituir.keys():           
        as_list = pivot_ordered.index.tolist()
        idx = as_list.index(i)
        as_list[idx] = nomes_substituir[i]
        pivot_ordered.index = as_list

    
    #gera o título da tabela, com o nome do setor
    pivot_ordered.index.names = [nome_setor[29:].strip() + "; " + dimensao[20:].strip()]
    
    return pivot_ordered






    
##############################MAIN############################

st.markdown("### Demonstração Resultados, Balanço & Indicadores")
uploaded_file = st.file_uploader("Selecionar ficheiro Indicadores Macros")
uploaded_file = "C:\\Users\\Bruno\\OneDrive\\Ambiente de Trabalho\\STREAM\\dashboard-tool\\Indicadores_macros_backup_2606 .xlsb.xlsm"
if uploaded_file is not None:

    st.session_state.df_demo_resultados = pd.read_excel(uploaded_file, sheet_name="Demonstração de Resultados", skiprows=3)
    st.session_state.df_demo_resultados = st.session_state.df_demo_resultados.iloc[:,1:]
    
    st.session_state.df_balanco = pd.read_excel(uploaded_file, sheet_name="Balanço", skiprows=3)
    st.session_state.df_balanco = st.session_state.df_balanco.iloc[:,1:]
    
    st.session_state.df_indicadores = pd.read_excel(uploaded_file, sheet_name="Indicadores", skiprows=2)
     
    st.session_state.df_demo_resultados = calc_demo_resultados_df()
    
    st.session_state.df_balanco = calc_balanco_df() 
    
    st.session_state.df_indicadores = calc_indicadores_df()
     

    with st.expander("Indicadores"):
        st.write(st.session_state.df_indicadores)
    
    with st.expander("Demonstração Resultados"):
        
        st.write(st.session_state.df_demo_resultados)
         
    with st.expander("Balanço"):
        st.write(st.session_state.df_balanco)


st.markdown("### Dados do Setor")        
st.markdown("##### Todas as Dimensões")   
uploaded_file_todas_dimen = st.file_uploader("Selecionar ficheiro <Todas as dimensões>")

uploaded_file_todas_dimen = "C:\\Users\\Bruno\\OneDrive\\Ambiente de Trabalho\\STREAM\\dashboard-tool\\RelatorioQS.xls"

if uploaded_file_todas_dimen is not None:
    st.session_state.df_todas_dimen = normalizar_info_setor(uploaded_file_todas_dimen)
    with st.expander("Todas as Dimensões"):
        st.write(st.session_state.df_todas_dimen)
        

st.markdown("##### Dimensão Aplicável")
uploaded_file_varias_dimen = st.file_uploader("Selecionar ficheiro <Micro, Pequena, Média ou Grande dimensões>")  

uploaded_file_varias_dimen = "C:\\Users\\Bruno\\OneDrive\\Ambiente de Trabalho\\STREAM\\dashboard-tool\\RelatorioQS_micro.xls"

if uploaded_file_varias_dimen is not None:
    st.session_state.df_dimen_aplicavel = normalizar_info_setor(uploaded_file_varias_dimen)
    with st.expander("Dimensão Aplicável"):
        st.write(st.session_state.df_dimen_aplicavel)
    
    
if uploaded_file_todas_dimen and uploaded_file_varias_dimen is not None:
    st.markdown("##### Dados") # mudar para outro nome ou então mudar o capitulo de cima
    st.session_state.df_dados_setor_todas = create_dados_setor_df()
    
    for year in st.session_state.df_dados_setor_todas.columns[1:]:
    
        my_range = [x for x in range(len(st.session_state.df_dados_setor_todas)) if x not in [17, 23]]

        

        for row in my_range: 
            st.session_state.df_dados_setor_todas.at[row,year] = st.session_state.df_todas_dimen.loc[st.session_state.df_dados_setor_todas.loc[row,'Rúbricas'], str(year)+' Valor Médio']
        
        st.session_state.df_dados_setor_todas.at[17,year] = 123 #perguntar Taxa de VAB na CAE
        st.session_state.df_dados_setor_todas.at[23,year] = st.session_state.df_todas_dimen.loc['Vendas e serviços prestados no mercado externo',str(year)+' Total'] / st.session_state.df_todas_dimen.loc['Volume de Negócios',str(year)+' Total']
        
    with st.expander("Dados do Setor - Todas as dimensões"):
        st.write(st.session_state.df_dados_setor_todas)
        
    
    
    st.session_state.df_dados_setor_aplicavel = create_dados_setor_df()
    for year in st.session_state.df_dados_setor_aplicavel.columns[1:]:
    
        my_range = [x for x in range(len(st.session_state.df_dados_setor_aplicavel)) if x not in [17, 23,24]]

        for row in my_range: 
            st.session_state.df_dados_setor_aplicavel.at[row,year] = st.session_state.df_dimen_aplicavel.loc[st.session_state.df_dados_setor_aplicavel.loc[row,'Rúbricas'], str(year)+' Valor Médio']
        
        st.session_state.df_dados_setor_aplicavel.at[17,year] = 123 #perguntar Taxa de VAB na CAE
        st.session_state.df_dados_setor_aplicavel.at[23,year] = st.session_state.df_dimen_aplicavel.loc['Vendas e serviços prestados no mercado externo',str(year)+' Total'] / st.session_state.df_dimen_aplicavel.loc['Volume de Negócios',str(year)+' Total']
        st.session_state.df_dados_setor_aplicavel.at[24,year] = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção',str(year)+' Valor Médio'] / 100
    with st.expander("Dados do Setor - Dimensão aplicável"):
        st.write(st.session_state.df_dados_setor_aplicavel)
        
        

    st.session_state.df_quartis_todas = create_quartis_df()
    
    for year in st.session_state.df_quartis_todas.columns[2:]:
        for row in range(0,len(st.session_state.df_quartis_todas)): 
                st.session_state.df_quartis_todas.at[row,year] = st.session_state.df_todas_dimen.loc[st.session_state.df_quartis_todas.loc[row,'Indicadores'], str(year)+' '+st.session_state.df_quartis_todas.loc[row,'Quartil']] / 100
    
    with st.expander("Dados do Setor - Quartis - Todas as dimensões"):
        st.write(st.session_state.df_quartis_todas)
        
              
    st.session_state.df_quartis_varias = create_quartis_df()  
    
    for year in st.session_state.df_quartis_varias.columns[2:]:
        for row in range(0,len(st.session_state.df_quartis_varias)): 
                st.session_state.df_quartis_varias.at[row,year] = st.session_state.df_dimen_aplicavel.loc[st.session_state.df_quartis_varias.loc[row,'Indicadores'], str(year)+' '+st.session_state.df_quartis_varias.loc[row,'Quartil']] / 100
    
    with st.expander("Dados do Setor - Quartis - Dimensão aplicável"):
        st.write(st.session_state.df_quartis_varias)
        
        
if uploaded_file_todas_dimen and uploaded_file_varias_dimen and uploaded_file is not None:        
    st.markdown('### Comparação')    
    st.session_state.df_comparacao = create_comparacao_df()
    
    fill_comparacao_df()
    
    with st.expander("Comparação"):
        st.data_editor(st.session_state.df_comparacao)
        
                
