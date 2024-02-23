import plotly.graph_objects as go # pip install plotly
import streamlit as st # pip install streamlit
import Print as Print # ficheiro Print.py

# configuração da página
st.set_page_config(
    page_title="Dashboard Gestão",
    page_icon="📈",
    layout="wide",
)


if 'df_comparacao' and 'df_demo_resultados' and 'df_balanco' and 'df_indicadores' in st.session_state: # melhorar este if
    
    
    ##############################DASHBOARD GESTÃO############################

    col1_logo, col2_text = st.columns([1,3]) # coluna para a logo e para o texto

    config = {'displaylogo': False} # configuração para desabilitar o logo do plotly em cada gráfico
  
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
    .cell-text{
        user-select: all;

    }
    tspan.line{
        text-align: justify !important; 
        text-align-last: center !important;
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
    </style>
    """, unsafe_allow_html=True)   

    with col1_logo:
        st.image('images/logo1.png', use_column_width=True) # logo STREAM
    
    with col2_text:
        st.markdown('<p class="title-font">Indicadores para a gestão de negócio</p>', unsafe_allow_html=True)
        st.divider()

    # valor minimo do ano
    min_value=st.session_state.df_indicadores.columns[2]

    # valor máximo do ano
    max_value=st.session_state.df_indicadores.columns[-1]

    # caixa numérica para o ano de inicio do projeto
    ano_inicio = st.sidebar.number_input("Ano de inicio do projeto:", value=2017, min_value=min_value, max_value=max_value)

    # caixa numérica para o ano de término do projeto
    ano_fim = st.sidebar.number_input("Ano de fim do projeto:", value=2022, min_value=min_value, max_value=max_value)
    
    # caixa numérica para a despesa elegível do projeto
    despesa_elegivel = st.sidebar.number_input("Despesa elegível do projeto:",value=None)

    # VAB no inicio e no fim do projeto
    vab_inicio = st.session_state.df_demo_resultados.loc[31,int(ano_inicio)]
    vab_fim = st.session_state.df_demo_resultados.loc[31,int(ano_fim)]

    # Nível de Valor Acrescentado no inicio e no fim do projeto
    valor_acresc_inicio = round(st.session_state.df_indicadores.loc[4,int(ano_inicio)]*100,2)
    valor_acresc_fim = round(st.session_state.df_indicadores.loc[4,int(ano_fim)]*100,2)

    # Valor Gerado pelos Recursos Humanos no inicio e no fim do projeto
    valor_gerado_rh_inicio = round(st.session_state.df_indicadores.loc[14,int(ano_inicio)],2)
    valor_gerado_rh_fim = round(st.session_state.df_indicadores.loc[14,int(ano_fim)],2)

    
    if(despesa_elegivel==None):
        # Se a despesa elegível ainda não estiver indicada
        impacto_investimento = "Inserir valor da despesa<br> elegível do projeto"
    else:
        impacto_investimento = round((vab_fim-vab_inicio) / despesa_elegivel*100,2)
    
    rowEvenColor = 'white'
    rowOddColor = '#f2f2f2'

    
    table = go.Figure(go.Table(
    header=dict(values=["",str(ano_inicio)+"<br>Ano pré projeto", str(ano_fim)+"<br>Ano conclusão do investimento"],
                line_color='white',
                fill_color='white',
                font = dict(color='#4473c9', size=18, family="Droid Sans"),
                height=20,
                ),
    cells=dict(values=[
                        [r'I. Impacto do investimento no valor gerado pela empresa','','II. Nível de valor acrescentado','','III. Valor gerado por recurso humano'],
                        ['N.A.  ','', str(valor_acresc_inicio)+' %','', str('{:,.2f}'.format(valor_gerado_rh_inicio))+' €'],
                        [impacto_investimento if despesa_elegivel==None else str(impacto_investimento)+' %','', str(valor_acresc_fim)+' %','', str('{:,.2f}'.format(valor_gerado_rh_fim))+' €']],
                font_color=['#4473c9','#203a71','#203a71'],
                line_color=[[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
                fill_color=[[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
                font_size=18,
                font_family="Droid Sans",
                height=60,
                align=['left','center','center'])),
               
    )

    table.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=800,
        height=600
    )

    st.write("")
    st.write("")
    st.plotly_chart(table, use_container_width=True, config=config)


    # botões para fazer o download da imagem, PDF e copiar para a clipboard a dashboard 
    Print.buttons()
    
    st.markdown('<p style="text-align: right;" class="text-font">Fonte: Banco de Portugal</p>', unsafe_allow_html=True)


else:
    st.write('Carregar ficheiros primeiro')