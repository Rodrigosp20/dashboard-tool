import time
import numpy as np
import pandas as pd  
import plotly.express as px  # pip install plotly
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import streamlit.components.v1 as components
import math
import statistics

st.set_page_config(
    page_title="Dashboard Rentabilidade",
    page_icon="📈",
    layout="wide",
)


if 'df_comparacao' and 'df_demo_resultados' and 'df_balanco' and 'df_indicadores' in st.session_state: # melhorar este if
    
    option = st.sidebar.selectbox('Escolher Indicador',('Margem Bruta', 'Margem Operacional', 'Margem Líquida',
    'Rentabilidade do Ativo', 'Nível de Valor Acrescentado','Liquidez Geral','Liquidez Reduzida','Liquidez imediata','Autonomia Financeira','Endividamento','Solvabilidade',
    'Alavancagem Financeira','Rentabilidade do Capital Investido','Rentabilidade do Capital Próprio','Turnover do Ativo','% Rh no Volume de Negócios',
    '% FSE no Volume de Negócios','% CMVMC / Volume de negócios','% Custos no Volume de Negócios','Prazo Médio de Pagamentos','Prazo Médio de Recebimentos'))
    
    option_comparacao_varias = {'Margem Bruta': 'Margem bruta',
    'Margem Operacional':'Margem Operacional',
    'Margem Líquida':'Margem líquida',
    'Rentabilidade do Ativo':'Rentabilidade do ativo',
    'Liquidez Geral':'Liquidez geral',
    'Liquidez Reduzida':'Liquidez reduzida',
    'Autonomia Financeira':'Autonomia financeira',
    'Rentabilidade do Capital Próprio':'Rentabilidade do Capital Próprio',
    'Prazo Médio de Pagamentos':'Prazo médio de pagamentos',
    'Prazo Médio de Recebimentos':'Prazo médio de recebimentos',
    }
    

    st.markdown("## Dashboard Rentabilidade - "+option.title())
    
    col1_logo, col2_text = st.columns(2)
    
    col1_mid, col2_mid = st.columns([1, 3])
    col1_bot, col2_bot = st.columns([2, 1],gap="large")
    
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
    
    def mod_fraco():
        st.image('mod_low.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Moderadamente Fraco</p>', unsafe_allow_html=True)
    
    def mod_forte():
        st.image('mod_high.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Moderadamente Forte</p>', unsafe_allow_html=True)    
    
    def forte():
        st.image('high.png',use_column_width = True)
        st.markdown('<p class="sub_header-font">Forte</p>', unsafe_allow_html=True)
        
    def medias_per_year():
        media_quartil_1 = 0
        media_mediana = 0
        media_quartil_3 = 0
        flag_year = 0
        for year in st.session_state.df_comparacao.columns[3:]:
            
            if(option=='Liquidez imediata'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Passivo corrente', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Mediana'] / st.session_state.df_todas_dimen.loc['Passivo corrente', str(year) + ' Quartil 1']
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Passivo corrente', str(year) + ' Quartil 1']
                flag_year += 1
            elif(option=='Endividamento'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'] 
                media_mediana += st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Mediana'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'] 
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1']
                flag_year += 1
            elif(option=='Solvabilidade'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'] 
                media_mediana += st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Mediana'] / st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'] 
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1']
                flag_year += 1
            elif(option=='Alavancagem Financeira'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 1'] / (st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 1'] + st.session_state.df_todas_dimen.loc['Capital próprio', str(year) + ' Quartil 1'])
                media_mediana += st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Mediana'] / (st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Mediana'] + st.session_state.df_todas_dimen.loc['Capital próprio', str(year) + ' Mediana'])
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 3'] / (st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 3'] + st.session_state.df_todas_dimen.loc['Capital próprio', str(year) + ' Quartil 3'])
                media_gauge_empresa = media_gauge_empresa * 100
                flag_year += 1
            elif(option == 'Rentabilidade do Capital Investido'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += (st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Quartil 1'] - st.session_state.df_todas_dimen.loc['Imposto', str(year) + ' Quartil 1']) / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1']
                media_mediana += (st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Mediana'] - st.session_state.df_todas_dimen.loc['Imposto', str(year) + ' Mediana']) / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Mediana'] 
                media_quartil_3 += (st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Quartil 3'] - st.session_state.df_todas_dimen.loc['Imposto', str(year) + ' Quartil 3']) / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 3']
                flag_year += 1
            elif(option == 'Nível de Valor Acrescentado'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Quartil 1'] / 100
                media_mediana += st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Mediana'] / 100
                media_quartil_3 += st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Quartil 3'] / 100
                flag_year += 1
            elif(option == 'Turnover do Ativo'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Ativo', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Ativo', str(year) + ' Quartil 3']
                flag_year += 1
            elif(option == '% Rh no Volume de Negócios'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(option == '% FSE no Volume de Negócios'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(option == '% CMVMC / Volume de negócios'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(option == '% Custos no Volume de Negócios'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1']) and np.isnan(st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1']) and np.isnan(st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += (st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1']+st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1']+st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1']) / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += (st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Mediana']+st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Mediana']+st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Mediana']) / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += (st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Quartil 3']+st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Quartil 3']+st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Quartil 3']) / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            else:
                if(np.isnan(st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(option), str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(option), str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(option),str(year)+' Mediana']
                media_quartil_3 += st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(option),str(year)+' Quartil 3']
                flag_year += 1
                
        media_quartil_1 = media_quartil_1 / (flag_year if not flag_year == 0 else 1)
        media_mediana = media_mediana / (flag_year if not flag_year == 0 else 1)
        media_quartil_3 = media_quartil_3 / (flag_year if not flag_year == 0 else 1)
                
        return media_quartil_1, media_mediana, media_quartil_3, flag_year
     
    with col1_logo:
        st.image('logo1.png', width=300, use_column_width=True)
        
    
    with col2_text:
        st.markdown('<p class="title-font">Rentabilidade de negócio</p>', unsafe_allow_html=True)
        
        
        st.markdown('<p class="sub_header-font">'+option+'</p>', unsafe_allow_html=True)
        st.divider()
        
    with col1_mid:
        st.markdown('<p class="sub_header-font">Desempenho agregado nos anos avaliados</p>', unsafe_allow_html=True)

        media_gauge_empresa = statistics.mean(st.session_state.df_comparacao.loc[st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Indicador'] == option].index[0], st.session_state.df_comparacao.columns[3:]])*100
        
        media_quartil_1, media_mediana, media_quartil_3, flag_year = medias_per_year()
        
        
        st.write("")
        st.write("")
        
        if media_gauge_empresa == 0:
            st.image('0.png',use_column_width = True)
        elif media_quartil_1 == 0 and media_mediana == 0 and media_quartil_3 == 0:
            st.image('nan.png',use_column_width = True)
            st.markdown('<p class="sub_header-font">Dados Indisponíveis</p>', unsafe_allow_html=True)
        elif media_gauge_empresa < media_quartil_1:
            fraco()
        elif media_gauge_empresa >= media_quartil_1 and media_gauge_empresa < media_mediana:
            mod_fraco()
        elif media_gauge_empresa >= media_mediana and media_gauge_empresa < media_quartil_3:
            mod_forte()
        elif media_gauge_empresa >= media_quartil_3:
            forte()
        else:
            st.image('nan.png',use_column_width = True)
            st.markdown('<p class="sub_header-font">Dados Indisponíveis</p>', unsafe_allow_html=True)
    with col2_mid:
        st.markdown('<p class="sub_header-font">Diferença entre o desempenho da empresa e a média do setor</p>', unsafe_allow_html=True)
        value_empresa = st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Indicador'] == option,st.session_state.df_comparacao.columns[3:]].iloc[0]
       
        if(option=='Alavancagem Financeira'):
            value_empresa = value_empresa * 100
            
            value_media_setor = st.session_state.df_dados_setor_todas.loc[15, st.session_state.df_comparacao.columns[3:]] / (st.session_state.df_dados_setor_todas.loc[15, st.session_state.df_comparacao.columns[3:]] + st.session_state.df_dados_setor_todas.loc[8,st.session_state.df_comparacao.columns[3:]]) * 100
            
        else:
            value_media_setor = st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Indicador'] == option,st.session_state.df_comparacao.columns[3:]].iloc[1]
            
        value_diferenca = value_empresa-value_media_setor
        if(option == 'Alavancagem Financeira'):
            value_diferenca = value_diferenca/100
        if(option == 'Prazo Médio de Pagamentos' or option == 'Prazo Médio de Recebimentos'):
            value_diferenca = value_diferenca/100
        
        
        row1_col2_mid = st.columns(len(value_diferenca))
        for (col,year,value) in zip(row1_col2_mid,st.session_state.df_comparacao.columns[3:],value_diferenca):
        
            col.markdown('<p class="text-font">'+str(year)+'</p>', unsafe_allow_html=True)

            if(~np.isnan(value)):    
                col.markdown('<p class="sub_header-font">'+str(round(value*100,2))+'%</p>', unsafe_allow_html=True)
            else:
                col.markdown('<p class="sub_header-font">Sem Dados</p>', unsafe_allow_html=True)

        
        line_fig = px.line(x=st.session_state.df_comparacao.columns[3:], y=value_diferenca*100)
        
        
        #Arranjar a linha aos pontos. Acho que a aquela formula não está correta
        
        # line_fig.add_trace(
            # go.Scatter(
                # x=st.session_state.df_comparacao.columns[3:],
                # y = 0.045*value_diferenca + 0.0252,
                # mode="lines",
                # line=go.scatter.Line(color="gray"),
                # showlegend=False)
        # )
        line_fig.update_traces(line_color='#192646', line_width=5)       
        line_fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=st.session_state.df_comparacao.columns[3:],
                ticktext=[str(year) for year in st.session_state.df_comparacao.columns[3:]],
                
            ),
            xaxis_title=None,
            yaxis_title=None,
            height = 250

        )
        
        st.plotly_chart(line_fig,use_container_width=True)
    with col1_bot:
        bar_fig = go.Figure()
        bar_fig.add_trace(go.Bar(x=st.session_state.df_comparacao.columns[3:], y=value_empresa, name="Empresa", marker=dict(color='#192646')))
        bar_fig.add_trace(go.Bar(x=st.session_state.df_comparacao.columns[3:], y=value_media_setor, name="Média do Setor", marker=dict(color='#959fb8')))
        bar_fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=st.session_state.df_comparacao.columns[3:],
                ticktext=[str(year) for year in st.session_state.df_comparacao.columns[3:]],            
            ),
            height = 320

        )
        
        st.plotly_chart(bar_fig, use_container_width=True)
    with col2_bot:
    
     
        if media_gauge_empresa == 0:
            st.markdown('<p class="sub_header-font">Dados Indisponíveis</p>', unsafe_allow_html=True)
        elif media_gauge_empresa < media_quartil_1:
            st.markdown('<p class="sub_header-font">Em comparação com a média móvel do setor nos anos avaliados do indicador <strong>'+option+'</strong>, o desempenho da empresa no mesmo intervalo foi <strong>fraco</strong>, figurando entre as <strong>25% piores</strong>.</p>', unsafe_allow_html=True)
        elif media_gauge_empresa >= media_quartil_1 and media_gauge_empresa < media_mediana:
            st.markdown('<p class="sub_header-font">Em comparação com a média móvel do setor nos anos avaliados do indicador <strong>'+option+'</strong>, o desempenho da empresa no mesmo intervalo foi <strong>moderadamente fraco</strong>, figurando entre as <strong>50% piores</strong>.</p>', unsafe_allow_html=True)

        elif media_gauge_empresa >= media_mediana and media_gauge_empresa < media_quartil_3:
            st.markdown('<p class="sub_header-font">Em comparação com a média móvel do setor nos anos avaliados do indicador <strong>'+option+'</strong>, o desempenho da empresa no mesmo intervalo foi <strong>moderadamente forte</strong>, figurando entre as <strong>50% melhores</strong>.</p>', unsafe_allow_html=True)

        elif media_gauge_empresa >= media_quartil_3:
            st.markdown('<p class="sub_header-font">Em comparação com a média móvel do setor nos anos avaliados do indicador <strong>'+option+'</strong>, o desempenho da empresa no mesmo intervalo foi <strong>forte</strong>, figurando entre as <strong>25% melhores</strong>.</p>', unsafe_allow_html=True)

        else:
            st.markdown('<p class="sub_header-font">Dados Indisponíveis</p>', unsafe_allow_html=True)
else:
    st.write('Carregar ficheiros primeiro')