import streamlit as st
import pandas as pd
import numpy as np 

st.title('Usuários')
st.markdown('Painel de usuários e suas permissões')
st.sidebar.markdown('- Aqui podemos verificar os usuários cadastrados, suas permissões e quando eles foram cadastrados.')
    
tab1, tab2 = st.tabs(['Usuários', 'Remover Usuários'])

with tab1:
    st.markdown('## Usuários Cadastrados')
    df = pd.read_csv('./data/usuarios.csv')
    st.dataframe(df)

with tab2:
    st.markdown('## Remover usuários')

    with st.form("my_second_form"):
        st.write("Remover Usuário")
        # Adicionar lista dos usuários depois ***** 
        selected_user = st.selectbox("Selecione um usuário para apagar", ["User 1", 'User 2'])

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Usuário: ", selected_user, " removido com sucesso ✅")