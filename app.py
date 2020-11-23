import streamlit as st

import defunciones_registro
import casos_region
import vista_deis
import ocupacion_hospitalaria
import vista_icovid
import reporte_diario
import casos_comuna
import casos_activos
import casos_grupo_etario

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
    "Defunciones Deis",
    "Ocupación Hospitalaria",
    "Positivad ICOVID",
    "Casos Activos",
    "Rango Etario",
    )
)

if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "Casos por región":
    casos_region.main()

if opt == "Defunciones Deis":
    vista_deis.main()

if opt == "Ocupación Hospitalaria":
    ocupacion_hospitalaria.main()

if opt == "Positivad ICOVID":
    vista_icovid.main()

if opt == "Casos por comuna":
    casos_comuna.main()

if opt == "Casos Activos":
    casos_activos.main()

if opt == "Rango Etario":
    casos_grupo_etario.main()