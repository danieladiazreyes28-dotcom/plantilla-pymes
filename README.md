# Control de ventas para pymes · plantilla de Excel + datos de ejemplo

Plantilla de Excel para que un negocio pequeño sepa **qué productos y canales le dejan más utilidad, cuánto le falta por cobrar y qué debe reponer**, con datos de ejemplo 100 % inventados y un conjunto de CSV listo para practicar SQL, Python o BigQuery.

> **Aviso:** el negocio, los clientes y las cifras son ficticios y se generaron con un script (semilla fija). No representan a ningún negocio real, y los hallazgos de abajo son solo una demostración de la plantilla.

**Autora:** Daniela Díaz · versión 1.0 · noviembre de 2026

---

## Recomendación (primero lo importante)

Si tienes un negocio pequeño y hoy llevas las ventas en un cuaderno o en WhatsApp, empieza registrando **una fila por producto vendido** en la hoja `Ventas` y revisa el `Resumen` cada semana. Con tres semanas de datos ya puedes responder tres decisiones concretas:

1. **Qué reponer** antes de quedarte sin stock (hoja `Productos`, columna *Alerta*).
2. **A quién cobrarle** (hoja `Clientes`, columna *Por cobrar*).
3. **Dónde poner esfuerzo** según canal, categoría y producto (hoja `Resumen`).

## Contexto

Muchas pymes no usan un sistema contable porque es caro o complicado, pero sí necesitan ver su negocio con números. Esta plantilla usa solo Excel: sin macros, sin instalaciones y con fórmulas simples (`SUMIFS`, `INDEX`, `MATCH`) que funcionan en Excel y en otros programas de hojas de cálculo. Los datos de ejemplo simulan una tienda pequeña de café, snacks, regalos, hogar y papelería en Guatemala durante 12 meses (noviembre 2025 a octubre 2026).

## Qué incluye

```
control-ventas-pyme/
├── plantilla/
│   ├── plantilla_control_ventas_pyme.xlsx   ← CON datos de ejemplo (para explorar)
│   └── plantilla_vacia.xlsx                 ← VACÍA (para tus datos)
├── datos/
│   ├── ventas.csv                           ← 494 ventas
│   ├── productos.csv                        ← 15 productos
│   └── clientes.csv                         ← 21 clientes
├── sql/
│   └── consultas_ejemplo.sql                ← 8 consultas (sintaxis BigQuery)
├── scripts/
│   └── generar_datos.py                     ← regenera los CSV (semilla fija)
├── docs/
│   └── diccionario_de_datos.md              ← qué significa cada columna
├── README.md
├── LICENSE                                  ← MIT
└── .gitignore
```

## Cómo usar la plantilla (5 pasos)

1. **Productos:** escribe tu catálogo (SKU, nombre, categoría, precio, costo, stock inicial y punto de reorden).
2. **Clientes:** registra tus clientes. Para ventas de mostrador usa un ID genérico, por ejemplo `C000`.
3. **Listas:** ajusta categorías, métodos de pago y canales; de ahí salen los menús desplegables.
4. **Ventas:** una fila por producto vendido. Llena solo las columnas **verdes (A a I)**; las **grises (J a P)** se calculan solas.
5. **Resumen:** se actualiza solo. Cambia el mes inicial (celda amarilla `B7`) para ver otro periodo de 12 meses.

Código de colores: encabezado verde y texto azul = lo escribes tú · encabezado gris = fórmula automática (no la borres) · celda amarilla = ajuste del resumen.

## Los datos

| Archivo | Filas | Qué contiene |
|---|---|---|
| `ventas.csv` | 494 | Una fila por producto vendido: fecha, cliente, SKU, cantidad, precio, descuento, total, costo, utilidad, método de pago, estado de cobro y canal |
| `productos.csv` | 15 | Catálogo con precio, costo, stock inicial, reposiciones y punto de reorden |
| `clientes.csv` | 21 | Clientes minoristas y mayoristas, más un ID de mostrador (`C000`) |

Columna por columna: [`docs/diccionario_de_datos.md`](docs/diccionario_de_datos.md). Para regenerar los CSV: `python3 scripts/generar_datos.py` (solo usa la biblioteca estándar de Python y produce siempre los mismos archivos).

## Qué muestran los datos de ejemplo

| Indicador | Valor |
|---|---|
| Ventas totales (12 meses) | Q105,586.00 |
| Utilidad | Q40,880.00 (margen 38.7 %) |
| N.º de ventas / ticket promedio | 494 / Q213.74 |
| Por cobrar | Q11,555.65 (10.9 % de las ventas) |
| Mes más fuerte | Diciembre 2025 (Q15,321.20), por los regalos |
| Producto con más ventas | Café en grano 500 g (Q16,035.10) |
| Canal con más ventas | WhatsApp, 57.0 % (concentra las ventas a mayoristas) |
| Método de pago más usado | Transferencia, 64.1 % del monto |
| Productos con alerta de reposición | Café en grano 500 g, Té de hierbas, Canasta de regalo grande |

**Lectura de negocio (ficticia):** las ventas a mayoristas por WhatsApp sostienen el negocio, pero también concentran lo que queda por cobrar, así que el mayor riesgo no es vender sino cobrar. Dos de los productos que más venden están a punto de agotarse.

## Practicar con SQL, Python o BigQuery

Los CSV están pensados para cargarse en BigQuery (modo *sandbox*, gratuito) o en cualquier base de datos. En `sql/consultas_ejemplo.sql` hay 8 consultas: ventas por mes, por categoría y por canal, top de productos, cuentas por cobrar por cliente, productos a reponer y más. Cambia `mi_proyecto.control_ventas` por tu proyecto y dataset.

## Limitaciones

- **Datos inventados:** no sirven para sacar conclusiones sobre ningún negocio real.
- **Capacidad:** 1,000 ventas, 100 productos y 200 clientes. Para ampliar, inserta filas *dentro* del rango (no al final) y copia las fórmulas grises hacia abajo.
- **Una fila = un producto.** Una compra de tres productos son tres filas.
- **No calcula** impuestos (como el IVA), devoluciones ni compras a proveedores.
- **El costo es fijo por producto;** no promedia cambios de costo en el tiempo.
- **Stock actual** = stock inicial + reposiciones − unidades vendidas; cada reposición se suma a mano.
- Se verificó que el libro recalcula sin errores y que sus totales coinciden con los CSV. No se probó en todas las versiones de Excel.
- Las consultas SQL siguen la sintaxis de BigQuery y no se ejecutaron en BigQuery al prepararlas, así que revísalas antes de usarlas.

## Licencia

MIT. Puedes copiar, adaptar y compartir esta plantilla; se agradece mencionar la fuente.
