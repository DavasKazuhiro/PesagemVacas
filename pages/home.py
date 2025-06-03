import streamlit as st
import pandas as pd
import numpy as np 

st.title('Dashboard')
st.markdown('Bem vindo ao Dashboard da Fazenda Exprimental Gralha Azul')
st.sidebar.markdown('- Essa página é dedicada para verificar informações gerais de forma rápida e prática!')
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Gráfico 1")
    chart_data_1 = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data_1)

with col2:
    st.markdown("#### Gráfico 2")
    chart_data_2 = pd.DataFrame(np.random.randn(20, 2), columns=["a", "b"])
    st.line_chart(chart_data_2)

with col3:
    st.markdown("#### Gráfico 3")
    chart_data_3 = pd.DataFrame(np.random.randn(15, 2), columns=["a", "b"])
    st.bar_chart(chart_data_3)

    
st.markdown('## Pesagens Recentes')
df = pd.read_csv('./data/pesagens_vacas.csv')
df['Pesagem'] = pd.to_datetime(df['Pesagem'])
df['Pesagem'] = df['Pesagem'].dt.strftime('%H:%M | %d/%m ')

st.dataframe(df)