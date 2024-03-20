import numpy as np # pip install numpy
import plotly.express as px # pip install plotly
import plotly.graph_objects as go # pip install plotly
import requests
import streamlit as st # pip install streamlit
import statistics
import Print as Print # ficheiro Print.py
import streamlit.components.v1 as components
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Dashboard por Indicador",
    page_icon="📈",
    layout="wide",
)

def add_notation_to_fig(fig, years, values, color, enabled):
    offset = max(values)*10
    if enabled:
        for i, val in enumerate(values): 
                fig.add_annotation(
                    x=years[i],
                    y=val*100 + offset,
                    text=f"{int(val*100)}%" if pd.notna(val) else "N.A",
                    font=dict(color="#011138", size=12),
                    showarrow=False
                )

if 'df_todas_dimen' and 'df_dados_setor_todas' and 'df_comparacao' in st.session_state:

    ##############################DASHBOARD POR INDICADOR############################

    col1_logo, col2_text = st.columns([1,3]) # coluna do logo e do texto.
    
    col1_mid, col2_mid = st.columns([1,3]) # coluna do medidor e do gráfico de linhas.

    col1_bot, col2_bot = st.columns([2,1]) # coluna do gráfico de barras e do texto.

    config = {'displaylogo': False} # configuração para desabilitar o logo do plotly em cada gráfico

    # CSS
    st.markdown("""
    <style>
    
    div[data-testid='stAppViewBlockContainer'] {
        padding-left: 50px;
        padding-right: 50px;
        max-width: 1286px;
        max-height: 1620px;
    }
                
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
                
    div[data-testid="stHorizontalBlock"]:nth-child(-n+3):not(:first-child) div[data-testid="column"]  {
        background-color: rgb(243, 243, 243);
        border-radius: 25px;
        padding: 10px 20px 0 20px;
        
    }
                
    div[data-testid="stHorizontalBlock"]:nth-child(2) div[data-testid="column"]:first-child div[data-testid="stVerticalBlockBorderWrapper"]:first-child div[data-testid="element-container"]:nth-child(4) {
        padding: 30px 0 0 0;
        
    }
    
    .st-style-button {
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 38.4px;
        margin: 0px;
        line-height: 1.6;
        color: inherit;
        width: auto;
        user-select: none;
        background-color: white; /* Set a white background */
        border: 1px solid rgba(49, 51, 63, 0.2);
        outline: none; !important
        box-shadow: none !important;
    }

    .st-style-button:hover {
        background-color: white;
        color: #0A04D2;
        border: 1px solid #0A04D2;
    }
    div[data-testid='stSidebarNav'] ul{
        max-height:none;
    }
    button[title="View fullscreen"]{
        visibility: hidden;
    }
    hr{
        margin: 0px;
    }

    </style>
    """, unsafe_allow_html=True)

    # função que será chamada cada vez que o indicador selecionado muda
    # utilizada para corrigir bug do streamlit
    def option_callback():
        st.session_state.option = st.session_state.new_option

    options_array= ['Margem Bruta', 'Margem Operacional', 'Margem Líquida',
    'Rentabilidade do Ativo', 'Nível de Valor Acrescentado','Liquidez Geral','Liquidez Reduzida','Liquidez imediata','Autonomia Financeira','Endividamento','Solvabilidade',
    'Alavancagem Financeira','Rentabilidade do Capital Investido','Rentabilidade do Capital Próprio','Turnover do Ativo','% Rh no Volume de Negócios',
    '% FSE no Volume de Negócios','% CMVMC / Volume de negócios','% Custos no Volume de Negócios','Prazo Médio de Pagamentos','Prazo Médio de Recebimentos','Taxa de Exportação']
    
    # inicia o indicador a Margem Bruta
    if "option" not in st.session_state:
        st.session_state.option = 'Margem Bruta'

    # selectbox com os indicadores    
    st.session_state.option = st.sidebar.selectbox('Escolher Indicador',('Margem Bruta', 'Margem Operacional', 'Margem Líquida',
    'Rentabilidade do Ativo', 'Nível de Valor Acrescentado','Liquidez Geral','Liquidez Reduzida','Liquidez imediata','Autonomia Financeira','Endividamento','Solvabilidade',
    'Alavancagem Financeira','Rentabilidade do Capital Investido','Rentabilidade do Capital Próprio','Turnover do Ativo','% Rh no Volume de Negócios',
    '% FSE no Volume de Negócios','% CMVMC / Volume de negócios','% Custos no Volume de Negócios','Prazo Médio de Pagamentos','Prazo Médio de Recebimentos', 'Taxa de Exportação'),index=options_array.index(st.session_state.option), key = 'new_option',on_change = option_callback)

    # caixa de texto para mudar o título. Por omissão é "Rentabilidade do negócio"
    titulo_principal = st.sidebar.text_input("Titulo principal","Rentabilidade do negócio")

    st.sidebar.markdown("***") # Cria uma linha na sidebar
    
    years_graph_gauge = st.session_state.df_comparacao.columns[3:] # todos os anos presentes na dataframe Comparação
    
    # range slider para o medidor (gauge) que vai desde o primeiro até o último ano que aparece na lista years_graph_gauge 
    year_slider_gauge = st.sidebar.slider(
        "Anos gráfico medidor:",
        min_value=int(min(years_graph_gauge)),
        max_value=int(max(years_graph_gauge)),
        value=(int(min(years_graph_gauge)), int(max(years_graph_gauge))),
        step=1
    )

    # caixa de texto para mudar o título do medidor
    titulo_gauge = st.sidebar.text_input("Titulo medidor","Desempenho agregado entre "+str(year_slider_gauge[0])+" e "+str(year_slider_gauge[1]))

    st.sidebar.markdown("***")

    # caixa de texto para mudar o título do gráfico de linhas
    titulo_linhas = st.sidebar.text_input("Titulo gráfico linhas","Diferença entre o desempenho da empresa e a média do setor")
    
    #color picker para escolher a cor do gráfico de linhas
    color_1 = st.sidebar.color_picker('Cor do grafico de linhas','#192646', key=1)

    years_graph_linhas = st.session_state.df_comparacao.columns[3:] # todos os anos presentes na dataframe Comparação

    # range slider para o gráfico de linhas que vai desde o primeiro até o último ano que aparece na lista years_graph_linhas 
    year_slider_linhas = st.sidebar.slider(
        "Anos gráfico de linhas:",
        min_value=int(min(years_graph_linhas)),
        max_value=int(max(years_graph_linhas)),
        value=(int(min(years_graph_linhas)), int(max(years_graph_linhas))),
        step=1
    )

    st.sidebar.markdown("***")

    # caixa de texto para mudar o titulo do gráfico de barras
    titulo_barras = st.sidebar.text_input("Título gráfico de barras",st.session_state.option)

    # 2 color pickers para escolher a cor do gráfico de barras no que toca à empresa e à média do setor
    color_2 = st.sidebar.color_picker('Cor do grafico de barras para a empresa','#192646', key=2)
    color_3 = st.sidebar.color_picker('Cor do grafico de barras para a média do setor','#959fb8', key=3)

    years_graph_barras = st.session_state.df_comparacao.columns[3:] # todos os anos presentes na dataframe Comparação

    # range slider para o gráfico de linhas que vai desde o primeiro até o último ano que aparece na lista years_graph_barras 
    year_slider_barras = st.sidebar.slider( 
        "Anos gráfico de barras:",
        min_value=int(min(years_graph_barras)),
        max_value=int(max(years_graph_barras)),
        value=(int(min(years_graph_barras)), int(max(years_graph_barras))),
        step=1
    )

    st.sidebar.markdown("***")
    
    # variável utilizada por causa da diferença de maiscúlas/minúsculas que as tabelas dos quadros do setor têm
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
    'Taxa de Exportação':'Taxa de Exportação'
    }

    # função para calcular a média dos quartis do setor de todas as dimensões, utilizada no medidor.    
    # função recebe os anos do range slide e devolve os valores dos 3 quartis
    def medias_per_year(years):
        media_quartil_1 = 0
        media_mediana = 0
        media_quartil_3 = 0
        flag_year = 0 # flag para contar quantos anos têm o valor do respetivo indicador preenchido. Utilizado para fazer a média.
        # Alguns anos de certos indicadores não estão preenchidos nas tabelas dos quadros do setor.
        for year in years:
            if str(year) + ' Quartil 1' not in st.session_state.df_todas_dimen.columns:
                continue
            
            if(st.session_state.option=='Liquidez imediata'):

                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Passivo corrente', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Mediana'] / st.session_state.df_todas_dimen.loc['Passivo corrente', str(year) + ' Quartil 1']
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Caixa e depósitos bancários', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Passivo corrente', str(year) + ' Quartil 1']
                flag_year += 1
            elif(st.session_state.option=='Endividamento'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'] 
                media_mediana += st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Mediana'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'] 
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1']
                flag_year += 1
            elif(st.session_state.option=='Solvabilidade'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'] 
                media_mediana += st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Mediana'] / st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1'] 
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Passivo', str(year) + ' Quartil 1']
                flag_year += 1
            elif(st.session_state.option=='Alavancagem Financeira'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 1'] / (st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 1'] + st.session_state.df_todas_dimen.loc['Capital próprio', str(year) + ' Quartil 1'])
                media_mediana += st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Mediana'] / (st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Mediana'] + st.session_state.df_todas_dimen.loc['Capital próprio', str(year) + ' Mediana'])
                media_quartil_3 += st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 3'] / (st.session_state.df_todas_dimen.loc['Financiamentos obtidos', str(year) + ' Quartil 3'] + st.session_state.df_todas_dimen.loc['Capital próprio', str(year) + ' Quartil 3'])
                media_gauge_empresa = media_gauge_empresa * 100
                flag_year += 1
            elif(st.session_state.option == 'Rentabilidade do Capital Investido'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += (st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Quartil 1'] - st.session_state.df_todas_dimen.loc['Imposto', str(year) + ' Quartil 1']) / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1']
                media_mediana += (st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Mediana'] - st.session_state.df_todas_dimen.loc['Imposto', str(year) + ' Mediana']) / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Mediana'] 
                media_quartil_3 += (st.session_state.df_todas_dimen.loc['EBIT', str(year) + ' Quartil 3'] - st.session_state.df_todas_dimen.loc['Imposto', str(year) + ' Quartil 3']) / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 3']
                flag_year += 1
            elif(st.session_state.option == 'Nível de Valor Acrescentado'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Quartil 1'] / 100
                media_mediana += st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Mediana'] / 100
                media_quartil_3 += st.session_state.df_todas_dimen.loc['VAB em percentagem da produção', str(year) + ' Quartil 3'] / 100
                flag_year += 1
            elif(st.session_state.option == 'Turnover do Ativo'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Ativo', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Ativo', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Ativo', str(year) + ' Quartil 3']
                flag_year += 1
            elif(st.session_state.option == '% Rh no Volume de Negócios'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(st.session_state.option == '% FSE no Volume de Negócios'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(st.session_state.option == '% CMVMC / Volume de negócios'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Neg贸cios', str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Neg贸cios', str(year) + ' Mediana']
                media_quartil_3 += st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Quartil 3'] / st.session_state.df_dados_setor_todas.loc['Volume de Neg贸cios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(st.session_state.option == '% Custos no Volume de Negócios'):
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1']) and np.isnan(st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1']) and np.isnan(st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += (st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1']+st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1']+st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1']) / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1']
                media_mediana += (st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Mediana']+st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Mediana']+st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Mediana']) / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana']
                media_quartil_3 += (st.session_state.df_dados_setor_todas.loc['CMVMC', str(year) + ' Quartil 3']+st.session_state.df_dados_setor_todas.loc['FSE', str(year) + ' Quartil 3']+st.session_state.df_dados_setor_todas.loc['Gastos com Pessoal', str(year) + ' Quartil 3']) / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Quartil 3']
                flag_year += 1
            elif(st.session_state.option == 'Taxa de Exportação'):
                if(np.isnan(st.session_state.df_todas_dimen.loc['CMVMC', str(year) + ' Quartil 1']) and np.isnan(st.session_state.df_todas_dimen.loc['FSE', str(year) + ' Quartil 1']) and np.isnan(st.session_state.df_todas_dimen.loc['Gastos com Pessoal', str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += (st.session_state.df_todas_dimen.loc['Vendas e serviços prestados no mercado externo', str(year) + ' Quartil 1'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 1'])
                media_mediana += (st.session_state.df_dados_setor_todas.loc['Vendas e serviços prestados no mercado externo', str(year) + ' Mediana'] / st.session_state.df_dados_setor_todas.loc['Volume de Negócios', str(year) + ' Mediana'])
                media_quartil_3 += (st.session_state.df_todas_dimen.loc['Vendas e serviços prestados no mercado externo', str(year) + ' Quartil 3'] / st.session_state.df_todas_dimen.loc['Volume de Negócios', str(year) + ' Quartil 3'])
                flag_year += 1
                
                continue
            else:
                
                # se não estiver preenchido dá skip a esse ano
                if(np.isnan(st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(st.session_state.option), str(year) + ' Quartil 1'])):
                    continue
                media_quartil_1 += st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(st.session_state.option), str(year) + ' Quartil 1']
                media_mediana += st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(st.session_state.option),str(year)+' Mediana']
                media_quartil_3 += st.session_state.df_todas_dimen.loc[option_comparacao_varias.get(st.session_state.option),str(year)+' Quartil 3']
                flag_year += 1

        # cálcula da média         
        media_quartil_1 = media_quartil_1 / (flag_year if not flag_year == 0 else 1)
        media_mediana = media_mediana / (flag_year if not flag_year == 0 else 1)
        media_quartil_3 = media_quartil_3 / (flag_year if not flag_year == 0 else 1)
                
        return media_quartil_1, media_mediana, media_quartil_3
     
    with col1_logo:
        st.image('images/logo1.png', use_column_width=True) # logo STREAM
        
    
    with col2_text:
        #st.title(titulo_principal)
        #st.subheader(st.session_state.option)
        st.markdown(f'<p class="title-font">{titulo_principal}</p>', unsafe_allow_html=True)       
        st.markdown('<p class="sub_header-font">'+st.session_state.option+'</p>', unsafe_allow_html=True)
        st.divider()
        
    with col1_mid:

        # anos selecionados no range slider do medidor
        range_years_gauge = list(range(year_slider_gauge[0],year_slider_gauge[1]+1,1)) 

        # apresentação do titulo do medidor
        st.markdown(f'<p class="sub_header-font">{titulo_gauge}</p>', unsafe_allow_html=True) 
        
        # média da empresa
        
        media_gauge_empresa = statistics.mean(st.session_state.df_comparacao.loc[st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Indicador'] == st.session_state.option].index[0], range_years_gauge])*100
        
        # média do setor de todas as dimensões
        media_quartil_1, media_mediana, media_quartil_3 = medias_per_year(range_years_gauge)
        
        
        st.write("")
        st.write("")
        
        # apresentação da imagem com o medidor e o respetivo texto 
        if media_gauge_empresa == 0:
            st.image('images/0.png',use_column_width = True)
        elif media_quartil_1 == 0 and media_mediana == 0 and media_quartil_3 == 0:
            st.image('images/nan.png',use_column_width = True)
            st.markdown('<p class="sub_header-font"><b>Dados Indisponíveis</b></p>', unsafe_allow_html=True)
        elif media_gauge_empresa < media_quartil_1:
            st.image('images/low.png',use_column_width = True)
            st.markdown('<p class="sub_header-font"><b>Fraco</b></p>', unsafe_allow_html=True)
        elif media_gauge_empresa >= media_quartil_1 and media_gauge_empresa < media_mediana:
            st.image('images/mod_low.png',use_column_width = True)
            st.markdown('<p class="sub_header-font"><b>Insuficiente</b></p>', unsafe_allow_html=True)
        elif media_gauge_empresa >= media_mediana and media_gauge_empresa < media_quartil_3:
            st.image('images/mod_high.png',use_column_width = True)
            st.markdown('<p class="sub_header-font"><b>Forte</b></p>', unsafe_allow_html=True)  
        elif media_gauge_empresa >= media_quartil_3:
            st.image('images/high.png',use_column_width = True)
            st.markdown('<p class="sub_header-font"><b>Excelente</b></p>', unsafe_allow_html=True)
        else:
            st.image('images/nan.png',use_column_width = True)
            st.markdown('<p class="sub_header-font"><b>Dados Indisponíveis</b></p>', unsafe_allow_html=True)

    with col2_mid:
        
        # lista de anos selecionados no range slider do gráfico de linhas
        range_years_linhas = list(range(year_slider_linhas[0],year_slider_linhas[1]+1,1))

        # titulo do gráfico de linhas
        st.markdown(f'<p class="sub_header-font">{titulo_linhas}</p>', unsafe_allow_html=True)

        # valores da empresa do respetivo indicador selecionado, por ano
        value_empresa = st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Indicador'] == st.session_state.option,st.session_state.df_comparacao.columns[3:]].iloc[0]
        

        if(st.session_state.option=='Alavancagem Financeira'):
            value_empresa = value_empresa * 100 
            
            # valores da média do setor, de todas as dimensões, do respetivo indicador selecionado, por ano
            value_media_setor = st.session_state.df_dados_setor_todas.loc[15, st.session_state.df_comparacao.columns[3:]] / (st.session_state.df_dados_setor_todas.loc[15, st.session_state.df_comparacao.columns[3:]] + st.session_state.df_dados_setor_todas.loc[8,st.session_state.df_comparacao.columns[3:]]) * 100
            
        else:
            # valores da média do setor, de todas as dimensões, do respetivo indicador selecionado, por ano
            value_media_setor = st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Indicador'] == st.session_state.option,st.session_state.df_comparacao.columns[3:]].iloc[1]
            
        # calcula a diferença entre os valores da empresa e a média do setor 
        value_diferenca = value_empresa-value_media_setor
        if(st.session_state.option == 'Alavancagem Financeira'):
            value_diferenca = value_diferenca/100 
        if(st.session_state.option == 'Prazo Médio de Pagamentos' or st.session_state.option == 'Prazo Médio de Recebimentos'):
            value_diferenca = value_diferenca/100
        
        
        row1_col2_mid = st.columns(len(range_years_linhas)) # vai criar uma coluna para cada ano selecionado no range slider do gráfico de linhas
        for (col,year,value) in zip(row1_col2_mid,range_years_linhas,value_diferenca.loc[year_slider_linhas[0]:year_slider_linhas[1]]):
            # em cada coluna criada coloca-se o ano e o valor da diferença em percentagem
            col.markdown('<p class="text-font"><b>'+str(year)+'</b></p>', unsafe_allow_html=True)

            if(~np.isnan(value)):    
                # se tiver valor da diferença
                col.markdown('<p style="font-weight: 1000;font-size: 20px;">'+str(round(value*100,2))+' p.p</p>', unsafe_allow_html=True)
            else:
                # se não tiver valor da diferença
                col.markdown('<p style="font-weight: 1000;font-size: 20px;text-align:center;">Sem Dados</p>', unsafe_allow_html=True)

        # criação do gráfico de linhas com uma trendline (na verdade é um gráfico de dispersão, mas os pontos estão unidos por linhas)
        line_fig = px.scatter(x=range_years_linhas, y=value_diferenca.loc[year_slider_linhas[0]:year_slider_linhas[1]]*100, trendline='ols')

        line_fig.update_traces(line_color=color_1, line_width=5, mode="lines") # o mode="lines" é para criar linhas entre os pontos   
        
        line_fig.update_layout(
            xaxis=dict(
                type="category",
                tickmode='array',
                tickvals=st.session_state.df_comparacao.columns[3:],
                ticktext=[str(year)+"         " for year in st.session_state.df_comparacao.columns[3:]],
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=2,
                xanchor="right",
                x=1,
                bgcolor="rgba(0,0,0,0)",  # Adjust the opacity as needed
                bordercolor="rgba(0,0,0,0)"  # Adjust the opacity as needed
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title=None,
            yaxis_title=None,
            height = 260
        )

        # unica forma de transformar uma trendline em uma linha pontilhada
        for  k, trace  in enumerate(line_fig.data):
            if trace.mode is not None and trace.mode == 'lines':
                line_fig.data[1].update(line_dash='dot',line_width=3)

        line_fig['data'][0]['showlegend']=True
        line_fig['data'][0]['name']='Diferença empresa/setor(p.p)'
        line_fig['data'][1]['showlegend']=True
        line_fig['data'][1]['name']='Linha de Tendência'
    
        st.plotly_chart(line_fig,use_container_width=True, config=config)
        

    with col1_bot:
        # lista de anos selecionados no range slider do gráfico de barras
        range_years_barras = list(range(year_slider_barras[0],year_slider_barras[1]+1,1)) 

        # toggle box para mudar entre um gráfico de barras ou linhas
        if not (toggle_barras_linhas := st.sidebar.toggle('Barras/Linhas')):

            annotation = st.sidebar.toggle('Mostrar valores')

        else:
            annotation = False
        


        bar_fig = go.Figure()

        # adiciona à figura um gráfico de barras com os valores da empresa
        bar_fig.add_trace(go.Bar(x=range_years_barras, y=value_empresa.loc[year_slider_barras[0]:year_slider_barras[1]]*100, name="Empresa", marker=dict(color=color_2)))

        # dependendo da toggle box é apresentado um gráfico de barras ou um de linhas
        if toggle_barras_linhas:
            bar_fig.add_trace(go.Scatter(x=range_years_barras, y=value_media_setor.loc[year_slider_barras[0]:year_slider_barras[1]]*100, name="Média do Setor", line={'width': 3}, marker=dict(color=color_3)))
        else:
            bar_fig.add_trace(go.Bar(x=range_years_barras, y=value_media_setor.loc[year_slider_barras[0]:year_slider_barras[1]]*100, name="Média do Setor", marker=dict(color=color_3)))
        
        bar_fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=st.session_state.df_comparacao.columns[3:],
                ticktext=[str(year)+"         " for year in st.session_state.df_comparacao.columns[3:]],
                ticksuffix="       ",
                tickfont=dict(color="#011138")
            ),
            yaxis=dict(
                    ticksuffix=" %",
                    tickprefix="        ",
                    zeroline=True, 
                    zerolinewidth=1, 
                    zerolinecolor="black",
                    tickfont=dict(color="#011138")
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title = titulo_barras,
            height = 320
        )
        
        add_notation_to_fig(bar_fig, [year - 0.18 for year in range_years_barras], value_empresa.loc[year_slider_barras[0]:year_slider_barras[1]], color_2, annotation)
        add_notation_to_fig(bar_fig, [year + 0.18 for year in range_years_barras], value_media_setor.loc[year_slider_barras[0]:year_slider_barras[1]], color_3, annotation)

        st.plotly_chart(bar_fig, use_container_width=True, config=config)

    with col2_bot:
    
        # apresentação do texto dependendo como a média da empresa se compara à média dos quartis do setor
        if media_gauge_empresa == 0:
            txt = ""
        elif media_quartil_1 == 0 and media_mediana == 0 and media_quartil_3 == 0:
            txt = ""
        elif media_gauge_empresa < media_quartil_1:
            txt = "Em comparação com a média do setor nos anos avaliados do indicador <span style='font-weight: 1000;'><i>"+st.session_state.option+"</i></span>, o desempenho da empresa foi <b><i>Fraco</i></span> (entre os 25% inferiores da mesma dimensão)."
            
        elif media_gauge_empresa >= media_quartil_1 and media_gauge_empresa < media_mediana:
            txt = "Em comparação com a média do setor nos anos avaliados do indicador <span style='font-weight: 1000;'><i>"+st.session_state.option+"</i></span>, o desempenho da empresa foi <span style='font-weight: 1000;'><i>Insuficiente</i></span> (entre os 50% inferiores da mesma dimensão)."
        
        elif media_gauge_empresa >= media_mediana and media_gauge_empresa < media_quartil_3:
            txt = "Em comparação com a média do setor nos anos avaliados do indicador <span style='font-weight: 1000;'><i>"+st.session_state.option+"</i></span>, o desempenho da empresa foi <span style='font-weight: 1000;'><i>Forte</i></span> (entre os 50% superiores da mesma dimensão)."
        
        elif media_gauge_empresa >= media_quartil_3:
            txt = "Em comparação com a média do setor nos anos avaliados do indicador <span style='font-weight: 1000;'><i>"+st.session_state.option+"</i></span>, o desempenho da empresa foi <span style='font-weight: 1000;'><i>Excelente</i></span> (entre os 25% superiores da mesma dimensão)."
    
        else:
            txt = ""

        # caixa de texto para modificar o texto
        txt = st.sidebar.text_area("Texto",txt)

        # CSS dependendo se o texto existe ou não
        if txt=="":
            st.markdown("""
            <style>
            div[data-testid="stHorizontalBlock"]:nth-child(3) div[data-testid="column"]:nth-child(2)  {
                background-color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""   
            <style>
                div[data-testid="stHorizontalBlock"]:nth-child(3) div[data-testid="column"]:nth-child(2)  {
                    background-color: rgb(195, 196, 204) !important;
                    color: white;
                    border-radius: 25px;
                    padding: 70px 35px;
                    align-items: center;
                    text-align: left;
                }
                div[data-testid="stHorizontalBlock"]:nth-child(3) div[data-testid="column"]:nth-child(2) div[data-testid="stVerticalBlockBorderWrapper"]:first-child{
                    padding: 30px 10px 30px 10px;
                }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown(f'<p style="font-size:22px;">{txt}</p>', unsafe_allow_html=True)
        
    # botões para fazer o download da imagem, PDF e copiar para a clipboard a dashboard 
    Print.buttons()
    
    st.markdown('<p style="text-align: right;" class="text-font">Fonte: Banco de Portugal</p>', unsafe_allow_html=True)
    
else:
    st.write('Carregar ficheiros primeiro')