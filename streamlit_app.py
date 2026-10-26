import streamlit as st

st.set_page_config(page_title="Olist · Riesgo de mala reseña", page_icon="📦", layout="wide")

paginas = st.navigation([
    st.Page("paginas/riesgo.py",      title="Riesgo de un pedido",     icon="⚠️", default=True),
    st.Page("paginas/comentarios.py", title="Comentarios",             icon="💬"),
    st.Page("paginas/segmentos.py",   title="Segmentos de vendedores", icon="🧩"),
    st.Page("paginas/ficha.py",       title="Ficha del modelo",        icon="📄"),
])
paginas.run()
