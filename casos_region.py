import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import datetime
import calendar
import plotly.graph_objects as go
import plotly.express as px

@st.cache
#carga los datos y los segrega por region y fecha
def cargar_datos():
	URL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_T.csv"
	df = pd.read_csv(URL)
	df = df.rename(columns={"Region": "fecha"})
	df["fecha"] = pd.to_datetime(df["fecha"])
	df = df.set_index("fecha")
	df = df.sort_index()
	return df

@st.cache
#carga los datos y los segrega por region y poblacion
def cargar_poblacion():
    URL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR.csv"
    df = pd.read_csv(URL)
    df = df[["Region", "Poblacion"]]
    df = df.set_index("Region")
    return df

#retorna la grafica 
def graficaRegional(df, value_name, title, option="Normal"):
	df = df.reset_index()
	df = pd.melt(df, id_vars=["fecha"], var_name="Región" , value_name=value_name)

	fig = go.Figure()
	for i, reg in enumerate(list(set(df['Región']))):
		aux = df[df['Región'] == reg]
		fig.add_trace(go.Scatter(x=aux['fecha'], y=aux['casos confirmados'], name=reg, marker_color=px.colors.qualitative.G10[i], mode='lines'))
	fig.update_layout(
        title=title,
        xaxis_title="Fecha",
        yaxis_title="Casos confirmados",
        template='ggplot2',
        height=550
    )
	

	return fig
#metodo principal
def main():
	st.sidebar.markdown('---')

	df = cargar_datos()
	options = list(df.columns) + ["Todas las regiones"]
	region = st.sidebar.multiselect(
		"Elegir regiones", options, ["Atacama", "Ñuble", "Magallanes"]
	)

	if region[0] == "Todas las regiones":
		region = list(df.columns)

	start_date = st.sidebar.date_input('Fecha de inicio', df.index[0])
	end_date = st.sidebar.date_input('Fecha de término', df.index[-1])
	if start_date > end_date:
		st.sidebar.error('Error: La fecha de término debe ser después de la fecha de inicio.')

	opciones = ["Total de casos confirmados acumulados", "Total de casos confirmados acumulados por 100.000 habitantes", "Nuevos casos confirmados", "Nuevos casos confirmados por 100.000 habitantes"]
	plot = st.selectbox(
		"Elegir gráfico", opciones
	)

	if plot == "Nuevos casos confirmados":
		df = df.T
		df[pd.to_datetime("2020-03-02")] = [0 for i in range(len(df.index))]
		df = df.T
		df = df.sort_index()
		df = df.diff()
	elif plot == "Total de casos confirmados acumulados por 100.000 habitantes":
		pop = cargar_poblacion()
		df = df.T
		pop = pop.reset_index().append({"Region": "Total", "Poblacion": pop["Poblacion"].sum()}, ignore_index=True)
		pop = pop.set_index("Region")
		df["Población"] = pop
		df = df.apply(lambda x: 100000*x[:-1]/x[-1], axis=1)
		df = df.T
	elif plot == "Nuevos casos confirmados por 100.000 habitantes":
		df = df.T
		df[pd.to_datetime("2020-03-02")] = [0 for i in range(len(df.index))]
		df = df.T
		df = df.sort_index()
		df = df.diff()
		pop = cargar_poblacion()
		df = df.T
		pop = pop.reset_index().append({"Region": "Total", "Poblacion": pop["Poblacion"].sum()}, ignore_index=True)
		pop = pop.set_index("Region")
		df["Población"] = pop
		df = df.apply(lambda x: 100000*x[:-1]/x[-1], axis=1)
		df = df.T

	df = df[region].loc[start_date:end_date]

	if plot == "Total de casos confirmados acumulados":
		st.title("Evolución del total de casos confirmados acumulados por región")
	elif plot == "Total de casos confirmados acumulados por 100.000 habitantes":
		st.title("Evolución del total de casos confirmados acumulados por 100.000 habitantes/tasa de incidencia acumulada por región")
	elif plot == "Nuevos casos confirmados":
		st.title("Evolución de nuevos casos confirmados por región")
	else:
		st.title("Evolución de nuevos casos confirmados por 100.000 habitantes/tasa de incidencia por región")
		
	df = df.sort_index(ascending=False)
	show_df = st.checkbox("Mostrar datos")
	if show_df:
		st.write(df)

	df = df.sort_index(ascending=True)
	pm = st.sidebar.checkbox("Suavizar/Promedio móvil 7 días", True)
	if pm:
		df = df.rolling(window=7).mean()
	if plot == "Total de casos confirmados acumulados":
		title = "Total de casos confirmados acumulados*"
	elif plot == "Total de casos confirmados acumulados por 100.000 habitantes":
		title = "Total de casos confirmados acumulados por 100.000 habitantes*"
	elif plot == "Nuevos casos confirmados":
		title = "Nuevos casos confirmados*"
	else:
		title = "Nuevos casos confirmados por 100.000 habitantes*"

	fig = graficaRegional(df, "casos confirmados", title)
	st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()