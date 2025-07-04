import io
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as np
import plotly.graph_objs as go

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
    st.header("Matriz de Ingredientes - Análisis Avanzado de Costos y Alternativas")

    ingredientes_base = [
        {"Ingrediente": "Maíz", "Precio ($/kg)": 0.28, "Energía (kcal/kg)": 3350, "Proteína (%)": 8.5, "Lisina (%)": 0.25, "Calcio (%)": 0.02, "% Inclusión": 50},
        {"Ingrediente": "Soja", "Precio ($/kg)": 0.42, "Energía (kcal/kg)": 2400, "Proteína (%)": 46.0, "Lisina (%)": 2.85, "Calcio (%)": 0.30, "% Inclusión": 25},
        {"Ingrediente": "Harina de carne", "Precio ($/kg)": 0.60, "Energía (kcal/kg)": 2100, "Proteína (%)": 52.0, "Lisina (%)": 3.10, "Calcio (%)": 5.50, "% Inclusión": 10},
        {"Ingrediente": "Aceite", "Precio ($/kg)": 1.00, "Energía (kcal/kg)": 8800, "Proteína (%)": 0.0, "Lisina (%)": 0.0, "Calcio (%)": 0.0, "% Inclusión": 5},
        {"Ingrediente": "Sal", "Precio ($/kg)": 0.18, "Energía (kcal/kg)": 0, "Proteína (%)": 0.0, "Lisina (%)": 0.0, "Calcio (%)": 0.0, "% Inclusión": 5},
        {"Ingrediente": "Premix", "Precio ($/kg)": 0.80, "Energía (kcal/kg)": 0, "Proteína (%)": 0.0, "Lisina (%)": 0.1, "Calcio (%)": 1.5, "% Inclusión": 5},
    ]

    # Alternativas simples sugeridas
    alternativas_db = [
        {"Ingrediente": "Sorgo", "Precio ($/kg)": 0.22, "Energía (kcal/kg)": 3200, "Proteína (%)": 9.5, "Lisina (%)": 0.24, "Calcio (%)": 0.02, "Alternativa de": "Maíz"},
        {"Ingrediente": "Canola", "Precio ($/kg)": 0.40, "Energía (kcal/kg)": 2300, "Proteína (%)": 38.0, "Lisina (%)": 1.90, "Calcio (%)": 0.36, "Alternativa de": "Soja"},
        {"Ingrediente": "Girasol", "Precio ($/kg)": 0.38, "Energía (kcal/kg)": 2200, "Proteína (%)": 35.0, "Lisina (%)": 1.50, "Calcio (%)": 0.32, "Alternativa de": "Soja"},
        {"Ingrediente": "DDGS", "Precio ($/kg)": 0.33, "Energía (kcal/kg)": 2800, "Proteína (%)": 28.0, "Lisina (%)": 0.80, "Calcio (%)": 0.10, "Alternativa de": "Harina de carne"},
    ]

    columnas = ["Ingrediente", "Precio ($/kg)", "Energía (kcal/kg)", "Proteína (%)", "Lisina (%)", "Calcio (%)", "% Inclusión"]

    if "ingredientes" not in st.session_state or not isinstance(st.session_state["ingredientes"], list):
        st.session_state["ingredientes"] = ingredientes_base.copy()

    # Limpiar ingredientes
    ingredientes_limpios = []
    for ing in st.session_state["ingredientes"]:
        if isinstance(ing, dict) and all(k in ing for k in columnas):
            ingredientes_limpios.append(ing)
    if not ingredientes_limpios:
        ingredientes_limpios = ingredientes_base.copy()
    st.session_state["ingredientes"] = ingredientes_limpios
    ingredientes = st.session_state["ingredientes"]

    tab_names = [ing["Ingrediente"] for ing in ingredientes] + ["➕ Nuevo Ingrediente"]
    tabs = st.tabs(tab_names)

    tooltips = {
        "Precio ($/kg)": "Costo estimado en dólares por kilogramo del ingrediente.",
        "Energía (kcal/kg)": "Energía metabolizable aportada por el ingrediente (kcal/kg).",
        "Proteína (%)": "Porcentaje de proteína bruta sobre materia seca.",
        "Lisina (%)": "Porcentaje de lisina en base al ingrediente.",
        "Calcio (%)": "Porcentaje de calcio aportado.",
        "% Inclusión": "Porcentaje del ingrediente en la fórmula total (100% sumando todos)."
    }

    # Edición de ingredientes
    for idx, ing in enumerate(ingredientes):
        with tabs[idx]:
            st.subheader(f"🧬 {ing['Ingrediente']}")
            st.markdown(f"#### Edita los valores para {ing['Ingrediente']}")
            col1, col2 = st.columns(2)
            with col1:
                ing_name = st.text_input(
                    "Nombre del ingrediente",
                    value=ing["Ingrediente"],
                    key=f"name_{idx}",
                    help="Nombre único para el ingrediente"
                )
                ing["Ingrediente"] = ing_name

            with col2:
                if st.button("🗑️ Eliminar ingrediente", key=f"del_{idx}"):
                    st.session_state["ingredientes"].pop(idx)
                    st.experimental_rerun()

            for key in columnas:
                if key == "Ingrediente":
                    continue
                valor = ing[key]
                helptext = tooltips.get(key, "")
                nuevo_valor = st.number_input(
                    key,
                    min_value=0.0,
                    value=float(valor),
                    step=0.01 if "%" in key else 1.0,
                    key=f"{key}_{idx}",
                    help=helptext,
                    format="%.4f" if "%" in key else "%.2f"
                )
                ing[key] = nuevo_valor

            if st.button("📋 Duplicar este ingrediente", key=f"dup_{idx}"):
                copia = ing.copy()
                copia["Ingrediente"] = copia["Ingrediente"] + " (copia)"
                st.session_state["ingredientes"].append(copia)
                st.experimental_rerun()

    # Pestaña para agregar nuevo ingrediente
    with tabs[-1]:
        st.subheader("Agregar nuevo ingrediente")
        nuevo = {}
        col1, col2 = st.columns(2)
        with col1:
            nuevo["Ingrediente"] = st.text_input("Nombre nuevo ingrediente", key="new_ingr", help="Nombre único para el nuevo ingrediente")
        for col in columnas:
            if col == "Ingrediente":
                continue
            helptext = tooltips.get(col, "")
            nuevo[col] = st.number_input(
                f"{col}",
                min_value=0.0,
                value=0.0,
                step=0.01 if "%" in col else 1.0,
                key=f"new_{col}",
                help=helptext,
                format="%.4f" if "%" in col else "%.2f"
            )
        with col2:
            if st.button("Agregar", key="add_ing"):
                nombres_actuales = [i["Ingrediente"] for i in st.session_state["ingredientes"]]
                if nuevo["Ingrediente"] and nuevo["Ingrediente"] not in nombres_actuales:
                    st.session_state["ingredientes"].append(nuevo)
                    st.success(f"Ingrediente '{nuevo['Ingrediente']}' agregado.")
                    st.experimental_rerun()
                else:
                    st.warning("El nombre es obligatorio y no debe estar repetido.")

    st.markdown("---")
    buscar = st.text_input("🔎 Buscar ingrediente por nombre", "")
    filas_validas = []
    for i in st.session_state["ingredientes"]:
        if isinstance(i, dict) and all(k in i for k in columnas):
            if buscar.lower() in i["Ingrediente"].lower() if buscar else True:
                filas_validas.append([i[c] for c in columnas])
    df_vista = pd.DataFrame(filas_validas, columns=columnas)
    if df_vista.empty:
        df_vista = pd.DataFrame(columns=columnas)
    st.dataframe(df_vista)

    # ========== 1. Ranking de Ingredientes más Costosos ==========
    st.subheader("Ranking de Ingredientes por Aporte al Costo")
    df_costos = df_vista.copy()
    if not df_costos.empty:
        df_costos["Costo Parcial"] = df_costos["% Inclusión"] / 100 * df_costos["Precio ($/kg)"]
        df_costos = df_costos.sort_values("Costo Parcial", ascending=False)
        st.bar_chart(df_costos.set_index("Ingrediente")["Costo Parcial"])
        st.dataframe(df_costos[["Ingrediente", "% Inclusión", "Precio ($/kg)", "Costo Parcial"]])
        ingrediente_mas_costoso = df_costos.iloc[0]["Ingrediente"]
    else:
        st.info("No hay datos para analizar el costo de ingredientes.")
        ingrediente_mas_costoso = None

    # ========== 2. Ranking de nutrientes más costosos ==========
    st.subheader("Ranking de Nutrientes más Costosos en la Dieta")
    nutrientes = ["Proteína (%)", "Energía (kcal/kg)", "Lisina (%)", "Calcio (%)"]
    total_kg = sum(df_vista["% Inclusión"]) / 100 if not df_vista.empty else 0
    resumen_nutrientes = []
    for nut in nutrientes:
        # Total nutriente en la dieta (kg o unidad)
        total_nut = sum(df_vista["% Inclusión"] / 100 * df_vista[nut])
        # Costo relativo: suma de (costo parcial × % del nutriente que aporta cada ingrediente)
        if total_nut > 0:
            costo_nut = sum(
                (df_vista["% Inclusión"] / 100 * df_vista[nut]) / total_nut * df_vista["Costo Parcial"]
            )
        else:
            costo_nut = 0
        resumen_nutrientes.append({"Nutriente": nut, "Aporte total": total_nut, "Costo asociado": costo_nut})
    df_nut = pd.DataFrame(resumen_nutrientes)
    if not df_nut.empty:
        df_nut = df_nut.sort_values("Costo asociado", ascending=False)
        st.bar_chart(df_nut.set_index("Nutriente")["Costo asociado"])
        st.dataframe(df_nut)
        nutriente_mas_costoso = df_nut.iloc[0]["Nutriente"]
    else:
        st.info("No hay datos de nutrientes.")

    # ========== 3. Sugerencias simples de sustitución ==========
    st.subheader("Sugerencias de Sustitución de Materias Primas")
    sugerencias = []
    for idx, row in df_costos.iterrows():
        ingrediente = row["Ingrediente"]
        costo_parcial = row["Costo Parcial"]
        # Buscar alternativas
        alternativas = [alt for alt in alternativas_db if alt["Alternativa de"].lower() == ingrediente.lower()]
        if alternativas:
            for alt in alternativas:
                sugerencias.append({
                    "Ingrediente actual": ingrediente,
                    "Costo actual": costo_parcial,
                    "Alternativa sugerida": alt["Ingrediente"],
                    "Precio alternativa": alt["Precio ($/kg)"],
                    "Proteína (%)": alt["Proteína (%)"],
                    "Energía (kcal/kg)": alt["Energía (kcal/kg)"],
                })
    if sugerencias:
        st.dataframe(pd.DataFrame(sugerencias))
        st.markdown(
            "Puedes probar a reemplazar el ingrediente más costoso por su alternativa para ver el impacto en el costo total."
        )
    else:
        st.info("No hay alternativas sugeridas para los ingredientes actuales.")

    # ========== 4. Simulador de sustitución y recomendaciones automáticas ==========
    st.subheader("Simulador y Recomendaciones Automáticas")
    if ingrediente_mas_costoso:
        sugeridas = [alt for alt in alternativas_db if alt["Alternativa de"].lower() == ingrediente_mas_costoso.lower()]
        if sugeridas:
            alt = sugeridas[0]
            st.markdown(f"**¿Quieres simular reemplazar {ingrediente_mas_costoso} por {alt['Ingrediente']}?**")
            if st.button(f"Simular reemplazo de {ingrediente_mas_costoso} por {alt['Ingrediente']}"):
                # Copia de ingredientes actual
                ingredientes_nuevo = [i.copy() for i in ingredientes]
                for i in ingredientes_nuevo:
                    if i["Ingrediente"] == ingrediente_mas_costoso:
                        # Reemplaza por alternativa
                        for k in ["Ingrediente", "Precio ($/kg)", "Energía (kcal/kg)", "Proteína (%)", "Lisina (%)", "Calcio (%)"]:
                            i[k] = alt[k]
                st.session_state["ingredientes"] = ingredientes_nuevo
                st.success(f"Se simuló el reemplazo de {ingrediente_mas_costoso} por {alt['Ingrediente']}. Observa el nuevo análisis arriba.")
                st.experimental_rerun()
        else:
            st.info("No hay alternativa inmediata para el ingrediente más costoso.")

    # Recomendación automática simple
    if not df_costos.empty and not df_nut.empty:
        if df_costos.iloc[0]["Costo Parcial"] > 2 * df_costos["Costo Parcial"].mean():
            st.warning(
                f"El ingrediente **{df_costos.iloc[0]['Ingrediente']}** representa más del doble del costo promedio. Considera reducir su inclusión o buscar alternativas."
            )
        if df_nut.iloc[0]["Costo asociado"] > 1.5 * df_nut["Costo asociado"].mean():
            st.warning(
                f"El nutriente **{df_nut.iloc[0]['Nutriente']}** es el más caro de cubrir en la dieta. Revisa si puedes ajustar ingredientes para optimizar el costo de este nutriente."
            )

    # --- DESCARGA ---
    filas_validas_export = []
    for i in st.session_state["ingredientes"]:
        if isinstance(i, dict) and all(k in i for k in columnas):
            filas_validas_export.append([i[c] for c in columnas])
    df_export = pd.DataFrame(filas_validas_export, columns=columnas)
    if df_export.empty:
        df_export = pd.DataFrame(columns=columnas)
    excel_buffer = io.BytesIO()
    df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    st.download_button(
        "Descargar matriz en Excel",
        data=excel_buffer,
        file_name="matriz_ingredientes.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("""
    - Ahora puedes analizar los ingredientes y nutrientes más costosos, simular sustituciones y recibir recomendaciones automáticas.
    - Cambia porcentajes, precios o composición y observa el impacto en tiempo real.
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
