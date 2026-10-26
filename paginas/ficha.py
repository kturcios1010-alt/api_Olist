from pathlib import Path

import streamlit as st

DATOS = Path(__file__).resolve().parents[1] / "datos"

st.markdown((DATOS / "ficha_modelo.md").read_text(encoding="utf-8"))
