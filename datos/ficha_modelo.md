# Ficha del modelo · Riesgo de mala reseña (Olist)

## 1. Para qué sirve y para qué no

**Sirve para** decidir a qué clientes llamar primero justo después de la entrega. El modelo
estima, para cada pedido entregado, la probabilidad de que el cliente deje una reseña de 1 o 2
estrellas. Atención al cliente puede llamar a 1 de cada 10 pedidos; el modelo indica cuáles.

**No debe usarse para:**
- Evaluar, sancionar o excluir vendedores. El modelo califica pedidos, no vendedores, y gran
  parte del retraso depende del transportista.
- Decidir reembolsos, descuentos o beneficios para un cliente.
- Predecir antes de la entrega: usa la fecha real de entrega, que solo se conoce al final.

## 2. Datos

- **Origen:** pedidos públicos de Olist (plataforma brasileña de comercio electrónico),
  cargados en la base de datos del curso.
- **Periodo:** compras del 15/09/2016 al 31/05/2018.
- **Pedidos:** 77,304 pedidos entregados y con reseña.
- **Qué se excluyó y por qué:**
  - Pedidos no entregados o sin fecha de entrega: el modelo se usa en el momento de la entrega.
  - Pedidos sin reseña: no se sabe si el cliente quedó satisfecho.
  - Pedidos desde el 1 de junio de 2018: se reservan para evaluar el modelo con pedidos que
    nunca vio.
  - El texto y las fechas de la reseña: aparecen después de la entrega, y usarlos sería hacer
    trampa con información del futuro.

## 3. Qué tan bien funciona

El modelo se probó con pedidos más recientes que los que usó para aprender.

| Periodo de prueba | Con el modelo | Llamando a los más atrasados | Llamando al azar |
|---|---|---|---|
| Abril–mayo 2018 (pocos retrasos) | 4.4 de cada 10 | 3.4 de cada 10 | 1.1 de cada 10 |
| Febrero–marzo 2018 (muchos retrasos) | 8.2 de cada 10 | 8.3 de cada 10 | 2.0 de cada 10 |

En palabras simples: **de cada 10 clientes que se llaman, unos 4 iban a dejar una mala reseña**
en un periodo normal, frente a 1 si se eligieran al azar. Con muchos retrasos, el modelo rinde
igual que llamar a los pedidos más atrasados; con pocos retrasos, es claramente mejor.

Lo que más pesa en el modelo: los días de retraso frente a la fecha prometida (64.2 % de mala
reseña en pedidos tardíos frente a 9.5 % en puntuales) y la cantidad de artículos del pedido
(27.5 % con varios artículos frente a 12.0 % con uno solo).

## 4. Límites conocidos

- **Depende mucho del retraso.** Si los retrasos cambian (huelgas, temporadas altas como Black
  Friday o un nuevo transportista), su desempeño cambia.
- **En periodos con pocas malas reseñas, acierta menos.** Hay menos casos que encontrar: pasó
  de 8.2 a 4.4 de cada 10 entre febrero–marzo y abril–mayo de 2018.
- **No ve la calidad del producto.** Un producto defectuoso entregado a tiempo puede no
  detectarse.
- **Aprendió con datos de Brasil entre 2016 y 2018.** Puede no aplicar igual a otros países,
  productos o épocas.
- **No explica la causa de cada caso.** Indica qué pedidos tienen más riesgo, no por qué se
  quejará el cliente.

## 5. A quién afecta un error

- **Falso positivo** (se llama a un cliente que no iba a quejarse): unos 6 de cada 10 llamadas
  en un periodo normal. El costo es el tiempo del agente y una llamada que el cliente no
  necesitaba; el daño es bajo.
- **Falso negativo** (no se llama a un cliente que sí deja mala reseña): se pierde la
  oportunidad de resolver el problema, y el vendedor y Olist reciben la mala reseña.
- **Riesgo de mal uso:**
  - Usar el puntaje para castigar vendedores sería injusto: el vendedor despacha en unos 2 días
    (mediana), pero la entrega total tarda unos 11 días, y la mayor parte depende del
    transportista.
  - El modelo considera el estado de Brasil del cliente y del vendedor. Los clientes de
    regiones con más retrasos recibirán más llamadas; esto es útil, pero conviene vigilar que
    ninguna región quede sin atención por completo.

## 6. Recomendación de uso

- **Cómo usarlo:** cada día, ordenar los pedidos entregados por probabilidad y llamar al 10 %
  de mayor riesgo. El umbral de 26.8 % sirve como alerta, pero no debe usarse como corte fijo:
  en periodos tranquilos, menos del 10 % de los pedidos lo supera y quedaría capacidad sin usar.
- **Supervisión humana:** el agente decide qué ofrecer en cada llamada. El modelo solo
  prioriza; ninguna decisión sobre clientes o vendedores debe tomarse sin revisión humana.
- **Revisión:** medir cada mes cuántos de los clientes llamados tenían un problema real y
  compararlo con llamar a los más atrasados. Reentrenar el modelo cada trimestre, o antes si la
  tasa de malas reseñas cambia mucho, por ejemplo en temporadas altas o ante problemas
  logísticos.
