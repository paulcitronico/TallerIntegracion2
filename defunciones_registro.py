import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

@st.cache

#Extrae los datos
def cargar_datos():
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto32/Defunciones_std.csv')
    df["Año"] = [df["Fecha"][i].split("-")[0] for i in range(df.shape[0])]
    df["Mes"] = [df["Fecha"][i].split("-")[1] for i in range(df.shape[0])]
    df["Dia"] = [df["Fecha"][i].split("-")[2] for i in range(df.shape[0])]
    df = df[[int(df['Año'][i])>=2016 for i in range(df.shape[0])]].reset_index(drop=True)
    l_semana = [datetime.datetime.strptime(df["Fecha"][i], '%Y-%m-%d').date().isocalendar()[1] for i in range(df.shape[0])]
    df['Semana'] = l_semana

    data = df.groupby(['Año','Semana','Region','Comuna'],as_index=False).sum()
    data = data.drop(columns=['Codigo region','Codigo comuna'])
    return data

#Crea el grafico a nivel nacional
def grafico_nacional(dfs):
    fig = go.Figure()
    colors = ["seagreen","teal","deepskyblue","gray","red"]
    grouped = dfs.groupby("Año")
    i = 0
    for year, group in grouped:
        l_semana = []
        l_def = []
        grouped2 = group.groupby("Semana")
        for semana, group2 in grouped2:
            l_semana.append(semana)
            l_def.append(sum(group2["Defunciones"]))

        fig.add_trace(go.Scatter(x=l_semana[1:-1], y=l_def[1:-1],
                        mode='lines',
                        name=year,
                        marker_color=colors[i]))

        i += 1

    fig.update_layout(
        title_text='Defunciones inscritas en Chile',
        xaxis_title='Número de semana',
        height=550)
    return fig

#Crea el grafico de region
def grafica_region(dfs, region):
    dfs = dfs[dfs['Region']==region]
    fig = go.Figure()
    colors = ["seagreen","teal","deepskyblue","gray","red"]
    grouped = dfs.groupby("Año")
    i = 0
    for year, group in grouped:
        l_semana = []
        l_def = []
        grouped2 = group.groupby("Semana")
        for semana, group2 in grouped2:
            l_semana.append(semana)
            l_def.append(sum(group2["Defunciones"]))
        fig.add_trace(go.Scatter(x=l_semana[1:-1], y=l_def[1:-1],
                    mode='lines',
                    name=year,
                    marker_color=colors[i]))
        i += 1
    fig.update_layout(
        title_text=f'Defunciones inscritas en Región {region}', 
        xaxis_title='Número de semana',
        height=550)
    return fig

#Clase principal
def main():
    st.title("Defunciones inscritas Registro Civil")

    st.header('Datos')
    st.write('Cantidad de defunciones inscritas en el Registro Civil por número de semana.')
    df = cargar_datos()
    show_df = st.checkbox('Mostrar datos')
    if show_df:
        st.write(df.sort_values(by="Año"))

    st.header('Gráfico Nacional')
    fig = grafico_nacional(df)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Gráfico por regiones')
    regiones = list(set(df['Region']))
    reg = st.selectbox('Region', regiones, index=regiones.index('Metropolitana de Santiago'))
    fig = grafica_region(df, reg)
    st.plotly_chart(fig, use_container_width=True) 

    

if __name__ == "__main__":
    main()