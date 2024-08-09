# Contratos UGPP

Universidad Externado de Colombia*

![python311](https://img.shields.io/badge/python-3.12-blue) 
![pandas2.2.2](https://img.shields.io/badge/pandas-2.2.2-blue)
![streamlit](https://img.shields.io/badge/Streamlit-blue)
![socrata](https://img.shields.io/badge/Socrata-blue)
![license](https://img.shields.io/badge/license-MIT-green)


## Descripción

 Se realizó una APP con la base de datos de contratos extraída de [Datos Abiertos de Colombia](https://www.datos.gov.co/). En donde en la primera sección se visualiza la descripción de contratos por modalidad de contratación, el comportamiento en valor de los mismos durante el tiempo y una pie chart para ver la participación de la misma, seguido a ello se pueden ver las métricas (Monto Total Contrato, Número Total de Contratos Y precio  promedio del contrato) por modalidad, Por último se encuentra esta información desglosada por contratista. 

 ## **MIT License** 

Para mayor información puede consultar el archivo de [Licencia](https://github.com/SP2024MINE/Contratos_MJ2/blob/main/LICENSE)


## Pasos para Configurar el Proyecto

### 1. Crear el Ambiente de Trabajo
1. Instalar Python 3.10 o superior.
2. Instalar conda si no está instalado. Puede descargarse desde [Conda](https://docs.conda.io/en/latest/miniconda.html).
3. Crear y activar el ambiente virtual con conda:
   ```bash
   conda create --name myenv python=3.10
   conda activate myenv
   ```

### 2. Gestionar Dependencias con Poetry
1. Instalar Poetry siguiendo las instrucciones en su [sitio oficial](https://python-poetry.org/docs/#installation).
2. Iniciar un nuevo proyecto con Poetry:
   ```bash
   poetry init
   ```
3. Añadir las dependencias necesarias:
   ```bash
   poetry add streamlit pandas requests sodapy
   ```

### 3. Gestión del Repositorio en GitHub
1. Crear un repositorio en la organización de GitHub de la clase [SP2024MINE](https://github.com/SP2024MINE).
2. Clonar el repositorio en la máquina local:
   ```bash
   git clone https://github.com/SP2024MINE/your-repo-name.git
   cd your-repo-name
   ```
3. Añadir y realizar commit de los archivos generados por Poetry:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### 4. Consultar Datos usando Socrata
1. Seleccionar una entidad pública de interés cuyos datos estén disponibles en el portal Socrata.
2. Consultar los datos de contratación utilizando la librería `sodapy`:
   ```python
   from sodapy import Socrata
   import pandas as pd

   client = Socrata("www.datos.gov", None)
   results = client.get("xxxx", limit=1000)  # Reemplazar 'xxxx' con el endpoint específico
   df = pd.DataFrame.from_records(results)
   ```

### 5. Desarrollo de la Webapp con Streamlit
1. Crear un archivo `app.py` en el proyecto y desarrollar la webapp:
   ```python
   import streamlit as st
   import pandas as pd
   from sodapy import Socrata

   st.title("Consulta de Datos de Contratación")

   # Configuración de la API Socrata
   client = Socrata("www.datos.gov", None)

   # Solicitud de datos
   @st.cache
   def load_data():
       results = client.get("xxxx", limit=1000)  # Reemplazar 'xxxx' con el endpoint específico
       return pd.DataFrame.from_records(results)

   df = load_data()

   # Mostrar datos
   st.write(df)
   ```


## Contacto

Para comunicarse con los creadores del contenido,  lo puede hacer mediante el correo electrónico xxxx@est.uexternado.edu.co