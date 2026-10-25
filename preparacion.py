import numpy as np
import pandas as pd

FECHAS = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
          "order_delivered_customer_date", "order_estimated_delivery_date"]

NUMERICAS = ["n_items", "n_vendedores", "precio_total", "flete_total", "peso_total_g",
             "fotos_promedio", "cuotas_max",
             "dias_retraso", "entregado_tarde", "dias_entrega", "dias_prometidos",
             "dias_aprobacion", "dias_transportista", "flete_relativo",
             "misma_region", "multi_vendedor"]

CATEGORICAS = ["estado_cliente", "estado_vendedor", "categoria", "tipo_pago"]


def _dias(fin, inicio):
    """Diferencia en días (con decimales) entre dos columnas de fechas."""
    return (fin - inicio).dt.total_seconds() / 86400


def crear_variables(df):
    """Convierte las columnas del contrato en las variables del modelo."""
    X = df.copy()

    # Las fechas pueden llegar como texto (por ejemplo, desde la API)
    for c in FECHAS:
        X[c] = pd.to_datetime(X[c], errors="coerce")

    compra     = X["order_purchase_timestamp"]
    aprobacion = X["order_approved_at"]
    transporte = X["order_delivered_carrier_date"]
    entrega    = X["order_delivered_customer_date"]
    prometida  = X["order_estimated_delivery_date"]

    # Retraso por días calendario (sin hora): entregar el día prometido vale 0
    X["dias_retraso"]    = (entrega.dt.normalize() - prometida.dt.normalize()).dt.days
    X["entregado_tarde"] = (X["dias_retraso"] > 0).astype(int)

    # Duraciones del proceso; las negativas (errores de registro) se recortan a 0
    X["dias_entrega"]       = _dias(entrega, compra).clip(lower=0)
    X["dias_prometidos"]    = _dias(prometida, compra).clip(lower=0)
    X["dias_aprobacion"]    = _dias(aprobacion, compra).clip(lower=0)
    X["dias_transportista"] = _dias(transporte, aprobacion).clip(lower=0)

    # Relaciones del pedido
    X["flete_relativo"] = (X["flete_total"] / X["precio_total"]).replace([np.inf, -np.inf], np.nan)
    X["misma_region"]   = (X["estado_cliente"] == X["estado_vendedor"]).astype(int)
    X["multi_vendedor"] = (X["n_vendedores"] > 1).astype(int)

    # Corrección de valores imposibles: todo pago tiene al menos una cuota
    X["cuotas_max"] = X["cuotas_max"].clip(lower=1)

    # Categóricas: el faltante se conserva como grupo propio
    for c in CATEGORICAS:
        X[c] = X[c].fillna("desconocida").astype(str)

    return X[NUMERICAS + CATEGORICAS]
