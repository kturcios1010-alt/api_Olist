from pathlib import Path

import pandas as pd
import streamlit as st

DATOS = Path(__file__).resolve().parents[1] / "datos"
ORDEN = ["negative", "neutral", "positive"]

st.title("Comentarios: sentimiento contra estrellas")
st.caption("Resultados de la Parte 4: modelo preentrenado "
           "cardiffnlp/twitter-xlm-roberta-base-sentiment aplicado a una muestra de comentarios.")

datos = pd.read_csv(DATOS / "sentimiento_muestra.csv")

c1, c2, c3 = st.columns(3)
c1.metric("Comentarios analizados", f"{len(datos):,}")
c2.metric("Coincidencia con las estrellas", f"{datos['coincide'].mean():.1%}")
c3.metric("Desacuerdos", f"{(~datos['coincide']).sum():,}")

st.subheader("Tabla cruzada")
st.caption("Filas: estrellas agrupadas (1–2 negativo, 3 neutro, 4–5 positivo). "
           "Columnas: sentimiento del texto según el modelo.")
izq, der = st.columns(2)
izq.markdown("**Cantidad de comentarios**")
izq.dataframe(pd.crosstab(datos["estrellas_grupo"], datos["sentimiento"])
              .reindex(index=ORDEN, columns=ORDEN))
der.markdown("**Porcentaje por fila**")
der.dataframe((pd.crosstab(datos["estrellas_grupo"], datos["sentimiento"], normalize="index")
               .reindex(index=ORDEN, columns=ORDEN) * 100).round(1))

st.subheader("Desacuerdos clasificados")
if "clasificacion_desacuerdo" in datos.columns:
    st.dataframe(datos.dropna(subset=["clasificacion_desacuerdo"])
                 [["review_score", "sentimiento", "confianza", "texto",
                   "clasificacion_desacuerdo"]],
                 use_container_width=True)

st.subheader("Explorar comentarios")
f1, f2, f3 = st.columns(3)
estrellas = f1.multiselect("Estrellas agrupadas", ORDEN, default=ORDEN)
sentimiento = f2.multiselect("Sentimiento del modelo", ORDEN, default=ORDEN)
solo_desacuerdos = f3.checkbox("Solo desacuerdos", value=True)

filtro = datos["estrellas_grupo"].isin(estrellas) & datos["sentimiento"].isin(sentimiento)
if solo_desacuerdos:
    filtro &= ~datos["coincide"]
st.write(f"{filtro.sum():,} comentarios")
st.dataframe(datos.loc[filtro, ["review_score", "estrellas_grupo", "sentimiento",
                                "confianza", "texto"]]
             .sort_values("confianza", ascending=False),
             use_container_width=True)
