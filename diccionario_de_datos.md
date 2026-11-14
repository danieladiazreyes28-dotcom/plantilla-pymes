# Diccionario de datos

Todos los datos son **inventados** (negocio ficticio). Montos en quetzales (Q). Fechas en formato `AAAA-MM-DD`. Codificación UTF-8, separador coma.

## `ventas.csv` (una fila por producto vendido)

| Columna | Tipo | Descripción |
|---|---|---|
| `id_venta` | texto | Identificador único de la fila (V0001, V0002, ...) |
| `fecha` | fecha | Día de la venta |
| `id_cliente` | texto | Cliente (ver `clientes.csv`). `C000` = venta de mostrador sin registro |
| `sku` | texto | Código del producto (ver `productos.csv`) |
| `cantidad` | entero | Unidades vendidas |
| `precio_unitario` | decimal | Precio de venta por unidad, sin descuento |
| `descuento_pct` | decimal (0 a 1) | Descuento aplicado: `0.05` = 5 % |
| `total` | decimal | `cantidad × precio_unitario × (1 − descuento_pct)`, redondeado a 2 decimales |
| `costo_total` | decimal | `cantidad × costo_unitario` |
| `utilidad` | decimal | `total − costo_total` |
| `metodo_pago` | texto | Efectivo, Tarjeta, Transferencia o Link de pago |
| `estado_cobro` | texto | `Pagado` o `Pendiente` |
| `canal` | texto | Tienda física, Instagram, WhatsApp o Feria |

## `productos.csv`

| Columna | Tipo | Descripción |
|---|---|---|
| `sku` | texto | Código único del producto |
| `producto` | texto | Nombre |
| `categoria` | texto | Café y bebidas, Snacks, Regalos, Hogar o Papelería |
| `precio_venta` | decimal | Precio de venta por unidad |
| `costo_unitario` | decimal | Costo por unidad |
| `stock_inicial` | entero | Unidades al inicio del periodo |
| `reposiciones` | entero | Unidades compradas durante el periodo |
| `punto_reorden` | entero | Si el stock actual baja a este nivel o menos, se marca "Reponer" |

Stock actual = `stock_inicial + reposiciones − unidades vendidas`.

## `clientes.csv`

| Columna | Tipo | Descripción |
|---|---|---|
| `id_cliente` | texto | Identificador único (C000 a C020) |
| `nombre` | texto | Nombre ficticio |
| `tipo` | texto | `Minorista` o `Mayorista` |
| `ciudad` | texto | Guatemala, Mixco, Villa Nueva, Antigua Guatemala o Quetzaltenango |

## Cómo se simularon los datos

El script `scripts/generar_datos.py` usa una semilla fija (2026). Incluye estacionalidad (diciembre fuerte por regalos, enero flojo), más ventas viernes y sábado, descuentos por volumen a mayoristas y cobros pendientes concentrados en ventas recientes a mayoristas. Son supuestos del ejercicio, no datos observados.
