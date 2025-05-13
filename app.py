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
 df = df_raw.iloc[1:15, 0:8]
 df.columns = ["Bloqueios", "Jan", "Fev", "Mar", "Abr", "Mai", "Total Geral", "Porcentagem"]
 df.reset_index(drop=True, inplace=True)
 
 df["Total Geral"] = pd.to_numeric(df["Total Geral"], errors="coerce")
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
 st.image("claro_logo.png", width=80)

st.markdown("<hr style='border: 2px solid red;'>", unsafe_allow_html=True)

# Seleção de meses
meses_selecionados = st.multiselect(
 "Selecione os meses para visualizar os dados:",
 options=["Jan", "Fev", "Mar", "Abr", "Mai", "Total Geral"],
 default=["Jan", "Fev", "Mar", "Abr", "Mai"]
)

# Filtrar dados para os meses selecionados
df_selecionado = df[["Bloqueios"] + meses_selecionados]

# Conteúdo
st.subheader("Resumo Mensal")
st.dataframe(df_selecionado, use_container_width=True)

# Transformar para formato "long" para o gráfico de barras
df_long = df_selecionado.melt(
 id_vars=["Bloqueios"],
 value_vars=meses_selecionados,
 var_name="Mês",
 value_name="Quantidade"
)

st.subheader("Bloqueios por mês")
bar_fig = px.bar(
 df_long,
 x="Mês",
 y="Quantidade",
 color="Bloqueios",
 barmode="group",
 title="Contagem de bloqueios por Mês",
 text_auto=True,
)
bar_fig.update_layout(
 xaxis_title="Mês",
 yaxis_title="Quantidade",
 legend_title="Bloqueios",
 uniformtext_minsize=8,
 uniformtext_mode='hide',
 template="plotly_white"
)
st.plotly_chart(bar_fig, use_container_width=True)

# Gráfico de Pizza
st.subheader("Distribuição Total por Categoria")
pie_fig = px.pie(
 df_long,
 names="Bloqueios",
 values="Quantidade",
 title="Distribuição Percentual por Categoria",
 hole=0.3
)
pie_fig.update_traces(textinfo='percent')
st.plotly_chart(pie_fig, use_container_width=True)

st.text("Última atualização: 13/05/2025")