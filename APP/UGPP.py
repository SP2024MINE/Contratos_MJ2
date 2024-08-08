from msilib import add_data
import streamlit as st
from sodapy import Socrata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
 
st.title('contratos')
st.write('Mi primer aplicativo para contratos')
 
## Selector de contratos, cargo dsatos de contrtos desde sodapy y le permito al usuario escoger un contrato a visualizar
 
client = Socrata("www.datos.gov.co","xv66xLFwvXNRjMns6TbebGarR")
 
Query = """
select
    id_contrato, nombre_entidad, departamento, modalidad_de_contratacion, valor_del_contrato, fecha_de_firma, proveedor_adjudicado
where
    nombre_entidad LIKE 'UNIDAD DE GESTION PENSIONAL Y PARAFISCALES - UGPP'
limit
10000000
"""
 
results=client.get("jbjy-vk9h",query = Query)
 
df = pd.DataFrame.from_records(results)
 
df['valor_del_contrato'] = df ['valor_del_contrato'].astype(float)
df['fecha_de_firma'] = pd.to_datetime(df['fecha_de_firma'], format='mixed')
 
# Filtros de Búsqueda
st.sidebar.header('Filtros')
start_date = st.sidebar.date_input('Fecha de inicio', pd.to_datetime('2018-01-01'))
end_date = st.sidebar.date_input('Fecha de fin', pd.to_datetime('2023-01-01'))
 
modalidad = st.selectbox('Seleccione la modalidad', df['modalidad_de_contratacion'].unique())
 
# Métricas
 
st.header('Métricas')
total_valor = df['valor_del_contrato'].sum()
total_contratos = len(df)
promedio = df['valor_del_contrato'].mean()
st.metric('Monto Total Contratado', f'${total_valor:,.2f}')
st.metric('Número Total de Contratos', total_contratos)
st.metric('Promedio del Monto por Contrato', f'${promedio:,.2f}')
st.header('Gráficos')
 
# Gráficos
 
bar_chart = alt.Chart(df).mark_bar().encode(
    x='count()',
    y='modalidad_de_contratacion',
    color='modalidad_de_contratacion')
st.altair_chart(bar_chart, use_container_width=True)
 
 
# Gráfico de Líneas
 
line_chart = alt.Chart(df).mark_line().encode(
    x='fecha_de_firma',
    y='sum(valor_del_contrato)')
st.altair_chart(line_chart, use_container_width=True)
 
# Gráfico Circular (Pie Chart)
 
pie_chart = alt.Chart(df).mark_arc().encode(
    theta=alt.Theta(field='valor_del_contrato', type='quantitative'),
    color=alt.Color(field='modalidad_de_contratacion', type='nominal')
)
 
st.altair_chart(pie_chart, use_container_width=True)
 
# Listar los contratistas con mayor numero de contratos y el monto total contratado