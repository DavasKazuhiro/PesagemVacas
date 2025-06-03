import streamlit as st

st.set_page_config(page_title='Fazendo Exprimental Gralha Azul', page_icon='🦜', layout='wide')

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")      

home = st.Page("pages/home.py", title="Home", icon="🐮")
users = st.Page("pages/users.py", title="Usuários", icon="👤")
dashboards = st.Page("pages/dashboards.py", title="Análises", icon="📊")
reports = st.Page("pages/reports.py", title="Relatórios", icon="📑")
config = st.Page("pages/config.py", title="Config", icon="⚙")


sd = st.sidebar.title('🦜 Gralha Azul')

if st.session_state.logged_in:
    pg = st.navigation(
        {
        "Páginas Principais": [home, users, dashboards, reports], 
        "Configurações" : [config, logout_page]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()