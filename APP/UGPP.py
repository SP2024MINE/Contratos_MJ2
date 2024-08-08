from msilib import add_data
import streamlit as st
from sodapy import Socrata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
 
st.title('Contratos')
st.write('Aplicativo para contratos')
 
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
df['proveedor_adjudicado'] = df['proveedor_adjudicado'].str.title()
 
# Filtros de Búsqueda
st.sidebar.header('Filtros')
start_date = st.sidebar.date_input('Fecha de inicio', pd.to_datetime('2018-01-01'))
end_date = st.sidebar.date_input('Fecha de fin', pd.to_datetime('2023-01-01'))
 
entidad = st.selectbox('Entidad', df['nombre_entidad'].unique()) 

# Gráficos
st.header('Gráficos')
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
 
modalidad = st.selectbox('Seleccione la modalidad', df['modalidad_de_contratacion'].unique())

 
# Métricas
 
df_filtrado = df[df['modalidad_de_contratacion'] == modalidad]

st.header('Métricas')
total_valor = df_filtrado['valor_del_contrato'].sum()
total_contratos = len(df_filtrado)
promedio = df_filtrado['valor_del_contrato'].mean()
st.metric('Monto Total Contratado', f'${total_valor:,.2f}')
st.metric('Número Total de Contratos', total_contratos)
st.metric('Promedio del Monto por Contrato', f'${promedio:,.2f}')

 

# Listar los contratistas con mayor numero de contratos y el monto total contratado


st.header('Análisis de Contratistas')

dataset_contratista = df.filter(items=['proveedor_adjudicado', 'valor_del_contrato'])
dataset_contratista['suma_contratos'] = 1


contratistas_agrupados = dataset_contratista.groupby('proveedor_adjudicado').agg(
    numero_contratos=('suma_contratos', 'count'),
    monto_total=('valor_del_contrato', 'sum')
    )

contratistas_ordenados = contratistas_agrupados.sort_values(by=['numero_contratos', 'monto_total'], ascending=[False, False])
contratistas_ordenados


contratista = st.selectbox('Seleccione el contratista', df['proveedor_adjudicado'].str.title())

df_filtrado1 = dataset_contratista[dataset_contratista['proveedor_adjudicado'] == contratista]

st.header('Métricas')
total_valor1 = df_filtrado1['valor_del_contrato'].sum()
total_contratos1 = len(df_filtrado1)
promedio1 = df_filtrado1['valor_del_contrato'].mean()
st.metric('Monto Total Contratado', f'${total_valor1:,.2f}')
st.metric('Número Total de Contratos', total_contratos1)
st.metric('Promedio del Monto por Contrato', f'${promedio1:,.2f}')