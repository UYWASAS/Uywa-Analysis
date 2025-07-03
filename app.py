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

# ---------------------- SIMULADOR PRODUCTIVO ----------------------
elif menu == "Simulador Productivo":
    st.header("Simulador Productivo Mejorado")

    with st.expander("Mostrar y editar genética cargada"):
        df_edit = st.data_editor(
            st.session_state["genetica_edit"], 
            num_rows="dynamic", 
            use_container_width=True, 
            key="edit_genetica"
        )
        if st.button("Guardar cambios en la genética"):
            st.session_state["genetica_edit"] = df_edit
            st.success("¡Cambios guardados!")
    df_lineas = st.session_state["genetica_edit"].copy()

    st.subheader("Parámetros de simulación e interacción")
    col1, col2, col3 = st.columns(3)
    with col1:
        lineas_disponibles = list(df_lineas['linea'].unique())
        linea_sel = st.selectbox("Selecciona línea genética", lineas_disponibles)
        edad_inicial = st.number_input("Edad inicial (días)", min_value=0, max_value=40, value=0)
        aves_ini = st.number_input("Aves iniciales", min_value=1000, max_value=100000, value=10000)
    with col2:
        mortalidad = st.slider("Mortalidad (%)", 0.0, 20.0, 5.0, 0.1)
        edad_salida = st.selectbox("Edad de salida (días)", sorted(df_lineas[df_lineas['linea']==linea_sel]['edad'].unique()), index=2)
        precio_alimento_kg = st.slider("Precio alimento (USD/kg)", 0.20, 1.50, 0.50, 0.01)
    with col3:
        precio_venta_kg = st.slider("Precio venta pollo vivo (USD/kg)", 0.5, 4.0, 2.0, 0.01)
        df_gen = df_lineas[df_lineas['linea'] == linea_sel].copy().reset_index(drop=True)
        peso_sug = float(df_gen[df_gen['edad'] == edad_salida]['peso'].values[0])
        consumo_sug = float(df_gen[df_gen['edad'] == edad_salida]['consumo'].values[0])
        peso_final = st.number_input("Peso final esperado (kg)", min_value=0.5, max_value=5.0, value=peso_sug)
        consumo_total = st.number_input("Consumo acumulado (kg/ave)", min_value=1.0, max_value=10.0, value=consumo_sug)

    aves_finales = aves_ini * (1 - mortalidad/100)
    try:
        peso_inicial = float(df_gen[df_gen['edad'] == edad_inicial]['peso'].values[0])
    except:
        peso_inicial = 0.04

    fcr_real = consumo_total / peso_final if peso_final > 0 else np.nan
    gdp = (peso_final - peso_inicial) / (edad_salida - edad_inicial) if (edad_salida - edad_inicial) > 0 else 0
    consumo_diario = consumo_total / edad_salida if edad_salida > 0 else 0
    iep = (peso_final * (aves_finales/aves_ini) * 100) / (edad_salida * fcr_real) if (edad_salida * fcr_real) > 0 else 0
    prod_total = aves_finales * peso_final
    costo_alim = consumo_total * aves_ini * precio_alimento_kg
    ingreso_bruto = prod_total * precio_venta_kg
    margen_neto = ingreso_bruto - costo_alim

    st.markdown("### KPIs productivos y económicos")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("GDP (kg/día)", f"{gdp:.3f}")
    kpi2.metric("IEP", f"{iep:.1f}")
    kpi3.metric("Rentabilidad (USD)", f"{margen_neto:,.2f}")
    kpi4.metric("Producción total carne (kg)", f"{prod_total:,.0f}")

    kpi5, kpi6, kpi7, kpi8 = st.columns(4)
    kpi5.metric("Consumo diario (kg/ave)", f"{consumo_diario:.3f}")
    kpi6.metric("Costo total alimento (USD)", f"{costo_alim:,.2f}")
    kpi7.metric("Ingreso bruto (USD)", f"{ingreso_bruto:,.2f}")
    kpi8.metric("Mortalidad (%)", f"{mortalidad:.2f}")

    st.markdown("---")

    nombre_escenario = st.text_input("Nombre del escenario", f"Escenario {len(st.session_state['escenarios_guardados'])+1}")
    if st.button("Guardar este escenario"):
        st.session_state['escenarios_guardados'].append({
            "nombre": nombre_escenario,
            "linea": linea_sel,
            "edad_ini": edad_inicial,
            "edad_fin": edad_salida,
            "aves_ini": aves_ini,
            "aves_finales": aves_finales,
            "peso_ini": peso_inicial,
            "peso_fin": peso_final,
            "consumo": consumo_total,
            "fcr": fcr_real,
            "gdp": gdp,
            "iep": iep,
            "mortalidad": mortalidad,
            "prod_total": prod_total,
            "costo_alim": costo_alim,
            "precio_alimento_kg": precio_alimento_kg,
            "precio_venta_kg": precio_venta_kg,
            "ingreso_bruto": ingreso_bruto,
            "margen_neto": margen_neto,
            "consumo_diario": consumo_diario
        })
        st.success("¡Escenario guardado!")

    st.markdown("### Visualización de variables")
    tabs = st.tabs([
        "Peso", "Consumo", "FCR", "GDP", "IEP", "Consumo diario", "Producción total", "Rentabilidad", "Gráfico Combinado"
    ])
    edades = df_gen['edad']
    gdp_curve = [ (df_gen.loc[i, "peso"] - df_gen.loc[0, "peso"]) / (df_gen.loc[i,"edad"]-df_gen.loc[0,"edad"]) if (df_gen.loc[i,"edad"]-df_gen.loc[0,"edad"])>0 else 0 for i in range(len(df_gen))]
    iep_curve = [ 
        (df_gen.loc[i, "peso"] * (aves_finales/aves_ini) * 100) / (df_gen.loc[i,"edad"] * df_gen.loc[i,"fcr"])
        if (df_gen.loc[i,"edad"] * df_gen.loc[i,"fcr"])>0 else 0
        for i in range(len(df_gen))
    ]
    consumo_diario_curve = [df_gen.loc[i,"consumo"]/df_gen.loc[i,"edad"] if df_gen.loc[i,"edad"]>0 else 0 for i in range(len(df_gen))]
    prod_total_curve = [aves_finales * df_gen.loc[i,"peso"] for i in range(len(df_gen))]
    rentabilidad_curve = [ (prod_total_curve[i]*precio_venta_kg) - (df_gen.loc[i,"consumo"]*aves_ini*precio_alimento_kg) for i in range(len(df_gen))]
    with tabs[0]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=df_gen['peso'], mode="lines+markers", name="Peso"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[peso_final], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="Peso vs Edad", xaxis_title="Edad (días)", yaxis_title="Peso (kg)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=df_gen['consumo'], mode="lines+markers", name="Consumo"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[consumo_total], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="Consumo vs Edad", xaxis_title="Edad (días)", yaxis_title="Consumo (kg/ave)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=df_gen['fcr'], mode="lines+markers", name="FCR"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[fcr_real], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="FCR vs Edad", xaxis_title="Edad (días)", yaxis_title="FCR")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[3]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=gdp_curve, mode="lines+markers", name="GDP"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[gdp], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="GDP vs Edad", xaxis_title="Edad (días)", yaxis_title="GDP (kg/día)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[4]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=iep_curve, mode="lines+markers", name="IEP"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[iep], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="IEP vs Edad", xaxis_title="Edad (días)", yaxis_title="IEP")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[5]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=consumo_diario_curve, mode="lines+markers", name="Consumo Diario"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[consumo_diario], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="Consumo diario vs Edad", xaxis_title="Edad (días)", yaxis_title="Consumo diario (kg/ave)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[6]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=prod_total_curve, mode="lines+markers", name="Producción total"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[prod_total], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="Producción total carne vs Edad", xaxis_title="Edad (días)", yaxis_title="Producción total (kg)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[7]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edades, y=rentabilidad_curve, mode="lines+markers", name="Rentabilidad"))
        fig.add_trace(go.Scatter(x=[edad_salida], y=[margen_neto], mode="markers", name="Simulación", marker=dict(size=16, color="red")))
        fig.update_layout(title="Rentabilidad vs Edad", xaxis_title="Edad (días)", yaxis_title="Rentabilidad (USD)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs[8]:
        opciones = st.multiselect(
            "Elige las variables a visualizar en el gráfico combinado",
            ["Peso", "Consumo", "FCR", "GDP", "IEP", "Consumo diario", "Producción total", "Rentabilidad"],
            default=["Peso", "Consumo"]
        )
        fig = go.Figure()
        if "Peso" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=df_gen['peso'], mode="lines+markers", name="Peso"))
        if "Consumo" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=df_gen['consumo'], mode="lines+markers", name="Consumo"))
        if "FCR" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=df_gen['fcr'], mode="lines+markers", name="FCR"))
        if "GDP" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=gdp_curve, mode="lines+markers", name="GDP"))
        if "IEP" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=iep_curve, mode="lines+markers", name="IEP"))
        if "Consumo diario" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=consumo_diario_curve, mode="lines+markers", name="Consumo Diario"))
        if "Producción total" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=prod_total_curve, mode="lines+markers", name="Producción total"))
        if "Rentabilidad" in opciones:
            fig.add_trace(go.Scatter(x=edades, y=rentabilidad_curve, mode="lines+markers", name="Rentabilidad"))
        fig.update_layout(title="Variables seleccionadas vs Edad", xaxis_title="Edad (días)")
        st.plotly_chart(fig, use_container_width=True)

    if len(st.session_state['escenarios_guardados']) > 0:
        st.markdown("### Comparador de escenarios guardados")
        df_hist = pd.DataFrame(st.session_state['escenarios_guardados'])
        st.dataframe(df_hist)
        var_comp = st.selectbox("Selecciona variable a comparar", [
            "peso_fin","consumo","fcr","gdp","iep","prod_total","costo_alim","ingreso_bruto","margen_neto","consumo_diario"
        ], format_func=lambda x: {
            "peso_fin":"Peso final",
            "consumo":"Consumo acumulado",
            "fcr":"FCR",
            "gdp":"GDP",
            "iep":"IEP",
            "prod_total":"Producción total",
            "costo_alim":"Costo alimento",
            "ingreso_bruto":"Ingreso bruto",
            "margen_neto":"Rentabilidad",
            "consumo_diario":"Consumo diario"
        }[x])
        fig = go.Figure()
        for idx, row in df_hist.iterrows():
            fig.add_trace(go.Bar(
                name=row["nombre"],
                x=[row["nombre"]], y=[row[var_comp]]
            ))
        fig.update_layout(title=f"Comparativa de {var_comp}", barmode="group")
        st.plotly_chart(fig)

# ---------------------- SIMULADOR ECONOMICO ----------------------
elif menu == "Simulador Económico":
    st.header("Simulador Económico Interactivo")
    col1, col2, col3 = st.columns(3)
    with col1:
        precio_venta = st.slider("Precio venta (USD/kg)", 0.5, 4.0, 2.0, 0.01)
        peso_final = st.slider("Peso final (kg)", 1.0, 4.0, 2.5, 0.1)
    with col2:
        precio_alimento = st.slider("Precio alimento (USD/kg)", 0.2, 1.5, 0.5, 0.01)
        consumo = st.slider("Consumo acumulado (kg/ave)", 2.0, 7.0, 4.5, 0.1)
    with col3:
        aves_ini = st.number_input("Aves iniciales", 1000, 100000, 10000)
        mortalidad = st.slider("Mortalidad (%)", 0.0, 20.0, 5.0, 0.1)
        otros_costos = st.slider("Otros costos por ave (USD)", 0.0, 2.0, 0.5, 0.01)

    aves_finales = aves_ini * (1 - mortalidad/100)
    prod_total = aves_finales * peso_final
    costo_alim = consumo * aves_ini * precio_alimento
    costo_total = costo_alim + aves_ini * otros_costos
    ingreso_bruto = prod_total * precio_venta
    margen_neto = ingreso_bruto - costo_total
    margen_ave = margen_neto / aves_finales if aves_finales > 0 else 0
    rentabilidad = (margen_neto / costo_total)*100 if costo_total>0 else 0

    st.markdown("### KPIs económicos")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Margen neto total (USD)", f"{margen_neto:,.2f}")
    k2.metric("Margen neto por ave (USD)", f"{margen_ave:.2f}")
    k3.metric("Rentabilidad (%)", f"{rentabilidad:.2f}")
    k4.metric("Producción total carne (kg)", f"{prod_total:,.0f}")

    k5, k6, k7 = st.columns(3)
    k5.metric("Costo total alimento (USD)", f"{costo_alim:,.2f}")
    k6.metric("Costo total (USD)", f"{costo_total:,.2f}")
    k7.metric("Ingreso bruto (USD)", f"{ingreso_bruto:,.2f}")

    st.markdown("---")
    tabs_e = st.tabs(["Margen vs Precio Venta", "Margen vs Precio Alimento", "Margen vs Consumo", "Gráfico Combinado"])
    precios_venta = np.linspace(0.5, 4.0, 60)
    margenes_venta = [(prod_total*p - costo_total) for p in precios_venta]
    precios_alim = np.linspace(0.2, 1.5, 60)
    margenes_alim = [(prod_total*precio_venta - (consumo*aves_ini*pa + aves_ini*otros_costos)) for pa in precios_alim]
    consumos = np.linspace(2.0, 7.0, 60)
    margenes_consumo = [(prod_total*precio_venta - (c*aves_ini*precio_alimento + aves_ini*otros_costos)) for c in consumos]
    with tabs_e[0]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=precios_venta, y=margenes_venta, mode="lines", name="Margen neto"))
        fig.add_trace(go.Scatter(x=[precio_venta], y=[margen_neto], mode="markers", marker=dict(size=14, color="red"), name="Simulación actual"))
        fig.update_layout(title="Margen vs Precio Venta", xaxis_title="Precio venta (USD/kg)", yaxis_title="Margen neto (USD)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs_e[1]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=precios_alim, y=margenes_alim, mode="lines", name="Margen neto"))
        fig.add_trace(go.Scatter(x=[precio_alimento], y=[margen_neto], mode="markers", marker=dict(size=14, color="red"), name="Simulación actual"))
        fig.update_layout(title="Margen vs Precio Alimento", xaxis_title="Precio alimento (USD/kg)", yaxis_title="Margen neto (USD)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs_e[2]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=consumos, y=margenes_consumo, mode="lines", name="Margen neto"))
        fig.add_trace(go.Scatter(x=[consumo], y=[margen_neto], mode="markers", marker=dict(size=14, color="red"), name="Simulación actual"))
        fig.update_layout(title="Margen vs Consumo", xaxis_title="Consumo acumulado (kg/ave)", yaxis_title="Margen neto (USD)")
        st.plotly_chart(fig, use_container_width=True)
    with tabs_e[3]:
        opciones_e = st.multiselect(
            "Elige las variables económicas a visualizar",
            ["Margen neto", "Producción total", "Costo total", "Ingreso bruto", "Rentabilidad"],
            default=["Margen neto", "Producción total"]
        )
        fig = go.Figure()
        if "Margen neto" in opciones_e:
            fig.add_trace(go.Scatter(x=[0,1], y=[margen_neto, margen_neto], mode="lines", name="Margen neto"))
        if "Producción total" in opciones_e:
            fig.add_trace(go.Scatter(x=[0,1], y=[prod_total, prod_total], mode="lines", name="Producción total"))
        if "Costo total" in opciones_e:
            fig.add_trace(go.Scatter(x=[0,1], y=[costo_total, costo_total], mode="lines", name="Costo total"))
        if "Ingreso bruto" in opciones_e:
            fig.add_trace(go.Scatter(x=[0,1], y=[ingreso_bruto, ingreso_bruto], mode="lines", name="Ingreso bruto"))
        if "Rentabilidad" in opciones_e:
            fig.add_trace(go.Scatter(x=[0,1], y=[rentabilidad, rentabilidad], mode="lines", name="Rentabilidad (%)"))
        fig.update_layout(title="Variables seleccionadas (escala dummy)", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    nombre_eco = st.text_input("Nombre del escenario económico", f"Económico {len(st.session_state['escenarios_eco'])+1}")
    if st.button("Guardar este escenario económico"):
        st.session_state['escenarios_eco'].append({
            "nombre": nombre_eco,
            "precio_venta": precio_venta,
            "precio_alimento": precio_alimento,
            "peso_final": peso_final,
            "consumo": consumo,
            "aves_ini": aves_ini,
            "aves_finales": aves_finales,
            "mortalidad": mortalidad,
            "prod_total": prod_total,
            "costo_alim": costo_alim,
            "costo_total": costo_total,
            "ingreso_bruto": ingreso_bruto,
            "margen_neto": margen_neto,
            "margen_ave": margen_ave,
            "rentabilidad": rentabilidad,
            "otros_costos": otros_costos
        })
        st.success("¡Escenario económico guardado!")

    if len(st.session_state['escenarios_eco']) > 0:
        st.markdown("### Comparador de escenarios económicos guardados")
        df_eco = pd.DataFrame(st.session_state['escenarios_eco'])
        st.dataframe(df_eco)
        var_comp_e = st.selectbox("Selecciona variable a comparar", [
            "margen_neto","margen_ave","rentabilidad","prod_total","costo_total","ingreso_bruto"
        ], format_func=lambda x: {
            "margen_neto":"Margen neto total",
            "margen_ave":"Margen neto por ave",
            "rentabilidad":"Rentabilidad (%)",
            "prod_total":"Producción total",
            "costo_total":"Costo total",
            "ingreso_bruto":"Ingreso bruto"
        }[x])
        fig = go.Figure()
        for idx, row in df_eco.iterrows():
            fig.add_trace(go.Bar(
                name=row["nombre"],
                x=[row["nombre"]], y=[row[var_comp_e]]
            ))
        fig.update_layout(title=f"Comparativa de {var_comp_e}", barmode="group")
        st.plotly_chart(fig)

# ---------------------- COMPARADOR DE ESCENARIOS ----------------------
elif menu == "Comparador de Escenarios":
    st.header("Comparador de Escenarios Productivos y Económicos")
    if len(st.session_state['escenarios_guardados']) > 0:
        st.markdown("#### Productivos")
        df_hist = pd.DataFrame(st.session_state['escenarios_guardados'])
        st.dataframe(df_hist)
        var_comp = st.selectbox("Variable a comparar (productivo)", [
            "peso_fin","consumo","fcr","gdp","iep","prod_total","costo_alim","ingreso_bruto","margen_neto","consumo_diario"
        ], format_func=lambda x: {
            "peso_fin":"Peso final",
            "consumo":"Consumo acumulado",
            "fcr":"FCR",
            "gdp":"GDP",
            "iep":"IEP",
            "prod_total":"Producción total",
            "costo_alim":"Costo alimento",
            "ingreso_bruto":"Ingreso bruto",
            "margen_neto":"Rentabilidad",
            "consumo_diario":"Consumo diario"
        }[x], key="var_comp_prod")
        fig = go.Figure()
        for idx, row in df_hist.iterrows():
            fig.add_trace(go.Bar(
                name=row["nombre"], x=[row["nombre"]], y=[row[var_comp]]
            ))
        fig.update_layout(title=f"Comparativa de {var_comp}", barmode="group")
        st.plotly_chart(fig)
    else:
        st.info("No hay escenarios productivos guardados aún. Guarda escenarios desde el Simulador Productivo para comparar.")
    if len(st.session_state['escenarios_eco']) > 0:
        st.markdown("#### Económicos")
        df_eco = pd.DataFrame(st.session_state['escenarios_eco'])
        st.dataframe(df_eco)
        var_comp_e = st.selectbox("Variable a comparar (económico)", [
            "margen_neto","margen_ave","rentabilidad","prod_total","costo_total","ingreso_bruto"
        ], format_func=lambda x: {
            "margen_neto":"Margen neto total",
            "margen_ave":"Margen neto por ave",
            "rentabilidad":"Rentabilidad (%)",
            "prod_total":"Producción total",
            "costo_total":"Costo total",
            "ingreso_bruto":"Ingreso bruto"
        }[x], key="var_comp_eco")
        fig = go.Figure()
        for idx, row in df_eco.iterrows():
            fig.add_trace(go.Bar(
                name=row["nombre"], x=[row["nombre"]], y=[row[var_comp_e]]
            ))
        fig.update_layout(title=f"Comparativa de {var_comp_e}", barmode="group")
        st.plotly_chart(fig)
    else:
        st.info("No hay escenarios económicos guardados aún. Guarda escenarios desde el Simulador Económico para comparar.")

# ---------------------- MODELO PREDICTIVO ----------------------
elif menu == "Modelo Predictivo":
    st.header("Modelo Predictivo de Resultados Productivos según Composición Nutricional de la Dieta")
    st.write("Sube tu archivo histórico (csv/xlsx) con los nutrientes analíticos y resultados productivos. Elige la variable productiva a predecir y entrena el modelo. Luego, modifica los nutrientes para predecir el resultado esperado según la dieta propuesta.")

    archivo = st.file_uploader("Carga tu archivo histórico (csv/xlsx)", type=["csv","xlsx"], key="file_predictivo")
    df_hist = None
    if archivo:
        df_hist = cargar_archivo(archivo)
        st.write("Vista previa de tus datos históricos:")
        st.dataframe(df_hist.head(20), use_container_width=True)
        cols = df_hist.columns.str.lower()
        nutrientes_disponibles = [n for n in nutrientes_modelo if n in cols]
        productivos_disponibles = [p for p in productivos_modelo if p in cols]
        if len(nutrientes_disponibles) < 7:
            st.error(f"Tu archivo debe incluir al menos 7 de las siguientes columnas: {nutrientes_modelo}")
        elif len(productivos_disponibles) == 0:
            st.error(f"Tu archivo debe contener al menos una de estas variables productivas como resultado: {productivos_modelo}")
        else:
            variable_pred = st.selectbox("Elige la variable productiva a predecir:", productivos_disponibles)
            nutrientes_usar = st.multiselect("Selecciona los nutrientes para el modelo:", nutrientes_disponibles, default=nutrientes_disponibles)
            if st.button("Entrenar modelo predictivo"):
                df_hist = df_hist.copy()
                X = df_hist[nutrientes_usar].astype(float)
                y = df_hist[variable_pred].astype(float)
                X = X.fillna(X.mean())
                y = y.fillna(y.mean())
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                rf = RandomForestRegressor(n_estimators=200, random_state=42)
                lr = LinearRegression()
                rf.fit(X_train, y_train)
                lr.fit(X_train, y_train)
                pred_rf = rf.predict(X_test)
                pred_lr = lr.predict(X_test)
                mae_rf = mean_absolute_error(y_test, pred_rf)
                mae_lr = mean_absolute_error(y_test, pred_lr)
                r2_rf = r2_score(y_test, pred_rf)
                r2_lr = r2_score(y_test, pred_lr)
                if r2_rf > r2_lr:
                    modelo = rf
                    modelo_tipo = "Random Forest"
                    r2 = r2_rf
                    mae = mae_rf
                else:
                    modelo = lr
                    modelo_tipo = "Regresión Lineal"
                    r2 = r2_lr
                    mae = mae_lr
                st.session_state["modelo_predictivo"] = modelo
                st.session_state["scaler_predictivo"] = scaler
                st.session_state["nutrientes_usar"] = nutrientes_usar
                st.session_state["variable_pred"] = variable_pred
                st.success(f"¡Modelo entrenado exitosamente! ({modelo_tipo})")
                st.info(f"R² validación: {r2:.3f} | MAE: {mae:.4f}")

                if modelo_tipo == "Random Forest":
                    importancias = modelo.feature_importances_
                    importancia_df = pd.DataFrame({"Nutriente": nutrientes_usar, "Importancia": importancias})
                    importancia_df = importancia_df.sort_values("Importancia", ascending=False)
                    st.markdown("#### Importancia de cada nutriente para la predicción:")
                    st.dataframe(importancia_df)
                    fig_imp = go.Figure(go.Bar(x=importancia_df["Nutriente"], y=importancia_df["Importancia"]))
                    fig_imp.update_layout(title="Importancia relativa de los nutrientes", xaxis_title="Nutriente", yaxis_title="Importancia")
                    st.plotly_chart(fig_imp, use_container_width=True)

            if "modelo_predictivo" in st.session_state and st.session_state.get("variable_pred") == variable_pred:
                st.markdown("---")
                st.markdown("### Predice el resultado productivo para una dieta propuesta")
                inputs = {}
                for nutr in st.session_state["nutrientes_usar"]:
                    hist_vals = df_hist[nutr]
                    val_min = float(hist_vals.min())
                    val_max = float(hist_vals.max())
                    val_med = float(hist_vals.mean())
                    val_input = st.number_input(f"{nutr.capitalize()}",
                                                min_value=round(val_min*0.8, 3),
                                                max_value=round(val_max*1.2, 3),
                                                value=round(val_med, 3),
                                                step=0.001)
                    inputs[nutr] = val_input
                X_pred = pd.DataFrame([inputs])[st.session_state["nutrientes_usar"]]
                scaler = st.session_state["scaler_predictivo"]
                X_pred_scaled = scaler.transform(X_pred)
                modelo = st.session_state["modelo_predictivo"]
                pred = modelo.predict(X_pred_scaled)[0]
                st.success(f"Predicción para {st.session_state['variable_pred'].upper()}: **{pred:.4f}**")
                prom_hist = float(df_hist[st.session_state["variable_pred"]].mean())
                st.markdown(f"Promedio histórico: **{prom_hist:.4f}**")
                fig = go.Figure()
                fig.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=pred,
                    delta={'reference': prom_hist},
                    title={"text": f"{st.session_state['variable_pred'].upper()}"},
                    gauge={'axis': {'range': [min(prom_hist, pred)*0.9, max(prom_hist, pred)*1.1]}}
                ))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("#### Distribución histórica de la variable predicha:")
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(x=df_hist[st.session_state["variable_pred"]], nbinsx=20, name="Histórico"))
                fig_hist.add_trace(go.Scatter(x=[pred], y=[0], mode='markers', marker=dict(size=15, color='red'), name="Predicción"))
                fig_hist.update_layout(title=f"Histórico de {st.session_state['variable_pred'].upper()} vs Predicción")
                st.plotly_chart(fig_hist, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:11px;color:#fff;text-align:center'>Desarrollado como MVP para <b>UYWA-NUTRITION®</b></div>",
    unsafe_allow_html=True
)
