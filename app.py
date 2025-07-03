import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gestión y Análisis de Dietas", layout="wide")

# ----------- ESTILO CORPORATIVO -----------
st.markdown(
    """
    <style>
    body, .stApp {
        background: linear-gradient(120deg, #f3f6fa 0%, #e3ecf7 100%) !important;
    }
    .stSidebar, .stSidebarContent, .stSidebar * {
        background: #19345c !important;
        color: #fff !important;
    }
    section.main, section.main * {
        color: #19345c !important;
        font-family: 'Montserrat', 'Arial', sans-serif !important;
    }
    section.main > div:first-child {
        background: #fff !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 32px 0 rgba(32, 64, 128, 0.11), 0 2px 8px 0 rgba(32,64,128,0.04) !important;
        padding: 2.5rem 2rem 2rem 2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        min-height: 70vh !important;
    }
    h1, h2, h3, h4, h5, h6, .stTitle, .stHeader, .stSubheader, .stMarkdown, .stText, .stCaption {
        color: #19345c !important;
    }
    label, .stNumberInput label, .stTextInput label, .stSelectbox label, .stMultiSelect label, .stCheckbox label, .stRadio label {
        color: #19345c !important;
        font-weight: 600 !important;
    }
    .stNumberInput input, .stTextInput input, .stSelectbox, .stMultiSelect {
        background: #f4f8fa !important;
        border-radius: 6px !important;
        color: #19345c !important;
    }
    .stButton>button {
        background-color: #204080 !important;
        color: #fff !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("nombre_archivo_logo.png", width=90)
    st.markdown(
        """
        <div style='text-align: center;'>
            <div style='font-size:24px;font-family:Montserrat,Arial;color:#fff; margin-top: 10px;letter-spacing:1px;'>
                <b>UYWA-NUTRITION<sup>®</sup></b>
            </div>
            <div style='font-size:13px;color:#fff; margin-top: 5px; font-family:Montserrat,Arial;'>
                Nutrición de Precisión Basada en Evidencia
            </div>
            <hr style='border-top:1px solid #2e4771; margin: 10px 0;'>
            <div style='font-size:12px;color:#fff; margin-top: 8px;'>
                <b>Contacto:</b> uywasas@gmail.com<br>
                Derechos reservados © 2025
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("Gestión y Análisis de Dietas")

menu = st.sidebar.radio(
    "Selecciona una sección",
    [
        "Análisis de Dieta",
        "Simulador Productivo",
        "Simulador Económico",
        "Comparador de Escenarios"
    ]
)

@st.cache_data
def cargar_archivo(file):
    if file is None:
        return None
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file, sheet_name=0)

if 'ingredientes' not in st.session_state:
    st.session_state['ingredientes'] = None

datos_geneticos_base = pd.DataFrame({
    "linea": ["Cobb", "Cobb", "Cobb", "Cobb", "Ross", "Ross", "Ross", "Ross"],
    "edad": [28, 35, 42, 49, 28, 35, 42, 49],
    "peso": [1.35, 1.95, 2.5, 3.05, 1.35, 1.95, 2.5, 3.05],
    "consumo": [2.2, 3.1, 4.3, 5.6, 2.2, 3.1, 4.3, 5.6],
    "fcr": [1.63, 1.59, 1.72, 1.84, 1.63, 1.59, 1.72, 1.84]
})

if "genetica_edit" not in st.session_state:
    st.session_state["genetica_edit"] = datos_geneticos_base.copy()
elif not isinstance(st.session_state["genetica_edit"], pd.DataFrame):
    st.session_state["genetica_edit"] = datos_geneticos_base.copy()

if 'escenarios_guardados' not in st.session_state:
    st.session_state['escenarios_guardados'] = []

if 'escenarios_eco' not in st.session_state:
    st.session_state['escenarios_eco'] = []

# ===================== ANÁLISIS DE DIETA =====================
if menu == "Análisis de Dieta":
    st.header("Matriz de Ingredientes Editable")
    ingredientes_data = {
        "Ingrediente": ["Maíz", "Sorgo", "Soja", "Harina de carne", "Aceite", "Sal", "Premix"],
        "Precio ($/kg)": [0.28, 0.22, 0.42, 0.60, 1.00, 0.18, 0.80],
        "Energía (kcal/kg)": [3350, 3200, 2400, 2100, 8800, 0, 0],
        "Proteína (%)": [8.5, 9.0, 46.0, 52.0, 0, 0, 0],
        "Lisina (%)": [0.25, 0.23, 2.85, 3.10, 0, 0, 0.1],
        "Calcio (%)": [0.02, 0.02, 0.30, 5.50, 0, 0, 1.5],
    }
    df_ingredientes = pd.DataFrame(ingredientes_data)
    df_ingredientes = st.data_editor(df_ingredientes, num_rows="dynamic", key="ingredientes_edit")

    st.header("Dieta del Cliente (editable)")
    dieta_data = {
        "Ingrediente": ["Maíz", "Soja", "Harina de carne", "Premix"],
        "Proporción (%)": [60, 25, 10, 5]
    }
    df_dieta = pd.DataFrame(dieta_data)
    df_dieta = st.data_editor(df_dieta, num_rows="dynamic", key="dieta_edit")

    st.subheader("Aportes Nutricionales y Costo de la Dieta")
    df = pd.merge(df_dieta, df_ingredientes, on="Ingrediente", how="left")
    df["Proporción (kg)"] = df["Proporción (%)"] / 100
    df["Costo ($/100kg)"] = df["Proporción (kg)"] * df["Precio ($/kg)"] * 100
    for nutr in ["Energía (kcal/kg)", "Proteína (%)", "Lisina (%)", "Calcio (%)"]:
        df[f"Aporte {nutr}"] = df["Proporción (kg)"] * df[nutr]

    st.write(df[[
        "Ingrediente", "Proporción (%)", "Precio ($/kg)", "Costo ($/100kg)", 
        "Aporte Energía (kcal/kg)", "Aporte Proteína (%)", "Aporte Lisina (%)", "Aporte Calcio (%)"
    ]])

    costo_total = df["Costo ($/100kg)"].sum()
    energia_total = df["Aporte Energía (kcal/kg)"].sum()
    proteina_total = df["Aporte Proteína (%)"].sum()
    lisina_total = df["Aporte Lisina (%)"].sum()
    calcio_total = df["Aporte Calcio (%)"].sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Costo total", f"${costo_total:.2f}/100kg")
    col2.metric("Energía", f"{energia_total:.0f} kcal/kg")
    col3.metric("Proteína", f"{proteina_total:.2f} %")
    col4.metric("Lisina", f"{lisina_total:.2f} %")
    col5.metric("Calcio", f"{calcio_total:.2f} %")

    st.info("Puede editar en vivo los precios y proporciones arriba para analizar nuevas soluciones en tiempo real.")

    st.markdown("""
    **Notas:**  
    - Este análisis es una referencia rápida. Para cambios grandes, revise que los requerimientos nutricionales globales se mantengan.
    """)

# ===================== SIMULADOR PRODUCTIVO Y ECONÓMICO =====================
elif menu == "Simulador Productivo":
    st.header("Simulador Productivo Mejorado")
    # (Aquí va tu código previo del simulador productivo...)

elif menu == "Simulador Económico":
    st.header("Simulador Económico Interactivo")
    # (Aquí va tu código previo del simulador económico...)

elif menu == "Comparador de Escenarios":
    st.header("Comparador de Escenarios Productivos y Económicos")
    # (Aquí va tu código previo del comparador...)
