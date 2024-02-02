# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:39:50 2023

@author: STREAM
"""

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog


#%% caixa de diálogo
#abre caixa de diálogo e busca o nome do arquivo

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

#%% import e limpeza

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

#%% transpõe

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

#%%

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

#copia a tabela para o clipboard

pivot_ordered.to_clipboard(excel = True)



#%%

