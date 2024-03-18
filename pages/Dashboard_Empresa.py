import plotly.graph_objects as go # pip install plotly
import requests
import streamlit as st # pip install streamlit
import Print as Print # ficheiro Print.py
import streamlit.components.v1 as components

def add_notation_to_fig(fig, years, values, color, enabled):
    offset = max(values)*10
    if enabled:
        for i, val in enumerate(values): 
            fig.add_annotation(
                x=years[i],
                y=val*100 + offset,
                text=f"{int(val*100)} %",
                font=dict(color=color, size=12),
                showarrow=False
            )

# Configuração da página
st.set_page_config(
    page_title="Dashboard Empresa",
    page_icon="📈",
    layout="wide",
)

# CSS
st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul{
        max-height:none;
    }
            
    button[title="View fullscreen"]{
        visibility: hidden;
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
            
    div[data-testid="stHorizontalBlock"] div[data-testid="column"] div[data-testid="stHorizontalBlock"] div[data-testid="element-container"] {
        background-color: rgb(241, 241, 241);
        border-radius: 25px;
    }
            
    div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(2) div[data-testid="element-container"]{
        background-color: rgb(241, 241, 241);
        border-radius: 25px;
    }
              
    div[data-testid="stImage"]{
        margin: auto;
    }
            
    div[class="stPlotlyChart js-plotly-plot"]{
        display: block !important;
        margin: auto !important;
    }
    div[class="user-select-none svg-container"]{
        margin: auto !important;   
    }
   
    </style>
    """, unsafe_allow_html=True)

if 'df_comparacao' in st.session_state: # se a dataframe Comparação estiver criada
    
    ##############################DASHBOARD EMPRESA############################
    # função que será chamada cada vez que o indicador selecionado muda
    # utilizada para corrigir bug do streamlit
    def option_callback():
        st.session_state.option = st.session_state.new_option

    options_array= ['Margem Bruta', 'Margem Operacional', 'Margem Líquida',
    'Rentabilidade do Ativo', 'Nível de Valor Acrescentado','Liquidez Geral','Liquidez Reduzida','Liquidez imediata','Autonomia Financeira','Endividamento','Solvabilidade',
    'Alavancagem Financeira','Rentabilidade do Capital Investido','Rentabilidade do Capital Próprio','Turnover do Ativo','% Rh no Volume de Negócios',
    '% FSE no Volume de Negócios','% CMVMC / Volume de negócios','% Custos no Volume de Negócios','Prazo Médio de Pagamentos','Prazo Médio de Recebimentos', 'Taxa de Exportação']

    # inicia o indicador a Margem Bruta
    if "option" not in st.session_state:
        st.session_state.option = 'Margem Bruta'

    # selectbox com os indicadores
    st.session_state.option = st.sidebar.selectbox('Escolher Indicador para o Dashboard por Indicador',('Margem Bruta', 'Margem Operacional', 'Margem Líquida',
    'Rentabilidade do Ativo', 'Nível de Valor Acrescentado','Liquidez Geral','Liquidez Reduzida','Liquidez imediata','Autonomia Financeira','Endividamento','Solvabilidade',
    'Alavancagem Financeira','Rentabilidade do Capital Investido','Rentabilidade do Capital Próprio','Turnover do Ativo','% Rh no Volume de Negócios',
    '% FSE no Volume de Negócios','% CMVMC / Volume de negócios','% Custos no Volume de Negócios','Prazo Médio de Pagamentos','Prazo Médio de Recebimentos', 'Taxa de Exportação'),index=options_array.index(st.session_state.option), key = 'new_option',on_change = option_callback)

    st.markdown("## Dashboard Empresa")
    # na coluna da esquerda ficaram todos os gráficos mais pequenos e o logotipo da STREAM, e na coluna da direita ficará o gráfico maior
    # colunas serão do mesmo tamanho por isso o [1, 1]
    left_col, right_col = st.columns([1, 1]) 

    # lista dos anos que estão na dataframe Comparação
    # será utilizado na iniciação do range slider
    years_graph = list(range(st.session_state.df_comparacao.columns[3],st.session_state.df_comparacao.columns[-1]+1))
    
    with left_col: # dentro da coluna da esquerda
        
        column_1, column_2 = st.columns(2) # coluna de esquerda é dividida em mais 2 colunas
        
        st.image('images/logo1.png', width=400) # logotipo STREAM
            
        with column_1:
            ### MARGEM OPERACIONAL
            margem_operacional = go.Figure() # criação de uma figura com o plotly

            # range slider que vai desde o primeiro até o último ano que aparece na lista years_graph 
            year_slider = st.sidebar.slider( 
                "Selecionar os anos:",
                min_value=int(min(years_graph)),
                max_value=int(max(years_graph)),
                value=(int(min(years_graph)), int(max(years_graph))),
                step=1
            )

            annotation = st.sidebar.checkbox("Adicionar Label (Valor)", value=True)
            
            color = st.sidebar.color_picker('Escolher uma cor','#192646') # color picker para escolher a cor para os gráficos
            
            range_years = list(range(year_slider[0],year_slider[1]+1,1)) # lista dos anos escolhidos pelo range slider

            # buscar o valor da margem operacional ao dataframe Comparação nos respetivos anos do range slider
            margem_operacional_values_graph = st.session_state.df_comparacao.loc[1, year_slider[0]:year_slider[1]]
            
            # adicionar o gráfico de barras à figura
            margem_operacional.add_trace(go.Bar(x=range_years, y=margem_operacional_values_graph*100, width=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7], marker=dict(color=color)))

            config = {'displaylogo': False} # configuração para desabilitar o logo do plotly em cada gráfico
            
            add_notation_to_fig(margem_operacional, range_years, margem_operacional_values_graph, color, annotation)
                
            margem_operacional.update_layout(
                xaxis=dict( # alteração do eixo X para utilizar apenas os valores que lhe são dados no range_years, caso contrário ele começa a utilizar casas decimais entre os valores do X
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                yaxis=dict( 
                    ticksuffix=" %", # adiciona sufixo de % no eixo do Y
                    tickprefix="      ", # adiciona espaços em branco atrás dos valores de Y. Fix a um bug do plotly que corta alguns valores na hora de fazer o download da imagem do gráfico.
                    zeroline=True, # adiciona linha no eixo do X
                    zerolinewidth=1, 
                    zerolinecolor=color,
                ),

                paper_bgcolor='rgba(0,0,0,0)', # transparência do background na hora do download da imagem
                plot_bgcolor='rgba(0,0,0,0)', # transparência do background na hora do download da imagem
                title = "Margem Operacional", # titulo que aparece em cima do gráfico
                title_x=0.2, # alterar a posição do titulo para ficar centrado com o gráfico
                height= 300, # altura do gráfico
                width=250, # largura do gráfico
                showlegend=False # não mostrar a legenda do gráfico
            )

            # apresentação do gráfico. O parâmetro config é para desabilitar o logo do plotly em cada gráfico
            st.plotly_chart(margem_operacional, config=config)


            ### RENTABILIDADE DO CAPITAL PRÓPRIO
            rent_capital_proprio_values_graph = st.session_state.df_comparacao.loc[71, year_slider[0]:year_slider[1]]

            rent_capital_proprio = go.Figure()

            rent_capital_proprio.add_trace(go.Bar(x=range_years, y=rent_capital_proprio_values_graph*100, width=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7], marker=dict(color=color)))
            
            add_notation_to_fig(rent_capital_proprio, range_years, rent_capital_proprio_values_graph, color, annotation)

            rent_capital_proprio.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                yaxis=dict(
                    ticksuffix=" %",
                    tickprefix="      ",
                    zeroline=True, 
                    zerolinewidth=1, 
                    zerolinecolor=color,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title = "Rentabilidade do<br>Capital Próprio",
                title_x=0.25,
                height= 300,
                width=250,
                showlegend=False
            )

            st.plotly_chart(rent_capital_proprio, config=config)
            
            ### LIQUIDEZ GERAL
            
            liquidez_geral_values_graph = st.session_state.df_comparacao.loc[45, year_slider[0]:year_slider[1]]

            liquidez_geral = go.Figure()

            liquidez_geral.add_trace(go.Bar(x=range_years, y=liquidez_geral_values_graph*100, width=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7], marker=dict(color=color)))
            
            add_notation_to_fig(liquidez_geral, range_years, liquidez_geral_values_graph, color, annotation)

            liquidez_geral.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                yaxis=dict(
                    ticksuffix=" %",
                    tickprefix="      ",
                    zeroline=True, 
                    zerolinewidth=1, 
                    zerolinecolor=color,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title = "Liquidez Geral",
                title_x=0.2,
                height= 300,
                width=250,
                showlegend=False
            )

            st.plotly_chart(liquidez_geral, config=config)
        
        with column_2:
            ### LIQUIDEZ REDUZIDA

            liquidez_reduzida_values_graph = st.session_state.df_comparacao.loc[48, year_slider[0]:year_slider[1]]

            liquidez_reduzida = go.Figure()

            liquidez_reduzida.add_trace(go.Bar(x=range_years, y=liquidez_reduzida_values_graph*100, width=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7], marker=dict(color=color)))
            
            add_notation_to_fig(liquidez_reduzida, range_years, liquidez_reduzida_values_graph, color, annotation)

            liquidez_reduzida.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                yaxis=dict(
                    ticksuffix=" %",
                    tickprefix="      ",
                    zeroline=True, 
                    zerolinewidth=1, 
                    zerolinecolor=color,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title = "Liquidez Reduzida",
                title_x=0.2,
                height= 300,
                width=250,
                showlegend=False
            )

            st.plotly_chart(liquidez_reduzida, config=config)
            
            ### AUTONOMIA FINANCEIRA
            
            autonomia_financeira_values_graph = st.session_state.df_comparacao.loc[55, year_slider[0]:year_slider[1]]
            
            autonomia_financeira = go.Figure()

            autonomia_financeira.add_trace(go.Bar(x=list(range(year_slider[0],year_slider[1]+1,1)), y=autonomia_financeira_values_graph*100, width=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7], marker=dict(color=color)))
            
            add_notation_to_fig(autonomia_financeira, range_years, autonomia_financeira_values_graph, color, annotation)

            autonomia_financeira.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                yaxis=dict(
                    ticksuffix=" %",
                    tickprefix="      ",
                    zeroline=True, 
                    zerolinewidth=1, 
                    zerolinecolor=color,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title = "Autonomia Financeira",
                title_x=0.2,
                height= 300,
                width=250,
                showlegend=False
            )

            st.plotly_chart(autonomia_financeira, config=config)

            ### ALAVANCAGEM FINANCEIRA
                        
            alavancagem_financeira_values_graph = st.session_state.df_comparacao.loc[64, year_slider[0]:year_slider[1]]

            alavancagem_financeira = go.Figure()

            alavancagem_financeira.add_trace(go.Bar(x=range_years, y=alavancagem_financeira_values_graph*100, width=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7], marker=dict(color=color)))
            
            add_notation_to_fig(alavancagem_financeira, range_years, alavancagem_financeira_values_graph, color, annotation)

            alavancagem_financeira.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=range_years,
                    ticktext=[str(year) for year in range_years]
                ),
                yaxis=dict(
                    ticksuffix=" %",
                    tickprefix="      ",
                    zeroline=True, 
                    zerolinewidth=1, 
                    zerolinecolor=color,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title = "Alavancagem Financeira",
                title_x=0.2,
                height= 300,
                width=250,
                showlegend=False
            )
            st.plotly_chart(alavancagem_financeira, config=config)
        
    with right_col: # dentro da coluna da direita (coluna do gráfico grande)
        ### Comparação do desempenho de indicadores chave da empresa face ao setor
        
        # valores do indice de cada indicador na dataframe Comparação
        indice_values_graph = st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Entidade'] == 'Índice', year_slider[1]]

        # indicadores que são utilizados pela dataframe Comparação
        indicadores_graph=st.session_state.df_comparacao.loc[st.session_state.df_comparacao['Entidade'] == 'Índice', 'Indicador']
        
        indice = go.Figure()


        indice.add_trace(go.Bar(x=indice_values_graph-100, y="          "+indicadores_graph, text=round(indice_values_graph).astype('Int64').astype('str')+"     " if annotation else None, 
        textposition='outside', base=100, orientation='h', marker=dict(color=color)))
        
        indice.update_layout(
            title = "Comparação do desempenho de indicadores <br> chave da empresa face ao setor no ano "+str(year_slider[1]),
            title_x=0.2,
            width=2000,
            height=1200,
            xaxis=dict(
                side="top" # troca a posição do eixo do X para ficar no topo
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(indice,use_container_width=True, config=config)

    
    # botões para fazer o download da imagem, PDF e copiar para a clipboard a dashboard 
    Print.buttons()

    @st.cache_resource
    def load_unpkg(src: str) -> str:
        return requests.get(src).text


    HTML_2_CANVAS = load_unpkg("https://unpkg.com/html2canvas@1.4.1/dist/html2canvas.js")
    JSPDF = load_unpkg("https://unpkg.com/jspdf@latest/dist/jspdf.umd.min.js")

    if st.sidebar.button("DOWNLOAD PDF"):
        components.html(
                        f"""
            <script>{HTML_2_CANVAS}</script>
            <script>{JSPDF}</script>
            <script>
            const html2canvas = window.html2canvas
            const {{ jsPDF }} = window.jspdf

            const streamlitDoc = window.parent.document;
            const stApp = streamlitDoc.querySelector('.main > .block-container');

            const buttons = Array.from(streamlitDoc.querySelectorAll('.stButton > button'));
            const pdfButton = buttons.find(el => el.innerText === 'DOWNLOAD PDF');
            const docHeight = stApp.scrollHeight;
            const docWidth = stApp.scrollWidth;

            let topLeftMargin = 15;
            let pdfWidth = docHeight + (topLeftMargin * 2);
            let pdfHeight = (pdfWidth * 1.5) + (topLeftMargin * 2);
            let canvasImageWidth = docWidth;
            let canvasImageHeight = docHeight;

            let totalPDFPages = Math.ceil(docHeight / pdfHeight)-1;

            pdfButton.innerText = 'Creating PDF...';

            html2canvas(stApp, {{ allowTaint: true }}).then(function (canvas) {{

                canvas.getContext('2d');
                let imgData = canvas.toDataURL("image/jpeg", 1.0);

                let pdf = new jsPDF('p', 'px', [pdfWidth, pdfHeight]);
                pdf.addImage(imgData, 'JPG', topLeftMargin, topLeftMargin, canvasImageWidth, canvasImageHeight);

                for (var i = 1; i <= totalPDFPages; i++) {{
                    pdf.addPage();
                    pdf.addImage(imgData, 'JPG', topLeftMargin, -(pdfHeight * i) + (topLeftMargin*4), canvasImageWidth, canvasImageHeight);
                }}

                pdf.save('test.pdf');
                pdfButton.innerText = 'DOWNLOAD PDF';
            }})
            </script>
            """,
                        height=0,
                        width=0,
                    )

    st.markdown('<p style="text-align: right;" class="text-font">Fonte: Banco de Portugal</p>', unsafe_allow_html=True)
        
else:
    st.write('Carregar ficheiros primeiro')
              