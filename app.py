import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Estudo Bloqueios x Reanálise",
    layout="wide",
    page_icon=":bar_chart:"
)

# Carrega os dados
@st.cache_data
def load_data():
    df_raw = pd.read_excel("estudo bloqueios py.xlsx", sheet_name="tabela", header=None)
    df = df_raw.iloc[1:16, 0:7]  # 7 colunas corretas
    df.columns = ["Bloqueios", "Jan", "Fev", "Mar", "Abr", "Total Geral", "Porcentagem"]
    df.reset_index(drop=True, inplace=True)
    
    df["Total Geral"] = pd.to_numeric(df["Total Geral"], errors="coerce")
    df["Porcentagem"] = pd.to_numeric(df["Porcentagem"], errors="coerce")
    df["Porcentagem"] = (df["Porcentagem"] / 1).apply(lambda x: f"{x:.2%}")
    return df

df = load_data()

# CABEÇALHO customizado
col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    st.markdown("""
    <div style='display: flex; align-items: center;'>
        <h1 style='color: red; margin: 0;'>GED</h1>
        <h1 style='color: black; margin: 0 0 0 10px;'>| ESTUDO BLOQUEIOS X REANÁLISE</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.image("claro_logo.png", width=80)  # <-- usando sua imagem local

st.markdown("<hr style='border: 2px solid red;'>", unsafe_allow_html=True)

# Conteúdo
st.subheader("Resumo Mensal")
st.dataframe(df, use_container_width=True)

# Transformar para formato "long" para o gráfico de barras
df_long = df.melt(
    id_vars=["Bloqueios"],
    value_vars=["Jan", "Fev", "Mar", "Abr"],
    var_name="Mês",
    value_name="Quantidade"
)

# Gráfico de Barras
st.subheader("Contagem por Categoria e Mês")
bar_fig = px.bar(
    df_long,
    x="Mês",
    y="Quantidade",
    color="Bloqueios",
    barmode="group",
    title="Contagem de Resumos por Mês",
    text_auto=True,
    template="plotly_white"
)
bar_fig.update_layout(
    xaxis_title="Mês",
    yaxis_title="Quantidade",
    legend_title="Bloqueios",
    template="plotly_white"  # Forçando o tema aqui também
)
st.plotly_chart(bar_fig, use_container_width=True)

# Adicionar seletor de mês
mes_selecionado = st.selectbox("Selecione o mês para o gráfico de pizza:", ["Jan", "Fev", "Mar", "Abr", "Total Geral"])

# Filtrar dados para o mês selecionado
df_mes = df[["Bloqueios", mes_selecionado]].copy()
df_mes.columns = ["Bloqueios", "Quantidade"]

# Gráfico de Pizza
st.subheader(f"Distribuição Total por Categoria - {mes_selecionado}")
pie_fig = px.pie(
    df_mes,
    names="Bloqueios",
    values="Quantidade",
    title=f"Distribuição Percentual por Categoria - {mes_selecionado}",
    template="plotly_white"
)
pie_fig.update_layout(template="plotly_white")  # Forçando o tema aqui também
st.plotly_chart(pie_fig, use_container_width=True)
