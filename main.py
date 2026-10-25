import json
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

import preparacion  # el pipeline guardado usa preparacion.crear_variables

# ---------- Carga del modelo y del umbral (una sola vez, al iniciar) ----------
CARPETA = Path(__file__).parent
modelo = joblib.load(CARPETA / "modelo_riesgo.joblib")
UMBRAL = json.loads((CARPETA / "umbral.json").read_text())["umbral"]

COLUMNAS = ["order_id", "order_purchase_timestamp", "order_approved_at",
            "order_delivered_carrier_date", "order_delivered_customer_date",
            "order_estimated_delivery_date", "estado_cliente", "n_items", "n_vendedores",
            "precio_total", "flete_total", "peso_total_g", "fotos_promedio", "categoria",
            "estado_vendedor", "tipo_pago", "cuotas_max"]
NUMERICAS = ["n_items", "n_vendedores", "precio_total", "flete_total",
             "peso_total_g", "fotos_promedio", "cuotas_max"]
FECHAS = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
          "order_delivered_customer_date", "order_estimated_delivery_date"]


# ---------- Esquema de entrada: las 17 columnas del contrato ----------
class Pedido(BaseModel):
    order_id: str
    order_purchase_timestamp: str
    order_approved_at: Optional[str] = None
    order_delivered_carrier_date: Optional[str] = None
    order_delivered_customer_date: str
    order_estimated_delivery_date: str
    estado_cliente: str
    n_items: int = Field(ge=1)
    n_vendedores: int = Field(ge=1)
    precio_total: float = Field(ge=0)
    flete_total: float = Field(ge=0)
    peso_total_g: Optional[float] = Field(default=None, ge=0)
    fotos_promedio: Optional[float] = Field(default=None, ge=0)
    categoria: Optional[str] = None
    estado_vendedor: str
    tipo_pago: Optional[str] = None
    cuotas_max: Optional[float] = Field(default=None, ge=0)

    @field_validator(*FECHAS)
    @classmethod
    def fecha_valida(cls, valor):
        if valor is not None and pd.isna(pd.to_datetime(valor, errors="coerce")):
            raise ValueError("Fecha no válida. Formato esperado: '2018-03-07 22:02:23'")
        return valor


# ---------- La API ----------
app = FastAPI(
    title="API de riesgo de mala reseña · Olist",
    description="Recibe un pedido entregado (17 columnas del contrato) y devuelve la "
                "probabilidad de una reseña de 1–2 estrellas.",
    version="1.0",
)


@app.get("/")
def inicio():
    return {"estado": "activa",
            "mensaje": "API de riesgo de mala reseña. Documentación en /docs",
            "umbral_riesgo_alto": round(UMBRAL, 4)}


@app.post("/riesgo")
def riesgo(pedido: Pedido):
    fila = pd.DataFrame([pedido.model_dump()])[COLUMNAS]
    fila[NUMERICAS] = fila[NUMERICAS].apply(pd.to_numeric, errors="coerce")
    prob = float(modelo.predict_proba(fila)[:, 1][0])
    return {"order_id": pedido.order_id,
            "probabilidad": round(prob, 4),
            "riesgo_alto": prob >= UMBRAL,
            "umbral": round(UMBRAL, 4)}
