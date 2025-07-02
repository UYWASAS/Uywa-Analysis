import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Inteligencia Productiva Avícola", layout="wide")

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
    .stSidebar input[type="radio"], .stSidebar input[type="checkbox"] {
        accent-color: #fff !important;
        background-color: #fff !important;
        border: 2px solid #fff !important;
    }
    .stSidebar .stRadio [data-baseweb="radio"] > div:first-child {
        border: 2px solid #fff !important;
        background: #19345c !important;
    }
    .stSidebar .stRadio [data-baseweb="radio"] svg {
        color: #fff !important;
        fill: #fff !important;
    }
    .stSidebar .stRadio [aria-checked="true"] svg {
        color: #ff5656 !important;
        fill: #ff5656 !important;
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
    /* Tablas y dataframes: texto SIEMPRE visible */
    .stDataFrame, .stDataFrame * {
        color: #19345c !important;
    }
    .stTable, .stTable td, .stTable th {
        color: #19345c !important;
    }
    div[data-testid="stDataFrame"] table, 
    div[data-testid="stDataFrame"] td, 
    div[data-testid="stDataFrame"] th {
        color: #19345c !important;
    }
    .stDataFrame, .dataframe, .stTable, .stDataFrame * {
        background: #f9fbfd !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background-color: #204080 !important;
        color: #fff !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    button[title="Browse files"] {
        color: #204080 !important;
        font-weight: 700 !important;
        background: #fff !important;
        border: 2px solid #204080 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }
    button[title="Browse files"]:hover {
        background: #204080 !important;
        color: #fff !important;
        border: 2px solid #204080 !important;
    }
    div[data-testid="stFileUploaderDropzone"] {
        border: 1.5px solid #204080 !important;
        border-radius: 12px !important;
        background: #f8fafc !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #19345c !important;
        background: transparent !important;
    }
    div[data-testid="stDataFrame"] td, 
    div[data-testid="stDataFrame"] th {
        color: #19345c !important;
        background: transparent !important;
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
        return pd.read_excel(file, sheet_name=0)

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
    lin = st.file_uploader("Líneas genéticas (csv/xlsx, ambas líneas en una hoja, columna 'linea')", type=["csv", "xlsx"])
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
        nombre_col = "Ingrediente"
        precio_col = "precio"  # cambia si tu archivo tiene otro nombre para el precio

        nutrientes = [col for col in df_ing.columns if col not in [nombre_col, precio_col]]

        for nutr in nutrientes:
            df_ing[nutr] = pd.to_numeric(df_ing[nutr], errors='coerce')

        seleccionados = st.multiselect("Selecciona ingredientes", df_ing[nombre_col].tolist())
        proporciones = []
        for ingr in seleccionados:
            prop = st.number_input(f"% de {ingr}", min_value=0.0, max_value=100.0, value=10.0)
            proporciones.append(prop)
        if seleccionados and sum(proporciones) > 0:
            df_formula = pd.DataFrame({"ingrediente": seleccionados, "proporcion": proporciones})
            df_formula["proporcion"] = df_formula["proporcion"] / 100
            st.dataframe(df_formula)

            # Calcular aportes de todos los nutrientes y mostrar en tabla
            resultado = {}
            for nutr in nutrientes:
                valores_nutr = df_ing.set_index(nombre_col)[nutr].reindex(df_formula["ingrediente"]).values
                resultado[nutr] = (df_formula["proporcion"] * valores_nutr).sum()
            df_resultado = pd.DataFrame(resultado, index=["Aporte total"])
            st.subheader("Aportes de nutrientes (por tonelada)")
            st.dataframe(df_resultado.T, use_container_width=True)  # Nutrientes como filas

            # Costo total
            if precio_col in df_ing.columns:
                precios = df_ing.set_index(nombre_col)[precio_col].reindex(df_formula["ingrediente"]).values
                costo_total = (df_formula["proporcion"] * precios).sum()
                st.success(f"Costo estimado por tonelada: U$D {costo_total:,.2f}")

elif menu == "Simulador Productivo":
    st.header("Simulador Productivo Mejorado")
    df_lineas = st.session_state['lineas']
    if df_lineas is not None and 'linea' in df_lineas.columns:
        # Mostramos todas las genéticas cargadas
        st.subheader("Curva genética de referencia:")
        st.dataframe(df_lineas)
        # Selector de línea genética
        lineas_disponibles = list(df_lineas['linea'].unique())
        linea_sel = st.selectbox("Selecciona línea genética", lineas_disponibles)
        df_gen = df_lineas[df_lineas['linea'] == linea_sel].copy().reset_index(drop=True)
        st.success(f"Línea seleccionada: {linea_sel}")
        st.dataframe(df_gen)

        # Parámetro a graficar
        opciones_grafico = {
            "Peso (kg)": "peso",
            "Consumo acumulado (kg)": "consumo",
            "FCR": "fcr"
        }
        grafico_sel = st.selectbox("¿Qué quieres graficar?", list(opciones_grafico.keys()))
        col_grafico = opciones_grafico[grafico_sel]

        # Entradas del usuario
        aves_ini = st.number_input("Aves iniciales", min_value=1000, max_value=100000, value=10000)
        mortalidad = st.number_input("Mortalidad (%)", min_value=0.0, max_value=20.0, value=5.0)
        edad_salida = st.number_input("Edad de salida (días)", min_value=1, max_value=int(df_gen['edad'].max()), value=42)
        peso_final = st.number_input("Peso final esperado (kg)", min_value=0.5, max_value=5.0, value=2.5)
        consumo_total = st.number_input("Consumo acumulado (kg/ave)", min_value=1.0, max_value=10.0, value=4.5)

        aves_finales = aves_ini * (1 - mortalidad/100)
        fcr_real = consumo_total / peso_final if peso_final > 0 else np.nan

        # Genética referencia
        fila_ref = df_gen[df_gen['edad'] == edad_salida]
        if not fila_ref.empty:
            peso_ref = float(fila_ref['peso'].values[0])
            consumo_ref = float(fila_ref['consumo'].values[0])
            fcr_ref = float(fila_ref['fcr'].values[0]) if 'fcr' in fila_ref.columns else consumo_ref / peso_ref
            desvio_peso = peso_final - peso_ref
            desvio_porc = 100 * desvio_peso / peso_ref
            st.markdown(f"""
            **Resultados respecto a genética**  
            - Peso ideal genética: {peso_ref:.2f} kg  
            - Peso final simulado: {peso_final:.2f} kg  
            - Desviación: {desvio_peso:+.2f} kg ({desvio_porc:+.1f}%)  
            - Consumo ideal genética: {consumo_ref:.2f} kg  
            - Consumo simulado: {consumo_total:.2f} kg  
            - FCR genética: {fcr_ref:.2f}  
            - FCR simulado: {fcr_real:.2f}  
            - Mortalidad: {mortalidad:.2f}%  
            - Aves vendibles: {aves_finales:.0f}  
            """)
            if abs(desvio_porc) > 5:
                st.error("¡Atención! El peso final se desvía más de un 5% respecto a la genética.")
            else:
                st.success("El peso final está dentro del rango esperado para la genética.")

            # Gráfico: curva seleccionada vs punto simulado
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_gen['edad'], y=df_gen[col_grafico], mode="lines+markers", name=f"Curva {grafico_sel} {linea_sel}"))
            # Poner el punto simulado sólo si corresponde
            y_sim = None
            if col_grafico == "peso":
                y_sim = peso_final
            elif col_grafico == "consumo":
                y_sim = consumo_total
            elif col_grafico == "fcr":
                y_sim = fcr_real
            if y_sim is not None:
                fig.add_trace(go.Scatter(
                    x=[edad_salida], y=[y_sim], mode="markers+text", name="Simulación usuario",
                    marker=dict(size=16, color="red", symbol="x"),
                    text=["Simulación"], textposition="top center"
                ))
            fig.update_layout(
                title=f"{grafico_sel} vs Edad",
                xaxis_title="Edad (días)", 
                yaxis_title=grafico_sel
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No se encontró la edad seleccionada en la curva genética.")
    else:
        st.warning("Debes cargar un archivo de líneas genéticas con columna 'linea' para comparar.")

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
