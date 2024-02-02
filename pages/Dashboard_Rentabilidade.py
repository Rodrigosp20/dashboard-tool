import time
import numpy as np
import pandas as pd
import plotly.express as px  # pip install plotly
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import math


st.set_page_config(
    page_title="Dashboard Rentabilidade",
    page_icon="📈",
    layout="wide",
)

def create_gauge(empresa,quartil_1,mediana,quartil_3):
    if empresa == 0:
        st.image('0.png',use_column_width = True)
    elif empresa<quartil_1:
        fraco()
    elif empresa >= quartil_1 and empresa < mediana:
        mod_fraco()
    elif empresa >= mediana and empresa < quartil_3:
        mod_forte()
    elif empresa >= quartil_3:
        forte()
    else:
        st.image('nan.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Dados Indisponíveis</p>', unsafe_allow_html=True)
        

if 'df_comparacao' and 'df_demo_resultados' and 'df_balanco' and 'df_indicadores' in st.session_state: # melhorar este if
    
    
    ##############################DASHBOARD RENTABILIDADE############################
    st.markdown("## Dashboard Rentabilidade")
    
    col1_logo, col2_text = st.columns(2)
    col1,col2,col3,col4,col5 = st.columns(5)
    
    st.markdown("""
    <style>
    .title-font {
        font-size:40px !important;
        text-align: center;
    }
    .header-font {
        font-size:30px !important;
        text-align: center;
    }
    .sub_header-font {
        font-size:20px !important;
        text-align: center;
    }
    .text-font {
        font-size:11px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    def fraco():
        st.image('low.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Fraco</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Em comparação com o setor,  o desempenho da empresa no último ano da comparação foi fraco, figurando entre as 25% piores da mesma dimensão.</p>', unsafe_allow_html=True)
    
    def mod_fraco():
        st.image('mod_low.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Moderadamente Fraco</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Em comparação com o setor,  o desempenho da empresa no último ano da comparação foi moderadamente fraco, figurando entre as 50% piores da mesma dimensão.</p>', unsafe_allow_html=True)
    
    def mod_forte():
        st.image('mod_high.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Moderadamente Forte</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Em comparação com o setor,  o desempenho da empresa no último ano da comparação foi moderadamente forte, figurando entre as 50% melhores da mesma dimensão.</p>', unsafe_allow_html=True)
    
    
    def forte():
        st.image('high.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Forte</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Em comparação com o setor,  o desempenho da empresa no último ano da comparação foi forte, figurando entre as 25% melhores da mesma dimensão.</p>', unsafe_allow_html=True)
    
    
    with col1_logo:
        st.image('logo1.png', width=300,use_column_width=True)
    
    with col2_text:
        st.markdown('<p class="header-font">Comparação Setorial</p>', unsafe_allow_html=True)
        st.markdown('<p class="title-font">Rentabilidade de negócio</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub_header-font">Qual é a lucratividade do meu negócio, comparado ao setor?</p>', unsafe_allow_html=True)
        st.divider()
    
    with col1:
    
        st.markdown('<p class="sub_header-font">Margem Operacional</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Qual é a eficiência com a qual a empresa gere suas despesas operacionais em relação a receita?</p>', unsafe_allow_html=True)
        years_graph = list(range(st.session_state.df_comparacao.columns[3],st.session_state.df_comparacao.columns[-1]+1))

        margem_operacional_values_graph = st.session_state.df_comparacao.loc[1, st.session_state.df_comparacao.columns[3:]]  
        media_margem_operacional_todos_values_graph = st.session_state.df_comparacao.loc[2, st.session_state.df_comparacao.columns[3:]]
        media_margem_operacional_aplicavel_values_graph = st.session_state.df_dados_setor_aplicavel.loc[1,st.session_state.df_dados_setor_aplicavel.columns[1:]] / st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]
        

        margem_operacional = go.Figure()

        margem_operacional.add_trace(go.Scatter(x=years_graph, y=media_margem_operacional_todos_values_graph, name="Média do Setor - Todas as Dimensões",line=dict(color='#67738f', width=4)))
        margem_operacional.add_trace(go.Scatter(x=years_graph, y=media_margem_operacional_aplicavel_values_graph, name="Média do Setor - Dimensão Aplicável",line=dict(color='#959fb8', width=4)))
        margem_operacional.add_trace(go.Bar(x=years_graph, y=margem_operacional_values_graph,name="Empresa", marker=dict(color='#192646')))
        
        margem_operacional.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=years_graph,
                ticktext=[str(year) for year in years_graph]
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(margem_operacional,use_container_width=True)
        
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_margem_operacional = st.session_state.df_comparacao.loc[1,st.session_state.df_comparacao.columns[-1]]*100
        quartil_1_margem_operacional = st.session_state.df_dimen_aplicavel.loc['Margem Operacional',str(st.session_state.df_comparacao.columns[-1])+' Quartil 1']
        mediana_margem_operacional = st.session_state.df_dimen_aplicavel.loc['Margem Operacional',str(st.session_state.df_comparacao.columns[-1])+' Mediana']
        quartil_3_margem_operacional = st.session_state.df_dimen_aplicavel.loc['Margem Operacional',str(st.session_state.df_comparacao.columns[-1])+' Quartil 3']
        
        
        create_gauge(gauge_empresa_margem_operacional,quartil_1_margem_operacional,mediana_margem_operacional,quartil_3_margem_operacional)
        
        
    with col2:
        st.markdown('<p class="sub_header-font">Margem Bruta</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Qual é o lucro obtido após subtrairem-se os custos de produção?</p>', unsafe_allow_html=True)
        
        margem_bruta_values_graph = st.session_state.df_comparacao.loc[4, st.session_state.df_comparacao.columns[3:]] 
        media_margem_bruta_todos_values_graph = st.session_state.df_comparacao.loc[5, st.session_state.df_comparacao.columns[3:]]
        media_margem_bruta_aplicavel_values_graph = (st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]-st.session_state.df_dados_setor_aplicavel.loc[2,st.session_state.df_dados_setor_aplicavel.columns[1:]]) / st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]
        

        margem_bruta = go.Figure()

        margem_bruta.add_trace(go.Scatter(x=years_graph, y=media_margem_bruta_todos_values_graph, name="Média do Setor - Todas as Dimensões",line=dict(color='#67738f', width=4)))
        margem_bruta.add_trace(go.Scatter(x=years_graph, y=media_margem_bruta_aplicavel_values_graph, name="Média do Setor - Dimensão Aplicável",line=dict(color='#959fb8', width=4)))
        margem_bruta.add_trace(go.Bar(x=years_graph, y=margem_bruta_values_graph,name="Empresa", marker=dict(color='#192646')))
        
        margem_bruta.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=years_graph,
                ticktext=[str(year) for year in years_graph]
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(margem_bruta,use_container_width=True)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_margem_bruta = st.session_state.df_comparacao.loc[4,st.session_state.df_comparacao.columns[-1]]*100
        quartil_1_margem_bruta = st.session_state.df_dimen_aplicavel.loc['Margem bruta',str(st.session_state.df_comparacao.columns[-1])+' Quartil 1']
        mediana_margem_bruta = st.session_state.df_dimen_aplicavel.loc['Margem bruta',str(st.session_state.df_comparacao.columns[-1])+' Mediana']
        quartil_3_margem_bruta = st.session_state.df_dimen_aplicavel.loc['Margem bruta',str(st.session_state.df_comparacao.columns[-1])+' Quartil 3']
            
            
        create_gauge(gauge_empresa_margem_bruta,quartil_1_margem_bruta,mediana_margem_bruta,quartil_3_margem_bruta)
        
                
    with col3:
        st.markdown('<p class="sub_header-font">Margem Líquida</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Qual é a lucratividade líquida do negócio?</p>', unsafe_allow_html=True)

        margem_liquida_values_graph = st.session_state.df_comparacao.loc[7, st.session_state.df_comparacao.columns[3:]] 
        media_margem_liquida_todos_values_graph = st.session_state.df_comparacao.loc[8, st.session_state.df_comparacao.columns[3:]]
        media_margem_liquida_aplicavel_values_graph = st.session_state.df_dados_setor_aplicavel.loc[5,st.session_state.df_dados_setor_aplicavel.columns[1:]] / st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]
        
        st.write("")
        margem_liquida = go.Figure()

        margem_liquida.add_trace(go.Scatter(x=years_graph, y=media_margem_liquida_todos_values_graph, name="Média do Setor - Todas as Dimensões",line=dict(color='#67738f', width=4)))
        margem_liquida.add_trace(go.Scatter(x=years_graph, y=media_margem_liquida_aplicavel_values_graph, name="Média do Setor - Dimensão Aplicável",line=dict(color='#959fb8', width=4)))
        margem_liquida.add_trace(go.Bar(x=years_graph, y=margem_liquida_values_graph,name="Empresa", marker=dict(color='#192646')))
        
        margem_liquida.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=years_graph,
                ticktext=[str(year) for year in years_graph]
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(margem_liquida,use_container_width=True)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_margem_liquida = st.session_state.df_comparacao.loc[7,st.session_state.df_comparacao.columns[-1]]*100
        quartil_1_margem_liquida = st.session_state.df_dimen_aplicavel.loc['Margem líquida',str(st.session_state.df_comparacao.columns[-1])+' Quartil 1']
        mediana_margem_liquida = st.session_state.df_dimen_aplicavel.loc['Margem líquida',str(st.session_state.df_comparacao.columns[-1])+' Mediana']
        quartil_3_margem_liquida = st.session_state.df_dimen_aplicavel.loc['Margem líquida',str(st.session_state.df_comparacao.columns[-1])+' Quartil 3']
          
        
        create_gauge(gauge_empresa_margem_liquida,quartil_1_margem_liquida,mediana_margem_liquida,quartil_3_margem_liquida)
        
        
    with col4:
        st.markdown('<p class="sub_header-font">Nivel de Valor Acrescentado</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Quanto valor adicional a empresa cria em relação aos custos de produção?</p>', unsafe_allow_html=True)
        
        valor_acresc_values_graph = st.session_state.df_comparacao.loc[10, st.session_state.df_comparacao.columns[3:]] 
        media_valor_acresc_todos_values_graph = st.session_state.df_comparacao.loc[11, st.session_state.df_comparacao.columns[3:]]
        media_valor_acresc_aplicavel_values_graph = st.session_state.df_dados_setor_aplicavel.loc[24, st.session_state.df_comparacao.columns[3:]]
        

        valor_acresc = go.Figure()

        valor_acresc.add_trace(go.Scatter(x=years_graph, y=media_valor_acresc_todos_values_graph, name="Média do Setor - Todas as Dimensões",line=dict(color='#67738f', width=4)))
        valor_acresc.add_trace(go.Scatter(x=years_graph, y=media_valor_acresc_aplicavel_values_graph, name="Média do Setor - Dimensão Aplicável",line=dict(color='#959fb8', width=4)))
        valor_acresc.add_trace(go.Bar(x=years_graph, y=valor_acresc_values_graph,name="Empresa", marker=dict(color='#192646')))
        
        valor_acresc.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=years_graph,
                ticktext=[str(year) for year in years_graph]
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(valor_acresc,use_container_width=True)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_valor_acresc = st.session_state.df_comparacao.loc[10,st.session_state.df_comparacao.columns[-1]]*100
        quartil_1_valor_acresc = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção', str(st.session_state.df_comparacao.columns[-1])+' Quartil 1']
        mediana_valor_acresc = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção', str(st.session_state.df_comparacao.columns[-1])+' Mediana']
        quartil_3_valor_acresc = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção', str(st.session_state.df_comparacao.columns[-1])+' Quartil 3']
       
        
        create_gauge(gauge_empresa_valor_acresc,quartil_1_valor_acresc,mediana_valor_acresc,quartil_3_valor_acresc)
        
        
    with col5:
        st.markdown('<p class="sub_header-font">Rentabilidade do Ativo</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Quão eficientemente a empresa utiliza seus ativos para gerar lucro?</p>', unsafe_allow_html=True)
        
        rent_ativo_values_graph = st.session_state.df_comparacao.loc[13, st.session_state.df_comparacao.columns[3:]] 
        

        media_rent_ativo_aplicavel_values_graph = []
        media_rent_ativo_todos_values_graph = []
        for year in years_graph:
            media_rent_ativo_todos_values_graph.append(st.session_state.df_todas_dimen.loc['Rentabilidade do ativo', str(year)+' Valor Médio']/100)
            media_rent_ativo_aplicavel_values_graph.append(st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo', str(year)+' Valor Médio']/100)


        rent_ativo = go.Figure()

        rent_ativo.add_trace(go.Scatter(x=years_graph, y=media_rent_ativo_todos_values_graph, name="Média do Setor - Todas as Dimensões",line=dict(color='#67738f', width=4)))
        rent_ativo.add_trace(go.Scatter(x=years_graph, y=media_rent_ativo_aplicavel_values_graph, name="Média do Setor - Dimensão Aplicável",line=dict(color='#959fb8', width=4)))
        rent_ativo.add_trace(go.Bar(x=years_graph, y=rent_ativo_values_graph,name="Empresa", marker=dict(color='#192646')))
        
        rent_ativo.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=years_graph,
                ticktext=[str(year) for year in years_graph]
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(rent_ativo,use_container_width=True)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_rent_ativo = st.session_state.df_comparacao.loc[13,st.session_state.df_comparacao.columns[-1]]*100
        quartil_1_rent_ativo = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo',str(st.session_state.df_comparacao.columns[-1])+' Quartil 1']
        mediana_rent_ativo = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo',str(st.session_state.df_comparacao.columns[-1])+' Mediana']
        quartil_3_rent_ativo = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo',str(st.session_state.df_comparacao.columns[-1])+' Quartil 3']
        
        create_gauge(gauge_empresa_rent_ativo,quartil_1_rent_ativo,mediana_rent_ativo,quartil_3_rent_ativo)

else:
    st.write('Carregar ficheiros primeiro')