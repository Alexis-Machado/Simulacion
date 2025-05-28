import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Simulación de Inventario", layout="wide")
st.title("📦 Simulación de Inventario - Centro de Distribución")

st.markdown("""
Este simulador modela el comportamiento del inventario de un material con demanda exponencial revisado semanalmente.
Se calculan los costos de almacenamiento, faltantes y órdenes a lo largo de un horizonte de **2 meses (60 días)**.
""")

# Parámetros del sistema
st.sidebar.header("🔧 Parámetros")
demanda_media_diaria = st.sidebar.number_input("Demanda promedio diaria (kg)", value=100)
capacidad_bodega = st.sidebar.number_input("Capacidad de bodega (kg)", value=700)
costo_orden = st.sidebar.number_input("Costo por orden ($)", value=1000)
costo_faltante = st.sidebar.number_input("Costo por faltante ($/kg)", value=6)
costo_almacenamiento = st.sidebar.number_input("Costo de almacenamiento ($/kg)", value=1)
periodo_revision = 7
horizonte_dias = 60

# Simulación
def simular_inventario():
    dias = list(range(1, horizonte_dias + 1))
    inventario = []
    faltantes = []
    ordenes = []
    almacenamiento = []

    inv_actual = capacidad_bodega  # inventario inicial
    for dia in dias:
        demanda = np.random.exponential(demanda_media_diaria)
        demanda = round(demanda, 2)

        if demanda > inv_actual:
            faltante = demanda - inv_actual
            vendido = inv_actual
            inv_actual = 0
        else:
            faltante = 0
            vendido = demanda
            inv_actual -= vendido

        # Registrar inventario al final del día
        inventario.append(inv_actual)
        faltantes.append(faltante)
        almacenamiento.append(inv_actual)

        # Cada 7 días se revisa el inventario y se ordena
        if dia % periodo_revision == 0:
            orden = capacidad_bodega - inv_actual
            inv_actual += orden
        else:
            orden = 0

        ordenes.append(orden)

    df = pd.DataFrame({
        'Día': dias,
        'Inventario': inventario,
        'Ordenado': ordenes,
        'Faltante': faltantes,
        'Costo Faltante': np.array(faltantes) * costo_faltante,
        'Costo Orden': [costo_orden if o > 0 else 0 for o in ordenes],
        'Costo Almacenamiento': np.array(almacenamiento) * costo_almacenamiento
    })

    df['Costo Diario Total'] = df['Costo Faltante'] + df['Costo Orden'] + df['Costo Almacenamiento']
    return df

# Ejecutar simulación
df_sim = simular_inventario()
costo_promedio_diario = df_sim['Costo Diario Total'].mean()

st.metric("💵 Costo promedio diario", f"${costo_promedio_diario:,.2f}")

# Gráficos
st.subheader("📊 Comportamiento del Inventario")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_sim['Día'], df_sim['Inventario'], label='Inventario', color='blue')
ax.plot(df_sim['Día'], df_sim['Faltante'], label='Faltantes', color='red')
ax.set_xlabel("Día")
ax.set_ylabel("Cantidad (kg)")
ax.set_title("Inventario y Faltantes por Día")
ax.legend()
st.pyplot(fig)

# Tabla
with st.expander("📋 Ver tabla de resultados"):
    st.dataframe(df_sim.head(30))

# Descargar CSV
csv = df_sim.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar CSV de la simulación", csv, "resultados_inventario.csv", "text/csv")
