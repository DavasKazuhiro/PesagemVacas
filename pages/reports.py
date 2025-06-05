import streamlit as st
import pandas as pd
import numpy as np 

st.title('Relatórios')
st.markdown('Relatórios e dados disponíveis para download')
st.sidebar.markdown('- Adicionar descrição.')

tab1, tab2, tab3 = st.tabs(['Vacas', 'Pesagens', 'Medidas'])

with tab1:
    st.markdown('## Tabela Vacas')

with tab2:
    st.markdown('## Tabela Pesagens')

with tab3:
    st.markdown('## Tabela Medidas')