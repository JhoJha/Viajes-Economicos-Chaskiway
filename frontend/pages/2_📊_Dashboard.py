# Al principio de frontend/pages/2_📊_Dashboard.py

import streamlit as st
import pandas as pd
import altair as alt  # Una excelente librería para gráficos

# Importamos NUESTRA función compartida desde el archivo utils
from frontend.utils import load_data

# ¡Y listo! Con esta línea ya tienen todos los datos.
df = load_data()