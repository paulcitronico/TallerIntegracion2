import streamlit as st

import casos_region
import vista_deis
import vista_icovid
import casos_comuna
import casos_activos
import defunciones_registro

# cd Downloads\Python\Streamlit\Covid-19
# streamlit run app.py   

# Config
st.beta_set_page_config(
    page_title="Covid-19 Chile",
 	layout="centered",
 	initial_sidebar_state="expanded",
)

# Sidebar   
st.sidebar.title('Navegación')
opt = st.sidebar.radio("",
    ("Casos por región",
    "Casos por comuna",
    "Defunciones Registro Civil",
    "Deis-DATOS",
    "ICOVID-DATOS",
    "Casos Activos",
    )
)

if opt == "Casos por región":
    casos_region.main()

if opt == "Deis-DATOS":
    vista_deis.main()

if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "ICOVID-DATOS":
    vista_icovid.main()

if opt == "Casos por comuna":
    casos_comuna.main()

if opt == "Casos Activos":
    casos_activos.main()