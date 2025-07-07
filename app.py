import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

st.set_page_config(page_title="Gestión y Análisis de Dietas", layout="wide")

# --- FONDO CORPORATIVO ---
st.markdown("""
    <style>
    html, body, .stApp, .main, .block-container {
        background: linear-gradient(120deg, #f3f6fa 0%, #e3ecf7 100%) !important;
        background-color: #f3f6fa !important;
    }
    section[data-testid="stSidebar"] {
        background: #19345c !important;
    }
    .block-container {
        background: transparent !important;
    }
    section.main {
        background: transparent !important;
    }
    .stFileUploader, .stMultiSelect, .stSelectbox, .stNumberInput, .stTextInput {
        background-color: #f4f8fa !important;
        border-radius: 6px !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR EMPRESARIAL ----------
with st.sidebar:
    st.image("nombre_archivo_logo.png", width=110)
    st.markdown(
        """
        <div style='text-align: center; margin-bottom:10px;'>
            <div style='font-size:32px;font-family:Montserrat,Arial;color:#fff; margin-top: 10px;letter-spacing:1px; font-weight:700; line-height:1.1;'>
                UYWA-<br>NUTRITION<sup>®</sup>
            </div>
            <div style='font-size:16px;color:#fff; margin-top: 5px; font-family:Montserrat,Arial; line-height: 1.1;'>
                Nutrición de Precisión Basada en Evidencia
            </div>
            <hr style='border-top:1px solid #2e4771; margin: 18px 0;'>
            <div style='font-size:14px;color:#fff; margin-top: 8px;'>
                <b>Contacto:</b> uywasas@gmail.com<br>
                Derechos reservados © 2025
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Selecciona una sección",
        [
            "Análisis de Dieta",
            "Simulador Productivo",
            "Simulador Económico",
            "Comparador de Escenarios"
        ],
        key="menu_radio"
    )

st.title("Gestión y Análisis de Dietas")

# ==================== Inicialización de session_state ====================
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

# --- Carga de ingredientes con detección de fila de unidades ---
@st.cache_data
def cargar_ingredientes_excel_unidades(archivo):
    # Lee el archivo, asume que la segunda fila es de unidades
    df_full = pd.read_excel(archivo, header=None)
    headers = df_full.iloc[0].values
    unidades = df_full.iloc[1].values
    # El resto de filas son datos
    data = df_full.iloc[2:].copy()
    data.columns = headers
    unidades_dict = {headers[i]: unidades[i] for i in range(len(headers))}
    return data.reset_index(drop=True), unidades_dict

# ============ ANÁLISIS DE DIETA =============
if menu == "Análisis de Dieta":
    archivo_excel = "Ingredientes1.xlsx"
    df_ing = None
    unidades_dict = {}
    if os.path.exists(archivo_excel):
        df_ing, unidades_dict = cargar_ingredientes_excel_unidades(archivo_excel)
    else:
        archivo_subido = st.file_uploader("Sube tu archivo de ingredientes (.xlsx)", type=["xlsx"])
        if archivo_subido is not None:
            df_ing, unidades_dict = cargar_ingredientes_excel_unidades(archivo_subido)
        else:
            st.warning("No se encontró el archivo Ingredientes1.xlsx. Sube uno para continuar.")

    if df_ing is not None:
        ingredientes_lista = df_ing["Ingrediente"].dropna().unique().tolist()
        ingredientes_seleccionados = st.multiselect(
            "Selecciona tus ingredientes", ingredientes_lista, default=[]
        )

        columnas_fijas = ["Ingrediente", "% Inclusión", "precio"]
        columnas_nut = [col for col in df_ing.columns if col not in columnas_fijas]
        nutrientes_seleccionados = st.multiselect(
            "Selecciona nutrientes a analizar",
            columnas_nut,
            default=columnas_nut[:4] if len(columnas_nut) >= 4 else columnas_nut
        )

        data_formula = []
        total_inclusion = 0
        st.markdown("### Ajusta % inclusión y precio (USD/tonelada) de cada ingrediente")
        for ing in ingredientes_seleccionados:
            fila = df_ing[df_ing["Ingrediente"] == ing].iloc[0].to_dict()
            cols = st.columns([2, 1, 1])
            with cols[0]:
                st.write(f"**{ing}**")
            with cols[1]:
                porcentaje = st.number_input(
                    f"% inclusión para {ing}",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.1,
                    key=f"porc_{ing}"
                )
            with cols[2]:
                # Mostramos el precio en USD/tonelada, pero guardamos en USD/kg para cálculos
                precio_kg = float(fila["precio"]) if "precio" in fila and pd.notnull(fila["precio"]) else 0.0
                precio_mod = st.number_input(
                    f"Precio {ing} (USD/tonelada)",
                    min_value=0.0,
                    max_value=3000.0,
                    value=precio_kg * 1000,
                    step=1.0,
                    key=f"precio_{ing}"
                )
            total_inclusion += porcentaje
            fila["% Inclusión"] = porcentaje
            fila["precio"] = precio_mod / 1000  # Guardamos en USD/kg para cálculos
            data_formula.append(fila)

        st.markdown(f"#### Suma total de inclusión: **{total_inclusion:.2f}%**")
        if abs(total_inclusion - 100) > 0.01:
            st.warning("La suma de los ingredientes no es 100%. Puede afectar el análisis final.")

        if ingredientes_seleccionados and nutrientes_seleccionados:
            df_formula = pd.DataFrame(data_formula)
            # Para mostrar el precio en USD/tonelada en la tabla
            df_mostrar = df_formula.copy()
            df_mostrar["precio (USD/ton)"] = df_mostrar["precio"] * 1000
            st.subheader("Ingredientes y proporciones de tu dieta")
            st.dataframe(df_mostrar[["Ingrediente", "% Inclusión", "precio (USD/ton)"] + nutrientes_seleccionados])

            color_palette = px.colors.qualitative.Plotly
            color_map = {ing: color_palette[idx % len(color_palette)] for idx, ing in enumerate(ingredientes_lista)}

            tab1, tab2, tab3 = st.tabs([
                "Aporte por Ingrediente a Nutrientes",
                "Costo Total por Ingrediente",
                "Costo por Unidad de Nutriente"
            ])

            with tab1:
                st.markdown("#### Aporte de cada ingrediente a cada nutriente (barras por nutriente)")
                nut_tabs = st.tabs([nut for nut in nutrientes_seleccionados])
                for i, nut in enumerate(nutrientes_seleccionados):
                    with nut_tabs[i]:
                        valores = []
                        for ing in ingredientes_seleccionados:
                            valor = pd.to_numeric(df_formula.loc[df_formula["Ingrediente"] == ing, nut], errors="coerce").values[0]
                            porc = df_formula[df_formula["Ingrediente"] == ing]["% Inclusión"].values[0]
                            aporte = (valor * porc) / 100 if pd.notnull(valor) else 0
                            valores.append(aporte)
                        unidad = unidades_dict.get(nut, "")
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=ingredientes_seleccionados,
                            y=valores,
                            marker_color=[color_map[ing] for ing in ingredientes_seleccionados],
                            text=[f"{v:.2f}" for v in valores],
                            textposition='auto'
                        ))
                        fig.update_layout(
                            xaxis_title="Ingrediente",
                            yaxis_title=f"Aporte de {nut} ({unidad})" if unidad else f"Aporte de {nut}",
                            title=f"Aporte de cada ingrediente a {nut} ({unidad})" if unidad else f"Aporte de cada ingrediente a {nut}"
                        )
                        st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.markdown("#### Costo total aportado por cada ingrediente (USD/tonelada de dieta, proporcional)")
                costos = [
                    (row["precio"] * row["% Inclusión"] / 100) if pd.notnull(row["precio"]) else 0
                    for idx, row in df_formula.iterrows()
                ]
                # Multiplicamos por 1000 para mostrar en tonelada
                costos_ton = [c * 1000 for c in costos]
                total_costo_ton = sum(costos_ton)
                proporciones = [(c / total_costo_ton * 100) if total_costo_ton > 0 else 0 for c in costos_ton]
                fig2 = go.Figure([go.Bar(
                    x=ingredientes_seleccionados,
                    y=costos_ton,
                    marker_color=[color_map[ing] for ing in ingredientes_seleccionados],
                    text=[f"{c:.2f} USD/ton<br>{p:.1f}%" for c, p in zip(costos_ton, proporciones)],
                    textposition='auto'
                )])
                fig2.update_layout(
                    xaxis_title="Ingrediente",
                    yaxis_title="Costo aportado (USD/tonelada de dieta)",
                    title="Costo total aportado por ingrediente (USD/tonelada)",
                    showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown(f"**Costo total de la fórmula:** ${total_costo_ton:.2f} USD/tonelada")
                st.markdown("Cada barra muestra el costo y el porcentaje proporcional de cada ingrediente respecto al costo total de la dieta.")

            with tab3:
                st.markdown("#### Costo por unidad de nutriente aportada (USD/tonelada por unidad de nutriente)")
                nut_tabs = st.tabs([nut for nut in nutrientes_seleccionados])
                for i, nut in enumerate(nutrientes_seleccionados):
                    with nut_tabs[i]:
                        costos_unit = []
                        for ing in ingredientes_seleccionados:
                            row = df_formula[df_formula["Ingrediente"] == ing].iloc[0]
                            aporte = pd.to_numeric(row[nut], errors="coerce")
                            aporte = (aporte * row["% Inclusión"]) / 100 if pd.notnull(aporte) else 0
                            costo = (row["precio"] * row["% Inclusión"] / 100) if pd.notnull(row["precio"]) else 0
                            costo_unitario = (costo / aporte) if aporte > 0 else np.nan
                            costo_unitario_ton = costo_unitario * 1000 if not np.isnan(costo_unitario) else np.nan
                            costos_unit.append(costo_unitario_ton)
                        unidad = unidades_dict.get(nut, "")
                        fig3 = go.Figure()
                        fig3.add_trace(go.Bar(
                            x=ingredientes_seleccionados,
                            y=costos_unit,
                            marker_color=[color_map[ing] for ing in ingredientes_seleccionados],
                            text=[f"{c:.4f}" if not np.isnan(c) else "-" for c in costos_unit],
                            textposition='auto'
                        ))
                        fig3.update_layout(
                            xaxis_title="Ingrediente",
                            yaxis_title=f"Costo por unidad de {nut} (USD/ton por {unidad})" if unidad else f"Costo por unidad de {nut} (USD/ton)",
                            title=f"Costo por unidad de {nut} (USD/ton por {unidad})" if unidad else f"Costo por unidad de {nut} (USD/ton)"
                        )
                        st.plotly_chart(fig3, use_container_width=True)

            st.markdown("""
            - Puedes modificar los precios de los ingredientes y ver el impacto instantáneamente.
            - Selecciona los nutrientes que más te interesan para un análisis enfocado.
            - Las pestañas te permiten comparar visualmente: el costo total por ingrediente (proporcional), el aporte por nutriente y el costo por unidad de nutriente.
            - **Recuerda:** El precio de cada ingrediente se ingresa y visualiza en USD por tonelada (USD/ton). Los cálculos internos y los resultados de costo total se muestran en USD/tonelada en los gráficos y tablas.
            """)

        else:
            st.info("Selecciona ingredientes y nutrientes para comenzar el análisis y visualización.")
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
