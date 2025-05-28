import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Simulación Muñeco Freddy", layout="wide")
st.title("🎄 Simulación Financiera - Muñeco Freddy")
st.markdown("""
Esta aplicación simula la utilidad neta de la producción del muñeco **Freddy** para la temporada navideña.

Se basa en un modelo de simulación de Monte Carlo usando distribución normal para la demanda.
""")

# Entradas del usuario en sidebar
st.sidebar.header("🔧 Parámetros de Simulación")
N = st.sidebar.slider("Número de simulaciones", 100, 2000, 500, 100)
Q = st.sidebar.selectbox("Cantidad producida (Q)", [50000, 60000, 70000], index=1)
media_demanda = st.sidebar.number_input("Demanda esperada (media)", value=60000)
desviacion_demanda = st.sidebar.number_input("Desviación estándar de la demanda", value=15000)

# Costos y precios (fijos)
costo_fijo = 100000
costo_variable = 34
precio_venta = 42
precio_liquidacion = 10

# Simulación
np.random.seed(42)
demanda = np.random.normal(media_demanda, desviacion_demanda, N).round().astype(int)
demanda = np.maximum(demanda, 0)
ventas = np.minimum(Q, demanda)
excedentes = np.maximum(Q - demanda, 0)

ingresos_ventas = ventas * precio_venta
ingresos_excedentes = excedentes * precio_liquidacion
costo_total = costo_fijo + (Q * costo_variable)
utilidad_neta = ingresos_ventas + ingresos_excedentes - costo_total

# DataFrame de resultados
resultados = pd.DataFrame({
    'Demanda': demanda,
    'Ventas': ventas,
    'Excedentes': excedentes,
    'Ingresos por Ventas': ingresos_ventas,
    'Ingresos por Excedentes': ingresos_excedentes,
    'Costo Total': costo_total,
    'Utilidad Neta': utilidad_neta
})

# Métricas clave
utilidad_media = utilidad_neta.mean()
utilidad_std = utilidad_neta.std()
probabilidad_quiebre_stock = np.mean(demanda > Q)

# Resultados clave
st.subheader("📊 Resultados de la Simulación")
col1, col2, col3 = st.columns(3)
col1.metric("Utilidad Promedio", f"${utilidad_media:,.2f}")
col2.metric("Desviación Estándar", f"${utilidad_std:,.2f}")
col3.metric("% Quiebre de Inventario", f"{probabilidad_quiebre_stock*100:.1f}%")

# Histograma de utilidad
st.subheader("📉 Distribución de la Utilidad Neta")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(utilidad_neta, bins=30, color='skyblue', edgecolor='black')
ax.axvline(utilidad_media, color='red', linestyle='dashed', linewidth=2)
ax.set_title('Histograma de la Utilidad Neta')
ax.set_xlabel('Utilidad Neta ($)')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

# Visualización de escenarios de demanda vs producción
st.subheader("📦 Comparación: Demanda vs Producción")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.kdeplot(demanda, label="Demanda", fill=True)
ax2.axvline(Q, color='orange', linestyle='--', label=f"Producción ({Q})")
ax2.set_title('Distribución de la Demanda con línea de Producción')
ax2.set_xlabel('Unidades')
ax2.legend()
st.pyplot(fig2)

# Mostrar tabla con primeros registros
with st.expander("📋 Ver tabla de resultados detallados"):
    st.dataframe(resultados.head(20))

# Descargar CSV
st.download_button(
    label="📥 Descargar resultados en CSV",
    data=resultados.to_csv(index=False).encode('utf-8'),
    file_name=f"resultados_simulacion_freddy_{Q}.csv",
    mime='text/csv'
)

# Conclusión
st.markdown("""
---
### 📌 Conclusión:
- Esta simulación te permite observar el impacto de diferentes niveles de producción sobre la utilidad esperada.
- Puedes ajustar los parámetros para evaluar decisiones más agresivas o conservadoras.
- Considera el equilibrio entre producción y demanda esperada para maximizar ganancias y minimizar excedentes.
""")
