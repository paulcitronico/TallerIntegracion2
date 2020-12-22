import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
#Extraer datos de comuna
def cargar_datos_comuna():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto55/Positividad_por_comuna.csv')
    return df

@st.cache
#Extraer datos de region
def cagar_datos_regional():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto55/Positividad_por_region.csv')
    return df

#Crea el grafico de comuna
def grafica_Comunal(df, comunas, op):
    fig = go.Figure()
    for i, comuna in enumerate(comunas):
        aux = df[df['Comuna']==comuna]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        if op:
            y = aux['positividad'].rolling(7).mean()
        else:
            y = aux['positividad']
        fig.add_trace(go.Scatter(
            x=aux['fecha'],
            y=100*y,
            name=str(comuna),
            mode='lines',
            marker_color=(px.colors.qualitative.D3+px.colors.qualitative.Safe)[i]
            
        ))
    fig.update_layout(
        title_text="Positividad Exámenes PCR",
        xaxis_title="Fecha",
        yaxis_title="Porcentaje Positividad",
        template='ggplot2',
        height=550
    )
    return fig

#Crea el grafico de region
def grafica_regional(df, regiones, op):
    fig = go.Figure()
    for i, region in enumerate(regiones):
        aux = df[df['Region']==region]
        aux = aux.sort_values(by=['fecha']).reset_index(drop=True)
        if op:
            y = aux['positividad'].rolling(7).mean()
        else:
            y = aux['positividad']
        fig.add_trace(go.Scatter(
            x=aux['fecha'],
            y=100*y,
            name=str(region),
            mode='lines',
            marker_color=px.colors.qualitative.G10[i]
        ))
    fig.update_layout(
        title_text="Positividad Exámenes PCR",
        xaxis_title="Fecha",
        yaxis_title="Porcentaje Positividad",
        template='ggplot2',
        height=550
    )
    return fig

#Clase principal
def main():
    st.title('Positividad ICOVID Chile')

    st.write('''
        Datos provistos por el grupo [ICOVID Chile](https://www.icovidchile.cl/) y el 
        Ministerio de Ciencia en su [producto 55](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto55).
    ''')

    st.header('Vista regional')
    
    df = cagar_datos_regional()
    l_reg = list(set(df['Region']))
    l_reg = [x for x in l_reg if str(x)!='nan']   
    regiones = st.multiselect('Regiones', l_reg, ['Antofagasta','Coquimbo','Metropolitana','Magallanes'], key=0)

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True, key=0)
    fig = grafica_regional(df, regiones, op)
    st.plotly_chart(fig, use_container_width=True) 

    st.header('Vista comunal')

    df = cargar_datos_comuna()
    regiones = list(set(df['Region']))
    reg = st.selectbox('Region', regiones, index=regiones.index('Metropolitana'))
    df_reg = df[df['Region']==reg].reset_index(drop=True)

    l_comunas = list(set(df_reg['Comuna']))

    cant = len(l_comunas)
    if cant > 10:
        cant = 10

    comunas = st.multiselect('Comunas', l_comunas, l_comunas[:cant], key=1)

    op = st.checkbox("Suavizar datos (Promedio móvil 7 días)", value=True, key=1)
    try:
        fig = grafica_Comunal(df, comunas, op)
        st.plotly_chart(fig, use_container_width=True) 
    except:
        st.write('Demasiadas comunas seleccionadas')

if __name__ == "__main__":
    main()