import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache
#carga los datos por comuna
def cargar_datos():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto45/CasosConfirmadosPorComuna_std.csv')
    df['Numero Semana'] = [int(semana.split('SE')[1]) for semana in df['Semana Epidemiologica']]
    df['Casos 100 mil'] = 100000*df['Casos confirmados']/df['Poblacion']
    return df

@st.cache
#carga los datos de inicio de los sintomas
def carga_datos_comienzo_sintomas():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomas_std.csv')
    df['Numero Semana'] = [int(semana.split('SE')[1]) for semana in df['Semana Epidemiologica']]
    df['Casos 100 mil'] = 100000*df['Casos confirmados']/df['Poblacion']
    return df

#metodo que retorna los casos por comuna
def graficoxComuna(df, comunas, op, op_data, op_plot):
    fig = go.Figure()
    for i, comuna in enumerate(comunas):
        aux = df[df['Comuna']==comuna]
        if op:
            y = aux['Casos 100 mil']
        else:
            y = aux['Casos confirmados']
        if op_plot == 'Barras':
            fig.add_trace(go.Bar(x=aux['Numero Semana'], y=y, name=comuna, marker_color=px.colors.qualitative.G10[i]))
        if op_plot == 'Lineas':
            fig.add_trace(go.Scatter(x=aux['Numero Semana'], y=y, name=comuna, marker_color=px.colors.qualitative.G10[i], mode='lines'))
    fig.update_layout(
        barmode='group',
        title=f'{op_data} por semana epidemiológica',
        xaxis_title="Semana epidemiológica",
        yaxis_title="Casos",
        template='ggplot2',
        height=550
    )
    return fig
# metodo que genera un mapa de calor 
def graficoTermico(df, comunas, op, op_data):
    data = df[df['Comuna'].isin(comunas)]
    if op:
        z = data['Casos 100 mil']
    else:
        z = data['Casos confirmados']

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=data['Numero Semana'],
        y=data['Comuna'],   
        colorscale='inferno_r'
        ))

    fig.update_layout(
        title=f'{op_data} por semana epidemiológica',
        xaxis_title="Semana epidemiológica",
        template='ggplot2',
        autosize=False,
        height=300 + 25*len(comunas) ,
    )

    return fig

#metodo principal
def main():
    st.title('Casos por comuna')
    
    st.sidebar.markdown('---')
    st.sidebar.markdown('Opciones')
    op_data = st.sidebar.selectbox('Datos', ['Casos confirmados','Casos nuevos por fecha de inicio de síntomas'], key=0)
    
    if op_data == 'Casos confirmados':
        df = cargar_datos()
    if op_data == 'Casos nuevos por fecha de inicio de síntomas':
        df = carga_datos_comienzo_sintomas()

    op_plot = st.sidebar.selectbox('Tipo gráfico', ['Lineas','Barras','Heatmap'])
    op = st.sidebar.checkbox('Ver casos por 100.000 habitantes', value=False, key=0)

    comunas = list(set(df['Comuna']))
    select = st.multiselect('Seleccionar comunas', comunas, ['Antofagasta','Puente Alto','Punta Arenas'])

    if op_plot != 'Heatmap':
        try:
            fig = graficoxComuna(df, select, op, op_data, op_plot)
            st.plotly_chart(fig, use_container_width=True) 
        except:
            st.write('Demasiadas comunas seleccionadas')
    else:
        fig = graficoTermico(df, select, op, op_data)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()