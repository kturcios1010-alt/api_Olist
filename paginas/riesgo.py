from pathlib import Path

import pandas as pd
import requests
import streamlit as st

DATOS = Path(__file__).resolve().parents[1] / "datos"
ENTEROS = ["n_items", "n_vendedores"]
DECIMALES = ["precio_total", "flete_total", "peso_total_g", "fotos_promedio", "cuotas_max"]

# URL de la API desde los secretos de la app
try:
    API_URL = st.secrets["API_URL"].rstrip("/")
except Exception:
    API_URL = None

st.title("Riesgo de mala reseña")
st.caption("Se elige un pedido de ejemplo, se pueden editar sus valores y la app consulta "
           "la API desplegada en Render.")

if API_URL is None:
    st.error("No se encontró la URL de la API (API_URL) en los secretos de la app.")
    st.stop()
st.sidebar.markdown(f"**URL de la API**  \n{API_URL}")

# Pedido de ejemplo, editable
ejemplos = pd.read_csv(DATOS / "pedidos_ejemplo.csv", dtype=str)
etiqueta = st.selectbox("Pedido de ejemplo", ejemplos["etiqueta"])
fila = ejemplos.loc[ejemplos["etiqueta"] == etiqueta].drop(columns="etiqueta").iloc[0]
editada = st.data_editor(pd.DataFrame({"valor": fila.fillna("")}),
                         use_container_width=True, height=420)


def a_json(valores):
    """Convierte la tabla editada en el JSON que espera la API."""
    pedido = {}
    for campo, valor in valores.items():
        valor = str(valor).strip()
        if valor == "" or valor.lower() == "nan":
            pedido[campo] = None
        elif campo in ENTEROS:
            pedido[campo] = int(float(valor))
        elif campo in DECIMALES:
            pedido[campo] = float(valor)
        else:
            pedido[campo] = valor
    return pedido


if st.button("Calcular riesgo", type="primary"):
    try:
        pedido = a_json(editada["valor"])
    except ValueError:
        st.error("Algún campo numérico tiene un valor no válido.")
        st.stop()

    with st.spinner("Consultando la API… si estaba inactiva, puede tardar hasta un minuto."):
        try:
            r = requests.post(f"{API_URL}/riesgo", json=pedido, timeout=90)
        except requests.exceptions.RequestException:
            st.error("La API no respondió. El servicio gratuito de Render se apaga cuando no "
                     "recibe visitas y puede tardar hasta un minuto en despertar. "
                     "Intente de nuevo en unos segundos.")
            st.stop()

    if r.status_code == 422:
        st.warning("La API rechazó el pedido: algún valor no es válido (por ejemplo, un precio "
                   "negativo o un campo obligatorio vacío).")
        st.json(r.json())
        st.stop()
    if r.status_code != 200:
        st.error(f"La API respondió con un error ({r.status_code}). Intente de nuevo más tarde.")
        st.stop()

    res = r.json()
    c1, c2 = st.columns(2)
    c1.metric("Probabilidad de 1–2 estrellas", f"{res['probabilidad']:.0%}")
    c2.metric("Umbral de riesgo alto (10 % más riesgoso)", f"{res['umbral']:.0%}")
    if res["riesgo_alto"]:
        st.error("Riesgo alto: contactar al cliente")
    else:
        st.success("Riesgo bajo: no es prioridad de contacto")
    with st.expander("Respuesta completa de la API"):
        st.json(res)
