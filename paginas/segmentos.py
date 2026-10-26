from pathlib import Path

import pandas as pd
import streamlit as st

DATOS = Path(__file__).resolve().parents[1] / "datos"

ACCIONES = {
    "Cuentas clave": "Ejecutivo de cuenta y condiciones logísticas preferentes; seguimiento "
                     "mensual, porque cualquier deterioro afecta a muchos clientes.",
    "Pequeños confiables": "Programa de crecimiento: visibilidad en el sitio y promociones; "
                           "son las futuras cuentas clave.",
    "Ticket bajo, flete caro": "Reducir el peso del envío: kits o combos, monto mínimo para "
                               "envío gratis y tarifas de flete negociadas.",
    "En riesgo operativo": "Plan de mejora con plazo máximo de despacho y alertas; prioridad "
                           "en las llamadas del modelo de riesgo. Acompañar y medir, no "
                           "sancionar automáticamente.",
}

st.title("Segmentación de vendedores")
st.caption("Parte 3 (opción 3B): K-Means con k = 4 sobre vendedores con al menos "
           "10 pedidos entregados.")

perfiles = pd.read_csv(DATOS / "perfiles_segmentos.csv", index_col=0)
vendedores = pd.read_csv(DATOS / "segmentos_vendedores.csv")

st.subheader("Perfil de cada segmento (medianas)")
st.dataframe(perfiles, use_container_width=True)

st.subheader("Acción recomendada por segmento")
for nombre in perfiles.index:
    st.markdown(f"**{nombre}** · {int(perfiles.loc[nombre, 'vendedores'])} vendedores, "
                f"{perfiles.loc[nombre, '% de ventas totales']} % de las ventas  \n"
                f"{ACCIONES.get(nombre, '')}")

st.subheader("Visualización de los grupos (PCA)")
st.image(str(DATOS / "segmentos_pca.png"), use_container_width=True)
st.caption("Las cuentas clave no se separan en el gráfico porque se distinguen por volumen, "
           "y el número de pedidos casi no pesa en los dos primeros componentes.")

st.subheader("Explorar vendedores")
segmento = st.selectbox("Segmento", perfiles.index)
columnas = ["seller_id", "estado_vendedor", "n_pedidos", "ventas", "ticket_promedio",
            "flete_relativo", "tasa_retraso", "dias_despacho", "tasa_mala_resena"]
st.dataframe(vendedores.loc[vendedores["nombre_segmento"] == segmento, columnas]
             .sort_values("ventas", ascending=False).round(3),
             use_container_width=True)
