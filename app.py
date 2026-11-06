import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Consultoria Demográfica - Startup", layout="wide", initial_sidebar_state="expanded")

# =========================================================================
# CRITÉRIO 1: INGESTÃO, TRATAMENTO DE DADOS (ETL) E INTERFACE
# =========================================================================
st.sidebar.title("🚀 Consultoria Demográfica")
st.sidebar.markdown("---")

st.sidebar.subheader("📥 Carga de Dados Públicos")
arquivo_postado = st.sidebar.file_uploader("Upload da Base IBGE (CSV)", type=["csv"])

# Função de ETL com tratamento de dados via Pandas e NumPy
def efetuar_etl(df_bruto):
    df = df_bruto.copy()
    df = df.dropna(subset=['Município', 'Taxa_Crescimento'])
    df['Taxa_Crescimento'] = pd.to_numeric(df['Taxa_Crescimento'], errors='coerce')
    df['Ano'] = df['Ano'].astype(int)
    return df

# Base de teste automática ou Upload do Usuário
if arquivo_postado is not None:
    df_bruto = pd.read_csv(arquivo_postado)
    df_limpo = efetuar_etl(df_bruto)
else:
    # Dados fictícios ajustados e corrigidos simulando o cenário real
    dados_mock = {
        'Município': ['Curitiba', 'Porto Alegre', 'Belo Horizonte', 'Salvador', 'Florianópolis', 'São Paulo', 'Rio de Janeiro', 'Cabo Frio', 'Cidade Exemplo X', 'Cidade Exemplo Y'],
        'Regiao': ['Sul', 'Sul', 'Sudeste', 'Nordeste', 'Sul', 'Sudeste', 'Sudeste', 'Sudeste', 'Norte', 'Nordeste'],
        'Ano':,
        'Taxa_Crescimento': [0.85, 0.25, 0.45, 0.12, 1.95, 0.65, 0.10, 3.85, -1.50, 0.50]
    }
    df_limpo = pd.DataFrame(dados_mock)
    st.sidebar.info("💡 Exibindo base simulada do Censo. Faça upload do seu próprio CSV para atualizar.")

# Filtros Funcionais na Barra Lateral
st.sidebar.subheader("🎛️ Filtros do Cenário")
regioes = df_limpo['Regiao'].unique()
regioes_sel = st.sidebar.multiselect("Filtrar por Região", options=regioes, default=regioes)

df_filtrado = df_limpo[df_limpo['Regiao'].isin(regioes_sel)]

anos = sorted(df_filtrado['Ano'].unique())
ano_sel = st.sidebar.selectbox("Ano do Censo/Pesquisa", options=anos)

df_final = df_filtrado[df_filtrado['Ano'] == ano_sel]

# Execução da Página Principal do Indicador
st.title("📊 Indicador: População e Crescimento Demográfico")
st.markdown("### Demandantes: Prefeitos de Capitais (Revisão de Planos Diretores)")
st.markdown("---")

# =========================================================================
# CRITÉRIO 2: RIGOR ESTATÍSTICO E PERGUNTA DE NEGÓCIO
# =========================================================================
valores = df_final['Taxa_Crescimento'].dropna().to_numpy()

if len(valores) > 0:
    # Cálculos estatísticos obrigatórios usando NumPy
    media = np.mean(valores)
    mediana = np.median(valores)
    q1 = np.percentile(valores, 25)
    q3 = np.percentile(valores, 75)
    iqr = q3 - q1
    amplitude = np.max(valores) - np.min(valores)
    desvio_padrao = np.std(valores, ddof=1) if len(valores) > 1 else 0.0
    
    # Regra rigorosa de 1,5xIQR para detecção de anomalias/outliers
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    outliers_df = df_final[(df_final['Taxa_Crescimento'] < limite_inferior) | (df_final['Taxa_Crescimento'] > limite_superior)]
    
    # Exibição de KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Média Aritmética", f"{media:.2f}%")
    kpi2.metric("Mediana (Robusta)", f"{mediana:.2f}%")
    kpi3.metric("Amplitude Territorial", f"{amplitude:.2f}%")
    kpi4.metric("Desvio Padrão (Homogeneidade)", f"{desvio_padrao:.2f}%")
    
    # Diagnóstico Estatístico
    st.markdown("#### 🧠 Diagnóstico Estatístico da Consultoria")
    if media > mediana:
        st.warning(f"**Assimetria Positiva:** A média ({media:.2f}%) é maior que a mediana ({mediana:.2f}%). Isso prova que existem cidades isoladas crescendo em ritmo explosivo (*outliers*), inflando artificialmente o índice médio geral.")
    else:
        st.info(f"**Distribuição Equilibrada:** A média ({media:.2f}%) está próxima ou abaixo da mediana ({mediana:.2f}%), indicando um crescimento populacional mais homogêneo entre as cidades filtradas.")
        
    # =========================================================================
    # CRITÉRIO 3: VISUALIZAÇÃO DE DADOS E CONTEÚDO ADICIONAL
    # =========================================================================
    st.markdown("---")
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.markdown("**Análise Quântica e de Dispersão (Boxplot)**")
        fig_box = px.box(df_final, y="Taxa_Crescimento", points="all",
                         title="Boxplot Interativo com Quartis e Identificação de Outliers",
                         labels={"Taxa_Crescimento": "Taxa de Crescimento Geométrico (%)"})
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_graf2:
        st.markdown("**Velocidade de Crescimento (Ranking de Cidades)**")
        df_top = df_final.nlargest(10, 'Taxa_Crescimento')
        fig_bar = px.bar(df_top, x="Município", y="Taxa_Crescimento", 
                         title="Top Municípios com Maior Crescimento Demográfico",
                         color="Taxa_Crescimento", color_continuous_scale="Viridis")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # Elemento visual extra: Pirâmide Etária Simulada exigida no cenário da persona
    st.markdown("---")
    st.markdown("**Transição Demográfica Nacional (Cenário de Envelhecimento)**")
    
    faixas_etarias = ['80+', '70-79', '60-69', '50-59', '40-49', '30-39', '20-29', '10-19', '0-9']
    homens_piramide = [-2.1, -3.4, -4.8, -6.2, -7.5, -8.1, -8.5, -7.9, -7.2]
    mulheres_piramide = [3.2, 4.1, 5.5, 6.8, 7.9, 8.4, 8.6, 7.8, 7.0]

    fig_piramide = go.Figure()
    fig_piramide.add_trace(go.Bar(y=faixas_etarias, x=homens_piramide, name='Homens', orientation='h', marker=dict(color='RoyalBlue')))
    fig_piramide.add_trace(go.Bar(y=faixas_etarias, x=mulheres_piramide, name='Mulheres', orientation='h', marker=dict(color='Crimson')))
    fig_piramide.update_layout(title='Pirâmide Etária Brasileira Ilustrativa (Impacto no Planejamento Urbano)',
                              barmode='overlay', bargap=0.1,
                              xaxis=dict(tickvals=[-8, -6, -4, -2, 0, 2, 4, 6, 8], ticktext=['8%', '6%', '4%', '2%', '0', '2%', '4%', '6%', '8%']))
    st.plotly_chart(fig_piramide, use_container_width=True)

    # Tabela Dinâmica de Outliers Detectados
    st.subheader("🚨 Cidades Classificadas como Outliers Estatísticos")
    st.write(f"Municípios cujo crescimento ficou totalmente fora das barreiras normais calculadas por IQR (Abaixo de **{limite_inferior:.2f}%** ou Acima de **{limite_superior:.2f}%**):")
    if not outliers_df.empty:
        st.dataframe(outliers_df[['Município', 'Regiao', 'Taxa_Crescimento']].sort_values(by='Taxa_Crescimento', ascending=False))
    else:
        st.success("Nenhuma cidade classificada como outlier extremo nos filtros selecionados.")
        
else:
    st.error("Por favor, selecione pelo menos uma Região na barra lateral para calcular as estatísticas.")

# Bloco Contextual de Mídia
st.markdown("---")
st.subheader("📰 Bloco Contextual: Economia do Cuidado & Transição Demográfica")
col_midia1, col_midia2 = st.columns(2)
with col_midia1:
    st.markdown("""
    **O Envelhecimento Populacional e os Planos Diretores**
    Os Censos mais recentes apontam que a base da pirâmide etária brasileira está encolhendo, enquanto o topo (idosos) cresce rapidamente. 
    Prefeitos que ignorarem as taxas próximas a zero ou negativas de crescimento demográfico correm o risco de construir estruturas públicas que ficarão vazias.
    """)
with col_midia2:
    st.info("💡 **Dica de Consultor:** Cidades classificadas como *outliers positivos* (crescimento explosivo) exigem zoneamento rígido e contenção de perímetro urbano para evitar o colapso do transporte coletivo e favelização.")
