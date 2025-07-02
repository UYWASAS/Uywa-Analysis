import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Inteligencia Productiva Avícola", layout="wide")

# ----------- ESTILO CORPORATIVO: Sidebar y centro legibles -----------
st.markdown(
    """
    <style>
    /* Fondo general */
    body, .stApp {
        background: linear-gradient(120deg, #f3f6fa 0%, #e3ecf7 100%) !important;
    }
    /* Sidebar */
    .stSidebar, .stSidebarContent, .stSidebar * {
        background: #19345c !important;
        color: #fff !important;
    }
    /* Centro: Forzar textos oscuros en todo el main */
    section.main, section.main * {
        color: #19345c !important;
        font-family: 'Montserrat', 'Arial', sans-serif !important;
    }
    /* Área principal blanca y con sombra */
    section.main > div:first-child {
        background: #fff !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 32px 0 rgba(32, 64, 128, 0.11), 0 2px 8px 0 rgba(32,64,128,0.04) !important;
        padding: 2.5rem 2rem 2rem 2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        min-height: 70vh !important;
    }
    /* Títulos y textos principales */
    h1, h2, h3, h4, h5, h6, .stTitle, .stHeader, .stSubheader, .stMarkdown, .stText, .stCaption {
        color: #19345c !important;
    }
    /* Labels y entradas de widgets */
    label, .stNumberInput label, .stTextInput label, .stSelectbox label, .stMultiSelect label, .stCheckbox label, .stRadio label {
        color: #19345c !important;
        font-weight: 600 !important;
    }
    .stNumberInput input, .stTextInput input, .stSelectbox, .stMultiSelect {
        background: #f4f8fa !important;
        border-radius: 6px !important;
        color: #19345c !important;
    }
    /* Tablas */
    .stDataFrame, .dataframe, .stTable, .stDataFrame * {
        background: #f9fbfd !important;
        color: #19345c !important;
        border-radius: 10px !important;
    }
    /* Botones */
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

# -------------------- LOGO Y MARCA EN LA SIDEBAR --------------------
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

st.title("Módulo de Inteligencia Productiva Avícola")

menu = st.sidebar.radio(
    "Selecciona una sección",
    [
        "Carga de Datos",
        "Formulación de Dieta",
        "Simulador Productivo",
        "Simulador Económico",
        "Comparador de Escenarios",
    ]
)

@st.cache_data
def cargar_archivo(file):
    if file is None:
        return None
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if 'ingredientes' not in st.session_state:
    st.session_state['ingredientes'] = None
if 'lineas' not in st.session_state:
    st.session_state['lineas'] = None
if 'precios' not in st.session_state:
    st.session_state['precios'] = None

if menu == "Carga de Datos":
    st.header("Carga de Datos de Entrada")
    ing = st.file_uploader("Ingredientes (csv/xlsx)", type=["csv", "xlsx"])
    if ing: 
        df_ing = cargar_archivo(ing)
        st.session_state['ingredientes'] = df_ing
        st.success("Ingredientes cargados.")
        st.dataframe(df_ing)
    lin = st.file_uploader("Líneas genéticas (csv/xlsx)", type=["csv", "xlsx"])
    if lin:
        df_lin = cargar_archivo(lin)
        st.session_state['lineas'] = df_lin
        st.success("Líneas genéticas cargadas.")
        st.dataframe(df_lin)
    pre = st.file_uploader("Precios de venta (csv/xlsx)", type=["csv", "xlsx"])
    if pre:
        df_pre = cargar_archivo(pre)
        st.session_state['precios'] = df_pre
        st.success("Precios cargados.")
        st.dataframe(df_pre)

elif menu == "Formulación de Dieta":
    st.header("Panel de Formulación de Dieta")
    df_ing = st.session_state['ingredientes']
    if df_ing is None:
        st.warning("Primero debes cargar los ingredientes.")
    else:
        seleccionados = st.multiselect("Selecciona ingredientes", df_ing['nombre'].tolist())
        proporciones = []
        for ingr in seleccionados:
            prop = st.number_input(f"% de {ingr}", min_value=0.0, max_value=100.0, value=10.0)
            proporciones.append(prop)
        if seleccionados and sum(proporciones) > 0:
            df_formula = pd.DataFrame({"ingrediente": seleccionados, "proporcion": proporciones})
            df_formula["proporcion"] = df_formula["proporcion"] / 100
            st.dataframe(df_formula)
            nutrientes = ["proteina", "energia", "lisina", "metionina", "Ca", "P"]
            resultado = {}
            for nutr in nutrientes:
                resultado[nutr] = (df_formula["proporcion"] *
                    df_ing.set_index("nombre")[nutr].reindex(df_formula["ingrediente"]).values).sum()
            st.subheader("Aportes de nutrientes (por tonelada)")
            st.json(resultado)
            precios = df_ing.set_index("nombre")["precio"].reindex(df_formula["ingrediente"]).values
            costo_total = (df_formula["proporcion"] * precios).sum()
            st.success(f"Costo estimado por tonelada: U$D {costo_total:,.2f}")

elif menu == "Simulador Productivo":
    st.header("Simulador Productivo")
    df_lin = st.session_state['lineas']
    if df_lin is not None:
        st.write("Curva genética de referencia:")
        st.dataframe(df_lin)
    edad = st.number_input("Edad de salida (días)", min_value=1, max_value=70, value=42)
    peso = st.number_input("Peso final esperado (kg)", min_value=0.5, max_value=5.0, value=2.5)
    consumo = st.number_input("Consumo acumulado (kg)", min_value=1.0, max_value=10.0, value=4.5)
    fcr = st.number_input("Conversión alimenticia (FCR)", min_value=1.2, max_value=2.5, value=1.8)
    st.write(f"Peso final: {peso} kg | Consumo acumulado: {consumo} kg | FCR: {fcr}")
    if df_lin is not None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_lin["edad"], y=df_lin["peso"], mode="lines+markers", name="Curva ideal"))
        fig.add_trace(go.Scatter(x=[edad], y=[peso], mode="markers", name="Resultado simulado"))
        fig.update_layout(title="Curva de crecimiento", xaxis_title="Edad (días)", yaxis_title="Peso (kg)")
        st.plotly_chart(fig)

elif menu == "Simulador Económico":
    st.header("Simulador Económico")
    costo_ton = st.number_input("Costo dieta por tonelada (USD)", min_value=200., max_value=1000., value=450.)
    consumo_ave = st.number_input("Consumo por ave (kg)", min_value=1.0, max_value=10.0, value=4.5)
    peso_ave = st.number_input("Peso final por ave (kg)", min_value=0.5, max_value=7.0, value=2.5)
    precio_kg = st.number_input("Precio venta por kg vivo (USD)", min_value=0.5, max_value=4.0, value=2.0)
    costo_ave = consumo_ave * costo_ton / 1000
    ingreso_ave = peso_ave * precio_kg
    margen = ingreso_ave - costo_ave
    st.write(f"Costo por ave: U$D {costo_ave:.2f}")
    st.write(f"Ingreso por ave: U$D {ingreso_ave:.2f}")
    st.success(f"Margen neto por ave: U$D {margen:.2f}")

elif menu == "Comparador de Escenarios":
    st.header("Comparador de Escenarios")
    formula1 = st.text_input("Fórmula 1", "Fórmula A")
    margen1 = st.number_input("Margen por ave fórmula 1", value=0.45, key="m1")
    formula2 = st.text_input("Fórmula 2", "Fórmula B")
    margen2 = st.number_input("Margen por ave fórmula 2", value=0.55, key="m2")
    fig = go.Figure([
        go.Bar(name=formula1, x=["Margen"], y=[margen1]),
        go.Bar(name=formula2, x=["Margen"], y=[margen2])
    ])
    fig.update_layout(barmode='group', title="Comparativo de margen por ave")
    st.plotly_chart(fig)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:11px;color:#fff;text-align:center'>Desarrollado como MVP para <b>UYWA-NUTRITION®</b></div>",
    unsafe_allow_html=True
)
