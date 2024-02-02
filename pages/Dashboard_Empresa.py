import time
import numpy as np
import pandas as pd
import plotly.express as px  # pip install plotly
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import math
import time
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from xhtml2pdf import pisa # pip install xhtml2pdf
from matplotlib.backends.backend_pdf import PdfPages
import pyautogui
from playwright.sync_api import Page, expect
import keyboard


st.set_page_config(
    page_title="Dashboard Empresa",
    page_icon="📈",
    layout="wide",
)

hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
        
allow_scroll = """
            <style>
                .stApp{ position: relative !important;}
                .appview-container{ position: relative !important;}
            </style>
            """
            
st.markdown(allow_scroll, unsafe_allow_html=True)
        
st.markdown(hide_img_fs, unsafe_allow_html=True)



def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err
    
if 'df_comparacao' in st.session_state: # melhorar este if
    
    
    ##############################DASHBOARD EMPRESA############################
    st.markdown("# Dashboard Empresa")
    
    
    
    left_col, right_col = st.columns([1, 1])
    years_graph = list(range(st.session_state.df_comparacao.columns[3],st.session_state.df_comparacao.columns[-1]+1))
    
    with left_col:
        
        column_1, column_2 = st.columns(2)
        
        st.image('logo1.png', use_column_width=True)
            
        with column_1:
            ### MARGEM OPERACIONAL

            margem_operacional = go.Figure()

            year_slider = st.sidebar.slider(
                "Selecionar os anos:",
                min_value=int(min(years_graph)),
                max_value=int(max(years_graph)),
                value=(int(min(years_graph)), int(max(years_graph))),
                step=1
            )
            
            range_years = list(range(year_slider[0],year_slider[1]+1,1))
            margem_operacional_values_graph = st.session_state.df_comparacao.loc[1, year_slider[0]:year_slider[1]]
            
            # margem_operacional_fig, margem_operacional_ax = plt.subplots(figsize=(13, 11))
            margem_operacional.add_trace(go.Bar(x=range_years, y=margem_operacional_values_graph,marker=dict(color='#192646')))
            
            # margem_operacional_ax.bar(range_years,margem_operacional_values_graph,color="#192646")
            # margem_operacional_ax.set_title('Margem Operacional', fontsize=50)
            # margem_operacional_ax.tick_params(axis='both', labelsize=35)
            # margem_operacional_ax.spines['top'].set_visible(False)
            # margem_operacional_ax.spines['right'].set_visible(False)
            # margem_operacional_ax.spines['bottom'].set_visible(False)
            # margem_operacional_ax.spines['left'].set_visible(False)
            # st.pyplot(margem_operacional_fig)
            
            
            margem_operacional.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                title = "Margem Operacional",
                height= 300,
                showlegend=False
            )

            st.plotly_chart(margem_operacional,use_container_width=True)


            ### RENTABILIDADE DO CAPITAL PRÓPRIO
            rent_capital_proprio_values_graph = st.session_state.df_comparacao.loc[71, year_slider[0]:year_slider[1]]

            # rent_capital_proprio_fig, rent_capital_proprio_ax = plt.subplots(figsize=(13, 11))
            
            # rent_capital_proprio_ax.bar(range_years,rent_capital_proprio_values_graph,color="#192646")
            # rent_capital_proprio_ax.set_title('Rentabilidade do Capital Próprio', fontsize=45)
            # rent_capital_proprio_ax.tick_params(axis='both', labelsize=35)
            # rent_capital_proprio_ax.spines['top'].set_visible(False)
            # rent_capital_proprio_ax.spines['right'].set_visible(False)
            # rent_capital_proprio_ax.spines['bottom'].set_visible(False)
            # rent_capital_proprio_ax.spines['left'].set_visible(False)
            # st.pyplot(rent_capital_proprio_fig)
            


            rent_capital_proprio = go.Figure()

            rent_capital_proprio.add_trace(go.Bar(x=range_years, y=rent_capital_proprio_values_graph,marker=dict(color='#192646')))
            
            rent_capital_proprio.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                title = "Rentabilidade do Capital Próprio",
                height= 300,
                showlegend=False
            )

            st.plotly_chart(rent_capital_proprio,use_container_width=True)
            
            ### LIQUIDEZ GERAL
            
            liquidez_geral_values_graph = st.session_state.df_comparacao.loc[45, year_slider[0]:year_slider[1]]
            
            # liquidez_geral_fig,  liquidez_geral_ax = plt.subplots(figsize=(13, 11))
            
            # liquidez_geral_ax.bar(range_years,liquidez_geral_values_graph,color="#192646")
            # liquidez_geral_ax.set_title('Liquidez Geral', fontsize=45)
            # liquidez_geral_ax.tick_params(axis='both', labelsize=35)
            # liquidez_geral_ax.spines['top'].set_visible(False)
            # liquidez_geral_ax.spines['right'].set_visible(False)
            # liquidez_geral_ax.spines['bottom'].set_visible(False)
            # liquidez_geral_ax.spines['left'].set_visible(False)
            # st.pyplot(liquidez_geral_fig)

            liquidez_geral = go.Figure()

            liquidez_geral.add_trace(go.Bar(x=range_years, y=liquidez_geral_values_graph,marker=dict(color='#192646')))
            
            liquidez_geral.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                title = "Liquidez Geral",
                height= 300,
                showlegend=False
            )

            st.plotly_chart(liquidez_geral,use_container_width=True)
        
        with column_2:
            ### LIQUIDEZ REDUZIDA

            liquidez_reduzida_values_graph = st.session_state.df_comparacao.loc[48, year_slider[0]:year_slider[1]]

            # liquidez_reduzida_fig,  liquidez_reduzida_ax = plt.subplots(figsize=(13, 11))
            
            # liquidez_reduzida_ax.bar(range_years,liquidez_reduzida_values_graph,color="#192646")
            # liquidez_reduzida_ax.set_title('Liquidez Reduzida', fontsize=45)
            # liquidez_reduzida_ax.tick_params(axis='both', labelsize=35)
            # liquidez_reduzida_ax.spines['top'].set_visible(False)
            # liquidez_reduzida_ax.spines['right'].set_visible(False)
            # liquidez_reduzida_ax.spines['bottom'].set_visible(False)
            # liquidez_reduzida_ax.spines['left'].set_visible(False)
            # st.pyplot(liquidez_reduzida_fig)

            liquidez_reduzida = go.Figure()

            liquidez_reduzida.add_trace(go.Bar(x=range_years, y=liquidez_reduzida_values_graph,marker=dict(color='#192646')))
            
            liquidez_reduzida.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                title = "Liquidez Reduzida",
                height= 300,
                showlegend=False
            )

            st.plotly_chart(liquidez_reduzida,use_container_width=True)
            
            ### AUTONOMIA FINANCEIRA
            
            autonomia_financeira_values_graph = st.session_state.df_comparacao.loc[55, year_slider[0]:year_slider[1]]
            
            # autonomia_financeira_fig,  autonomia_financeira_ax = plt.subplots(figsize=(13, 11))
            
            # autonomia_financeira_ax.bar(range_years,autonomia_financeira_values_graph,color="#192646")
            # autonomia_financeira_ax.set_title('Autonomia Financeira', fontsize=45)
            # autonomia_financeira_ax.tick_params(axis='both', labelsize=35)
            # autonomia_financeira_ax.spines['top'].set_visible(False)
            # autonomia_financeira_ax.spines['right'].set_visible(False)
            # autonomia_financeira_ax.spines['bottom'].set_visible(False)
            # autonomia_financeira_ax.spines['left'].set_visible(False)
            # st.pyplot(autonomia_financeira_fig)
            
            autonomia_financeira = go.Figure()

            autonomia_financeira.add_trace(go.Bar(x=list(range(year_slider[0],year_slider[1]+1,1)), y=autonomia_financeira_values_graph,marker=dict(color='#192646')))
            
            autonomia_financeira.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                title = "Autonomia Financeira",
                height= 300,
                showlegend=False
            )

            st.plotly_chart(autonomia_financeira,use_container_width=True)

            ### ALAVANCAGEM FINANCEIRA
                        
            alavancagem_financeira_values_graph = st.session_state.df_comparacao.loc[64, year_slider[0]:year_slider[1]]

            # alavancagem_financeira_fig,  alavancagem_financeira_ax = plt.subplots(figsize=(13, 11))
            
            # alavancagem_financeira_ax.bar(range_years,alavancagem_financeira_values_graph,color="#192646")
            # alavancagem_financeira_ax.set_title('Alavancagem Financeira', fontsize=45)
            # alavancagem_financeira_ax.tick_params(axis='both', labelsize=35)
            # alavancagem_financeira_ax.spines['top'].set_visible(False)
            # alavancagem_financeira_ax.spines['right'].set_visible(False)
            # alavancagem_financeira_ax.spines['bottom'].set_visible(False)
            # alavancagem_financeira_ax.spines['left'].set_visible(False)
            # st.pyplot(alavancagem_financeira_fig)

            alavancagem_financeira = go.Figure()

            alavancagem_financeira.add_trace(go.Bar(x=range_years, y=alavancagem_financeira_values_graph,marker=dict(color='#192646')))
            
            alavancagem_financeira.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                title = "Alavancagem Financeira",
                height= 300,
                showlegend=False
            )

            st.plotly_chart(alavancagem_financeira,use_container_width=True)
        
    with right_col:
        ### Comparação do desempenho de indicadores chave da empresa face ao setor
        
        indice_values_graph = st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Entidade'] == 'Índice', st.session_state.df_comparacao.columns[-1]]
        indicadores_graph=st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Entidade'] == 'Índice', 'Indicador']

        # indice_fig, indice_ax = plt.subplots(figsize=(13, 58))
            
        # indice_ax.barh(indicadores_graph,indice_values_graph,color="#192646")
        # indice_ax.set_title('Comparação do desempenho de indicadores chave da empresa face ao setor', fontsize=45)
        # indice_ax.tick_params(axis='both', labelsize=40, top=True, labeltop=True, bottom=False, labelbottom=False)
        # indice_ax.spines['top'].set_visible(False)
        # indice_ax.spines['right'].set_visible(False)
        # indice_ax.spines['bottom'].set_visible(False)
        # indice_ax.spines['left'].set_visible(False)
        # for index, value in enumerate(indice_values_graph):
            # plt.text(value, index,str(round(value)),fontsize=40)
        # indice_fig.align_labels()
        # st.pyplot(indice_fig)
        
        
        
        indice = go.Figure()
        
        indice.add_trace(go.Bar(x=indice_values_graph, y=indicadores_graph, text=round(indice_values_graph,2), 
        textposition='outside', orientation='h', marker=dict(color='#192646')))
        
        indice.update_layout(
            title = "Comparação do desempenho de indicadores <br> chave da empresa face ao setor",
            title_x=0.3,
            width=900,
            height=1200,
            xaxis=dict(side="top")
        )

        st.plotly_chart(indice,use_container_width=True)

    export_button = st.sidebar.button("Exportar Página PDF")
    
    if export_button:
          
        keyboard.press_and_release('ctrl+shift+s')

        
    
    # tmpfile = BytesIO()
    # indice_fig.savefig(tmpfile, format='png')
    # encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    # dashboard_content = """
      # <!DOCTYPE html>
          # <html lang="en">
          # <head>
              # <meta charset="UTF-8">
              # <meta name="viewport" content="width=device-width, initial-scale=1.0">
              # <link rel="stylesheet" href="style.css">
              # <style>
                # {
                  # box-sizing: border-box;
                # }
                # .column {
                  # float: left;
                  # width: 50%;
                  # padding: 10px;
                # }

                # .row:after {
                  # content: "";
                  # display: table;
                  # clear: both;
                # }
               # </style>
          # </head>
          # <body>

            # <h1>Dashboard Empresa</h1>
            # <div>
                # <img src="logo1.png" width="280" height="140">

            # </div>
            

            # <div class="image-container">
                # """+"<img src=\'data:image/png;base64,{}\' width='400' height='540' padding-left=''>".format(encoded)+"</div></body></html>"
             
    # convert_html_to_pdf(dashboard_content,'dasbhboard.pdf')

        
else:
    st.write('Carregar ficheiros primeiro')