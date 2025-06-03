import streamlit as st
import pandas as pd
import numpy as np 

st.title('Usuários')
st.markdown('Painel de usuários e suas permissões')
st.sidebar.markdown('- Aqui podemos verificar os usuários cadastrados, suas permissões e quando eles foram cadastrados.')
st.divider()
    
st.markdown('## Pesagens Recentes')
df = pd.read_csv('./data/usuarios.csv')

st.dataframe(df)