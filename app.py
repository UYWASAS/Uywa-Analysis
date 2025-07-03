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
        font-family: 'Montserrat', 'Arial', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6, .stTitle, .stHeader, .stSubheader {
        color: #19345c !important;
    }
    .stMarkdown, .stText, .stCaption, .stDataFrame, .stTabs, .stTab, .stMetric, .stAlert, .stExpander, .stNumberInput, .stSlider, .stSelectbox {
        color: #222 !important;
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

# ===================== SIMULADOR PRODUCTIVO =====================
elif menu == "Simulador Productivo":
    st.header("Simulador Productivo Mejorado")
    st.write("""
    Simula el desempeño productivo de tu lote con base en parámetros genéticos y manejo.
    """)
    # Parámetros editables
    st.subheader("Parámetros del Lote")
    col1, col2, col3 = st.columns(3)
    linea = col1.selectbox("Línea genética", ["Cobb", "Ross"])
    edad = col2.selectbox("Edad (días)", [28, 35, 42, 49])
    num_aves = col3.number_input("Número de aves", min_value=1000, value=10000, step=100)

    # Busca parámetros de referencia
    ref = datos_geneticos_base[(datos_geneticos_base["linea"] == linea) & (datos_geneticos_base["edad"] == edad)]
    if not ref.empty:
        peso_ref = ref["peso"].values[0]
        consumo_ref = ref["consumo"].values[0]
        fcr_ref = ref["fcr"].values[0]
    else:
        peso_ref = consumo_ref = fcr_ref = np.nan

    st.subheader("Resultados Esperados (Referencia Genética)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Peso final (kg)", f"{peso_ref:.2f}")
    col2.metric("Consumo (kg/ave)", f"{consumo_ref:.2f}")
    col3.metric("FCR", f"{fcr_ref:.2f}")

    st.subheader("Ajusta Parámetros Productivos")
    peso_real = st.number_input("Peso final real (kg)", min_value=0.5, max_value=5.0, value=float(peso_ref), step=0.01)
    consumo_real = st.number_input("Consumo real (kg/ave)", min_value=1.0, max_value=10.0, value=float(consumo_ref), step=0.01)
    fcr_real = st.number_input("FCR real", min_value=1.0, max_value=3.0, value=float(fcr_ref), step=0.01)
    st.write("Puedes comparar tus propios resultados contra la referencia.")

    st.subheader("Resumen del Lote")
    st.write(f"- **Línea:** {linea}")
    st.write(f"- **Edad:** {edad} días")
    st.write(f"- **N° de aves:** {num_aves:,}")
    st.write(f"- **Peso final:** {peso_real:.2f} kg/ave")
    st.write(f"- **Consumo:** {consumo_real:.2f} kg/ave")
    st.write(f"- **FCR:** {fcr_real:.2f}")

# ===================== SIMULADOR ECONÓMICO =====================
elif menu == "Simulador Económico":
    st.header("Simulador Económico Interactivo")
    st.write("""
    Calcula los costos y retornos económicos del lote de aves.
    """)
    # Parámetros económicos
    st.subheader("Parámetros Económicos")
    costo_pollo = st.number_input("Costo de pollo vivo ($/kg)", min_value=0.5, value=1.2, step=0.01)
    precio_venta = st.number_input("Precio de venta ($/kg)", min_value=0.5, value=1.8, step=0.01)
    costo_dieta = st.number_input("Costo de dieta ($/kg)", min_value=0.1, value=0.35, step=0.01)
    num_aves = st.number_input("N° de aves", min_value=1000, value=10000, step=100)
    peso_final = st.number_input("Peso final (kg/ave)", min_value=0.5, value=2.5, step=0.01)
    consumo_ave = st.number_input("Consumo total (kg/ave)", min_value=1.0, value=4.5, step=0.01)

    st.subheader("Resultados Económicos")
    ingreso = num_aves * peso_final * precio_venta
    costo_total = num_aves * consumo_ave * costo_dieta
    margen = ingreso - costo_total
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"${ingreso:,.2f}")
    col2.metric("Costo total dieta", f"${costo_total:,.2f}")
    col3.metric("Margen", f"${margen:,.2f}")

    st.write("Ajusta los parámetros para simular diferentes escenarios económicos.")

# ===================== COMPARADOR DE ESCENARIOS =====================
elif menu == "Comparador de Escenarios":
    st.header("Comparador de Escenarios Productivos y Económicos")
    st.write("""
    Compara dos escenarios de manejo/producto para tomar decisiones.
    """)
    st.subheader("Escenario 1")
    col1, col2 = st.columns(2)
    peso1 = col1.number_input("Peso final 1 (kg)", value=2.5, key="peso1")
    costo1 = col2.number_input("Costo dieta 1 ($/ave)", value=1.50, key="costo1")
    margen1 = peso1 * 1.8 - costo1

    st.subheader("Escenario 2")
    col1, col2 = st.columns(2)
    peso2 = col1.number_input("Peso final 2 (kg)", value=2.7, key="peso2")
    costo2 = col2.number_input("Costo dieta 2 ($/ave)", value=1.65, key="costo2")
    margen2 = peso2 * 1.8 - costo2

    st.subheader("Comparativo")
    df_comp = pd.DataFrame({
        "Escenario": ["Escenario 1", "Escenario 2"],
        "Peso final (kg)": [peso1, peso2],
        "Costo dieta ($/ave)": [costo1, costo2],
        "Margen ($/ave)": [margen1, margen2]
    })
    st.dataframe(df_comp, hide_index=True)
    st.write("Usa este comparador para analizar cambios en peso, costo o precio.")
