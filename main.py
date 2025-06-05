import streamlit as st

st.set_page_config(page_title='Fazendo Exprimental Gralha Azul', page_icon='🦜', layout='wide')

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    placeholder = st.empty()
    actual_email = "vini"
    actual_password = "123"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Digite suas credenciais")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and email == actual_email and password == actual_password:
        placeholder.empty()
        st.success("Login realizado com sucesso!")
        st.session_state.logged_in = True
        st.rerun()

    elif submit and email != actual_email and password != actual_password:
        st.error("Login incorreto. Tente novamente.")
        
    else:
        pass
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

sidebar_logo = 'images/n_logo.png'
st.logo(sidebar_logo, icon_image=sidebar_logo, size='large')
sd = st.sidebar.title('Gralha Azul')
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