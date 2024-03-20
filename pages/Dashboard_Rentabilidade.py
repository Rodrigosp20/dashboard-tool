import plotly.graph_objects as go # pip install plotly
import streamlit as st # pip install streamlit
import Print as Print # ficheiro Print.py

# configuração da página
st.set_page_config(
    page_title="Dashboard Rentabilidade",
    page_icon="📈",
    layout="wide",
)

# funções para apresentação do medidor e os respetivos textos de cada nível
def fraco():

    st.image('images/low.png',use_column_width=True)
    st.markdown('<p class="sub_header-font">Fraco</p>', unsafe_allow_html=True)
    st.markdown('<p class="text-font">No ano '+str(st.session_state.df_comparacao.columns[-1])+' em comparação com o setor, o desempenho da empresa foi <b>Fraco</b> (entre os 25% inferiores da mesma dimensão).</p>', unsafe_allow_html=True)
    
def mod_fraco():

    st.image('images/mod_low.png',use_column_width=True)
    st.markdown('<p class="sub_header-font">Insuficiente</p>', unsafe_allow_html=True)
    st.markdown('<p class="text-font">No ano '+str(st.session_state.df_comparacao.columns[-1])+' em comparação com o setor, o desempenho da empresa foi <b>Insuficiente</b> (entre os 50% inferiores da mesma dimensão).</p>', unsafe_allow_html=True)

def mod_forte():
    st.image('images/mod_high.png',use_column_width=True)
    st.markdown('<p class="sub_header-font">Forte</p>', unsafe_allow_html=True)
    st.markdown('<p class="text-font">No ano '+str(st.session_state.df_comparacao.columns[-1])+' em comparação com o setor, o desempenho da empresa foi <b>Forte</b> (entre os 50% superiores da mesma dimensão).</p>', unsafe_allow_html=True)
    
def forte():
    st.image('images/high.png',use_column_width=True)
    st.markdown('<p class="sub_header-font">Excelente</p>', unsafe_allow_html=True)
    st.markdown('<p class="text-font">No ano '+str(st.session_state.df_comparacao.columns[-1])+' em comparação com o setor, o desempenho da empresa foi <b>Excelente</b> (entre os 25% superiores da mesma dimensão).</p>', unsafe_allow_html=True)

# função que vai criar o medidor dependendo do valor da empresa em comparação com os quartis do setor
def create_gauge(empresa,quartil_1,mediana,quartil_3):
    if empresa == 0:
        st.image('images/0.png',use_column_width = True)
    elif empresa<quartil_1:
        fraco()
    elif empresa >= quartil_1 and empresa < mediana:
        mod_fraco()
    elif empresa >= mediana and empresa < quartil_3:
        mod_forte()
    elif empresa >= quartil_3:
        forte()
    else:
        st.image('images/nan.png',use_column_width=True)
        st.markdown('<p class="sub_header-font">Dados Indisponíveis</p>', unsafe_allow_html=True)


if 'df_comparacao' and 'df_demo_resultados' and 'df_balanco' and 'df_indicadores' and 'df_dados_setor_aplicavel' and 'df_dimen_aplicavel' in st.session_state: # melhorar este if
    
    ##############################DASHBOARD RENTABILIDADE############################
    
    col1_logo, col2_text = st.columns([1,3]) # coluna para o logo e o texto
    col1,col2,col3,col4,col5 = st.columns(5) # colunas para cada indicador

    config = {'displaylogo': False} # configuração para desabilitar o logo do plotly nos gráficos
    
    # CSS
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
    div[data-testid="stHorizontalBlock"]:nth-child(-n+3):not(:first-child) div[data-testid="column"]  {
        background-color: rgb(243, 243, 243);
        border-radius: 25px;
        padding: 10px 15px 10px 15px;
    }
                               
    div[data-testid="stHorizontalBlock"]:nth-child(-n+3):not(:first-child)  {
        gap: 0.5rem;
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
    button[title="View fullscreen"]{
            visibility: hidden;
    }
    div[data-testid='stSidebarNav'] ul{
        max-height:none;
    } 

       
    div[data-testid="stHorizontalBlock"]:nth-child(-n+3):not(:first-child) div[data-testid="column"] div[data-testid="element-container"]:nth-child(2) p.text-font{
        height: 30px;
    }  
                
    div[data-testid="stHorizontalBlock"]:nth-child(-n+3):not(:first-child) div[data-testid="column"] div[data-testid="element-container"]:first-child p.sub_header-font{
        height: 50px;
    }  
    
    </style>
    """, unsafe_allow_html=True)
    
       
    with col1_logo:
        st.image('images/logo1.png', use_column_width=True) # logo STREAM
    
    with col2_text:
        st.markdown('<p class="header-font">Comparação Setorial</p>', unsafe_allow_html=True)
        st.markdown('<p class="title-font">Rentabilidade do negócio</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub_header-font">Qual é a lucratividade do meu negócio, comparado ao setor?</p>', unsafe_allow_html=True)
        st.divider()

    with col1:
    
        # color pickers para as cores de cada gráfico
        color_1 = st.sidebar.color_picker('Cor do grafico de barras para a empresa','#192F5A', key=1)
        color_2 = st.sidebar.color_picker('Cor da linha para a todas as dimensões','#7D7F81', key=2)
        color_3 = st.sidebar.color_picker('Cor da linha para a dimensão aplicável','#BFCCE8', key=3)
    
        st.markdown('<p class="sub_header-font">Margem Operacional</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Qual é a eficiência com a qual a empresa gere suas despesas operacionais em relação a receita?</p>', unsafe_allow_html=True)
        
        years_graph = st.session_state.df_comparacao.columns[3:] # todos os anos da dataframe Comparação
        years_graph = [year for year in years_graph if not st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Entidade'] == 'Média do Setor', year].isna().any()]
        
        # range slider para os gráficos que vai desde o primeiro até o último ano que aparece na lista years_graph 
        year_slider = st.sidebar.slider(
                "Anos gráfico de linhas:",
                min_value=int(min(years_graph)),
                max_value=int(max(years_graph)),
                value=(int(min(years_graph)), int(max(years_graph))),
                step=1
        )

        range_years = list(range(year_slider[0],year_slider[1]+1,1)) # lista dos anos selecionados no range slider

        # valores da empresa, do setor em todas as dimensões e do setor na dimensão aplicável do indicador Margem Operacional
        # valores utilizados pelo gráfico de barras
        margem_operacional_values_graph = st.session_state.df_comparacao.loc[1, st.session_state.df_comparacao.columns[3:]]  
        media_margem_operacional_todos_values_graph = st.session_state.df_comparacao.loc[2, st.session_state.df_comparacao.columns[3:]]
        media_margem_operacional_aplicavel_values_graph = st.session_state.df_dados_setor_aplicavel.loc[1,st.session_state.df_dados_setor_aplicavel.columns[1:]] / st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]
        
        # toggle box para mudar entre gráfico de linhas ou barras
        toggle_barras_linhas = st.sidebar.toggle('Linhas/Barras')

        margem_operacional = go.Figure()
        
        # dependendo da toggle box é utilizado barras ou linhas nos gráficos do setor em todas as dimensões e do setor na dimensão aplicável
        if toggle_barras_linhas:
            margem_operacional.add_trace(go.Bar(x=range_years, y=media_margem_operacional_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões          ", marker=dict(color=color_2)))
            margem_operacional.add_trace(go.Bar(x=range_years, y=media_margem_operacional_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"         ",marker=dict(color=color_3)))
        else:
            margem_operacional.add_trace(go.Scatter(x=range_years, y=media_margem_operacional_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões          ",line=dict(color=color_2, width=2.3)))
            margem_operacional.add_trace(go.Scatter(x=range_years, y=media_margem_operacional_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"          ",line=dict(color=color_3, width=2.3)))

        margem_operacional.add_trace(go.Bar(x=range_years, y=margem_operacional_values_graph.loc[year_slider[0]:year_slider[1]]*100,name="Empresa", marker=dict(color=color_1)))

        margem_operacional.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=range_years,
                ticktext=[str(year)+"        " for year in range_years]
            ),
            yaxis=dict(
                ticksuffix=" %",
                tickprefix="   ",
                zeroline=True, 
                zerolinewidth=1, 
                zerolinecolor=color_1,
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(margem_operacional,use_container_width=True, config=config)
        
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        # valores da empresa e dos 3 quartis do setor do indicador Margem Operacional
        gauge_empresa_margem_operacional = st.session_state.df_comparacao.loc[1,range_years[-1]]*100
        quartil_1_margem_operacional = st.session_state.df_dimen_aplicavel.loc['Margem Operacional',str(range_years[-1])+' Quartil 1']
        mediana_margem_operacional = st.session_state.df_dimen_aplicavel.loc['Margem Operacional',str(range_years[-1])+' Mediana']
        quartil_3_margem_operacional = st.session_state.df_dimen_aplicavel.loc['Margem Operacional',str(range_years[-1])+' Quartil 3']
          
        # função para apresentação do medidor e dos respetivos textos  
        create_gauge(gauge_empresa_margem_operacional,quartil_1_margem_operacional,mediana_margem_operacional,quartil_3_margem_operacional)

        
    with col2:
        st.markdown('<p class="sub_header-font">Margem Bruta</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Qual é o lucro obtido após subtrairem-se os custos de produção?</p>', unsafe_allow_html=True)
        
        margem_bruta_values_graph = st.session_state.df_comparacao.loc[4, st.session_state.df_comparacao.columns[3:]] 
        media_margem_bruta_todos_values_graph = st.session_state.df_comparacao.loc[5, st.session_state.df_comparacao.columns[3:]]
        media_margem_bruta_aplicavel_values_graph = (st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]-st.session_state.df_dados_setor_aplicavel.loc[2,st.session_state.df_dados_setor_aplicavel.columns[1:]]) / st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]
        

        margem_bruta = go.Figure()
        if toggle_barras_linhas:
            margem_bruta.add_trace(go.Bar(x=range_years, y=media_margem_bruta_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões                      ",marker=dict(color=color_2)))
            margem_bruta.add_trace(go.Bar(x=range_years, y=media_margem_bruta_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"          ",marker=dict(color=color_3)))
        else:
            margem_bruta.add_trace(go.Scatter(x=range_years, y=media_margem_bruta_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões                     ",line=dict(color=color_2, width=2.3)))
            margem_bruta.add_trace(go.Scatter(x=range_years, y=media_margem_bruta_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"         ",line=dict(color=color_3, width=2.3)))
        margem_bruta.add_trace(go.Bar(x=range_years, y=margem_bruta_values_graph.loc[year_slider[0]:year_slider[1]]*100,name="Empresa", marker=dict(color=color_1)))

        margem_bruta.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=range_years,
                ticktext=[str(year)+"        " for year in range_years]
            ),
            yaxis=dict(
                ticksuffix=" %",
                tickprefix="   ",
                zeroline=True, 
                zerolinewidth=1, 
                zerolinecolor=color_1,
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(margem_bruta,use_container_width=True, config=config)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_margem_bruta = st.session_state.df_comparacao.loc[4,range_years[-1]]*100
        quartil_1_margem_bruta = st.session_state.df_dimen_aplicavel.loc['Margem bruta',str(range_years[-1])+' Quartil 1']
        mediana_margem_bruta = st.session_state.df_dimen_aplicavel.loc['Margem bruta',str(range_years[-1])+' Mediana']
        quartil_3_margem_bruta = st.session_state.df_dimen_aplicavel.loc['Margem bruta',str(range_years[-1])+' Quartil 3']
            

        create_gauge(gauge_empresa_margem_bruta,quartil_1_margem_bruta,mediana_margem_bruta,quartil_3_margem_bruta)
        
                
    with col3:
        st.markdown('<p class="sub_header-font">Margem Líquida</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Qual é a lucratividade líquida do negócio?</p>', unsafe_allow_html=True)

        margem_liquida_values_graph = st.session_state.df_comparacao.loc[7, st.session_state.df_comparacao.columns[3:]] 
        media_margem_liquida_todos_values_graph = st.session_state.df_comparacao.loc[8, st.session_state.df_comparacao.columns[3:]]
        media_margem_liquida_aplicavel_values_graph = st.session_state.df_dados_setor_aplicavel.loc[5,st.session_state.df_dados_setor_aplicavel.columns[1:]] / st.session_state.df_dados_setor_aplicavel.loc[0,st.session_state.df_dados_setor_aplicavel.columns[1:]]
        
        margem_liquida = go.Figure()
        if toggle_barras_linhas:
            margem_liquida.add_trace(go.Bar(x=range_years, y=media_margem_liquida_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões                    ",marker=dict(color=color_2)))
            margem_liquida.add_trace(go.Bar(x=range_years, y=media_margem_liquida_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"          ",marker=dict(color=color_3)))
        else:
            margem_liquida.add_trace(go.Scatter(x=range_years, y=media_margem_liquida_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões                    ",line=dict(color=color_2, width=2.3)))
            margem_liquida.add_trace(go.Scatter(x=range_years, y=media_margem_liquida_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"         ",line=dict(color=color_3, width=2.3)))
       
        margem_liquida.add_trace(go.Bar(x=range_years, y=margem_liquida_values_graph.loc[year_slider[0]:year_slider[1]]*100,name="Empresa", marker=dict(color=color_1)))
        
        margem_liquida.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=range_years,
                ticktext=[str(year)+"        " for year in range_years]
            ),
            yaxis=dict(
                ticksuffix=" %",
                tickprefix="   ",
                zeroline=True, 
                zerolinewidth=1, 
                zerolinecolor=color_1,
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(margem_liquida,use_container_width=True, config=config)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_margem_liquida = st.session_state.df_comparacao.loc[7,range_years[-1]]*100
        quartil_1_margem_liquida = st.session_state.df_dimen_aplicavel.loc['Margem líquida',str(range_years[-1])+' Quartil 1']
        mediana_margem_liquida = st.session_state.df_dimen_aplicavel.loc['Margem líquida',str(range_years[-1])+' Mediana']
        quartil_3_margem_liquida = st.session_state.df_dimen_aplicavel.loc['Margem líquida',str(range_years[-1])+' Quartil 3']
          
        
        create_gauge(gauge_empresa_margem_liquida,quartil_1_margem_liquida,mediana_margem_liquida,quartil_3_margem_liquida)
        
        
    with col4:
        st.markdown('<p class="sub_header-font">Nivel de Valor Acrescentado</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Quanto valor adicional a empresa cria em relação aos custos de produção?</p>', unsafe_allow_html=True)
        
        valor_acresc_values_graph = st.session_state.df_comparacao.loc[10, range_years] 
        media_valor_acresc_todos_values_graph = st.session_state.df_comparacao.loc[11, range_years]
        media_valor_acresc_aplicavel_values_graph = st.session_state.df_dados_setor_aplicavel.loc[24, range_years]
        

        valor_acresc = go.Figure()
        if toggle_barras_linhas:
            valor_acresc.add_trace(go.Bar(x=range_years, y=media_valor_acresc_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões                    ",marker=dict(color=color_2)))
            valor_acresc.add_trace(go.Bar(x=range_years, y=media_valor_acresc_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"          ",marker=dict(color=color_3)))
        else:
            valor_acresc.add_trace(go.Scatter(x=range_years, y=media_valor_acresc_todos_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Todas as Dimensões                   ",line=dict(color=color_2, width=2.3)))
            valor_acresc.add_trace(go.Scatter(x=range_years, y=media_valor_acresc_aplicavel_values_graph.loc[year_slider[0]:year_slider[1]]*100, name=st.session_state.dimensao+"         ",line=dict(color=color_3, width=2.3)))
        valor_acresc.add_trace(go.Bar(x=range_years, y=valor_acresc_values_graph.loc[year_slider[0]:year_slider[1]]*100,name="Empresa", marker=dict(color=color_1)))
        
        valor_acresc.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=range_years,
                ticktext=[str(year)+"        " for year in range_years]
            ),
            yaxis=dict(
                ticksuffix=" %",
                tickprefix="   ",
                zeroline=True, 
                zerolinewidth=1, 
                zerolinecolor=color_1,
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(valor_acresc,use_container_width=True, config=config)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_valor_acresc = st.session_state.df_comparacao.loc[10,range_years[-1]]*100
        quartil_1_valor_acresc = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção', str(range_years[-1])+' Quartil 1']
        mediana_valor_acresc = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção', str(range_years[-1])+' Mediana']
        quartil_3_valor_acresc = st.session_state.df_dimen_aplicavel.loc['VAB em percentagem da produção', str(range_years[-1])+' Quartil 3']
       
        
        create_gauge(gauge_empresa_valor_acresc,quartil_1_valor_acresc,mediana_valor_acresc,quartil_3_valor_acresc)
        
        
    with col5:
        st.markdown('<p class="sub_header-font">Rentabilidade do Ativo</p>', unsafe_allow_html=True)
        st.markdown('<p class="text-font">Quão eficientemente a empresa utiliza seus ativos para gerar lucro?</p>', unsafe_allow_html=True)
        
        rent_ativo_values_graph = st.session_state.df_comparacao.loc[13, st.session_state.df_comparacao.columns[3:]] 
        
        
        media_rent_ativo_aplicavel_values_graph = dict(zip(st.session_state.df_comparacao.columns[3:], [None]*len(st.session_state.df_comparacao.columns[3:])))
        media_rent_ativo_todos_values_graph = dict(zip(st.session_state.df_comparacao.columns[3:], [None]*len(st.session_state.df_comparacao.columns[3:])))
        
        for year in range_years:
            media_rent_ativo_todos_values_graph[year] = st.session_state.df_todas_dimen.loc['Rentabilidade do ativo', str(year)+' Valor Médio']
            media_rent_ativo_aplicavel_values_graph[year] = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo', str(year)+' Valor Médio']
            

        range_todos_value = list({year: value for year, value in media_rent_ativo_todos_values_graph.items() if year >= year_slider[0] and year <= year_slider[1]}.values())
        range_aplicavel_value = list({year: value for year, value in media_rent_ativo_aplicavel_values_graph.items() if year >= year_slider[0] and year <= year_slider[1]}.values())
        st.write()
        rent_ativo = go.Figure()

        if toggle_barras_linhas:
            rent_ativo.add_trace(go.Bar(x=range_years, y=range_todos_value, name="Todas as Dimensões               ",marker=dict(color=color_2)))
            rent_ativo.add_trace(go.Bar(x=range_years, y=range_aplicavel_value, name=st.session_state.dimensao+"          ",marker=dict(color=color_3)))
        else:
            rent_ativo.add_trace(go.Scatter(x=range_years, y=range_todos_value, name="Todas as Dimensões               ",line=dict(color=color_2, width=2.3)))
            rent_ativo.add_trace(go.Scatter(x=range_years, y=range_aplicavel_value, name=st.session_state.dimensao+"          ",line=dict(color=color_3, width=2.3)))
        rent_ativo.add_trace(go.Bar(x=range_years, y=rent_ativo_values_graph.loc[year_slider[0]:year_slider[1]]*100, name="Empresa", marker=dict(color=color_1)))
        
        rent_ativo.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=range_years,
                ticktext=[str(year)+"        " for year in range_years]
            ),
            yaxis=dict(
                ticksuffix=" %",
                tickprefix="   ",
                zeroline=True, 
                zerolinewidth=1, 
                zerolinecolor=color_1,
            ),
            height= 300,
            legend=dict(
                yanchor="top",
                y=1.6,
                xanchor="left",
                x=0
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(rent_ativo,use_container_width=True, config=config)
        
        st.markdown('<p class="text-font">Desempenho no último ano registado</p>', unsafe_allow_html=True)
        
        gauge_empresa_rent_ativo = st.session_state.df_comparacao.loc[13,range_years[-1]]*100
        quartil_1_rent_ativo = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo',str(range_years[-1])+' Quartil 1']
        mediana_rent_ativo = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo',str(range_years[-1])+' Mediana']
        quartil_3_rent_ativo = st.session_state.df_dimen_aplicavel.loc['Rentabilidade do ativo',str(range_years[-1])+' Quartil 3']
        
        create_gauge(gauge_empresa_rent_ativo,quartil_1_rent_ativo,mediana_rent_ativo,quartil_3_rent_ativo)
    

    # botões para fazer o download da imagem, PDF e copiar para a clipboard a dashboard 
    Print.buttons()

    st.write("")
    st.markdown('<p style="padding:20px 0 0 0; text-align: right;" class="text-font">Fonte: Banco de Portugal</p>', unsafe_allow_html=True)

    
else:
    st.write('Carregar ficheiros primeiro')