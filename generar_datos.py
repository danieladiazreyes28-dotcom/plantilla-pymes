#!/usr/bin/env python3
"""
generar_datos.py
================
Genera los datos de EJEMPLO (100 % inventados) de la plantilla "Control de ventas para pymes".

- Negocio ficticio: una tienda pequeña de café, snacks, regalos, hogar y papelería en Guatemala.
- Periodo: 1 de noviembre de 2025 al 31 de octubre de 2026 (12 meses).
- Semilla fija: si lo ejecutas de nuevo obtienes exactamente los mismos archivos.
- Solo usa la biblioteca estándar de Python (no necesitas instalar nada).

Uso:
    python3 scripts/generar_datos.py                 # escribe en ./datos
    python3 scripts/generar_datos.py --salida otra_carpeta

Cualquier parecido con negocios, clientes o cifras reales es pura coincidencia.
"""

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEMILLA = 2026
FECHA_INICIO = date(2025, 11, 1)
FECHA_FIN = date(2026, 10, 31)

# --------------------------------------------------------------------------------------
# Catálogo de productos: (sku, producto, categoría, precio de venta Q, costo unitario Q, popularidad)
# --------------------------------------------------------------------------------------
PRODUCTOS = [
    ("CAF-001", "Café molido 250 g", "Café y bebidas", 45.00, 28.00, 10),
    ("CAF-002", "Café en grano 500 g", "Café y bebidas", 82.00, 52.00, 7),
    ("CAF-003", "Té de hierbas (caja)", "Café y bebidas", 32.00, 18.00, 5),
    ("CAF-004", "Chocolate de mesa", "Café y bebidas", 28.00, 16.00, 6),
    ("SNK-001", "Granola artesanal 300 g", "Snacks", 38.00, 21.00, 8),
    ("SNK-002", "Nueces mixtas 200 g", "Snacks", 42.00, 26.00, 5),
    ("SNK-003", "Plátano deshidratado 150 g", "Snacks", 25.00, 13.00, 6),
    ("SNK-004", "Barra de amaranto", "Snacks", 10.00, 5.50, 12),
    ("REG-001", "Canasta de regalo pequeña", "Regalos", 150.00, 95.00, 3),
    ("REG-002", "Canasta de regalo grande", "Regalos", 260.00, 170.00, 2),
    ("HOG-001", "Taza artesanal", "Hogar", 55.00, 30.00, 4),
    ("HOG-002", "Vela aromática", "Hogar", 48.00, 25.00, 4),
    ("PAP-001", "Cuaderno artesanal", "Papelería", 35.00, 18.00, 5),
    ("PAP-002", "Set de tarjetas (6 u.)", "Papelería", 22.00, 10.00, 5),
    ("PAP-003", "Agenda anual", "Papelería", 75.00, 40.00, 2),
]

CATEGORIAS_ESTACIONALES = {
    # mes -> {categoría: multiplicador de popularidad}
    12: {"Regalos": 3.0, "Hogar": 1.8, "Café y bebidas": 1.4},
    11: {"Regalos": 1.5, "Papelería": 1.3},
    2: {"Regalos": 1.8},
    5: {"Regalos": 1.9, "Hogar": 1.4},   # Día de la Madre (10 de mayo)
    1: {"Papelería": 1.5},
}

# Multiplicador mensual del número de ventas (estacionalidad inventada)
FACTOR_MES = {11: 1.25, 12: 1.70, 1: 0.80, 2: 0.90, 3: 0.95, 4: 1.00,
              5: 1.10, 6: 1.00, 7: 0.95, 8: 1.00, 9: 1.05, 10: 1.10}
VENTAS_BASE_MES = 36

CIUDADES = ["Guatemala", "Mixco", "Villa Nueva", "Antigua Guatemala", "Quetzaltenango"]
CANALES_MINORISTA = [("Tienda física", 40), ("Instagram", 25), ("WhatsApp", 20), ("Feria", 15)]
PAGOS_MINORISTA = [("Efectivo", 40), ("Tarjeta", 30), ("Transferencia", 25), ("Link de pago", 5)]
PAGOS_MAYORISTA = [("Transferencia", 80), ("Efectivo", 20)]


def elegir(opciones):
    """Elige un valor de una lista [(valor, peso), ...]."""
    valores, pesos = zip(*opciones)
    return random.choices(valores, weights=pesos, k=1)[0]


def generar_clientes():
    clientes = [("C000", "Venta de mostrador (sin registro)", "Minorista", "Guatemala")]
    for i in range(1, 15):
        clientes.append((f"C{i:03d}", f"Cliente Minorista {i:02d}", "Minorista", random.choice(CIUDADES)))
    for i in range(1, 7):
        clientes.append((f"C{14 + i:03d}", f"Cliente Mayorista {i:02d}", "Mayorista", random.choice(CIUDADES)))
    return clientes


def dias_del_mes(anio, mes):
    d = date(anio, mes, 1)
    while d.month == mes:
        yield d
        d += timedelta(days=1)


def peso_dia(d):
    # viernes y sábado venden más; domingo menos
    return {4: 1.6, 5: 2.0, 6: 0.6}.get(d.weekday(), 1.0)


def generar_ventas(clientes):
    minoristas = [c for c in clientes if c[2] == "Minorista" and c[0] != "C000"]
    mayoristas = [c for c in clientes if c[2] == "Mayorista"]
    lineas = []
    anio, mes = FECHA_INICIO.year, FECHA_INICIO.month
    mes_idx = 0
    while date(anio, mes, 1) <= FECHA_FIN:
        tendencia = 1 + 0.012 * mes_idx
        n = round(VENTAS_BASE_MES * FACTOR_MES[mes] * tendencia + random.uniform(-3, 3))
        dias = list(dias_del_mes(anio, mes))
        pesos_dias = [peso_dia(d) for d in dias]
        estacional = CATEGORIAS_ESTACIONALES.get(mes, {})
        pesos_prod = [p[5] * estacional.get(p[2], 1.0) for p in PRODUCTOS]
        for _ in range(n):
            fecha = random.choices(dias, weights=pesos_dias, k=1)[0]
            prod = random.choices(PRODUCTOS, weights=pesos_prod, k=1)[0]
            es_mayorista = random.random() < 0.22
            es_canasta = prod[2] == "Regalos"
            if es_mayorista:
                cli = random.choice(mayoristas)
                cantidad = random.randint(3, 10) if es_canasta else random.randint(6, 24)
                descuento = 0.10 if cantidad >= 20 else (0.05 if cantidad >= 10 else 0.0)
                pago = elegir(PAGOS_MAYORISTA)
                canal = "WhatsApp" if random.random() < 0.7 else "Tienda física"
            else:
                cli = ("C000",) if random.random() < 0.55 else random.choice(minoristas)
                cantidad = random.choice([1, 1, 2]) if es_canasta else random.choice([1, 1, 1, 2, 2, 3, 4])
                descuento = 0.05 if random.random() < 0.08 else 0.0
                pago = elegir(PAGOS_MINORISTA)
                canal = elegir(CANALES_MINORISTA)
                if canal == "Feria" and fecha.weekday() < 5:
                    canal = "Tienda física"
            # Estado de cobro: los mayoristas recientes suelen estar pendientes
            if es_mayorista and fecha >= date(2026, 9, 16):
                estado = "Pendiente" if random.random() < 0.6 else "Pagado"
            elif es_mayorista:
                estado = "Pendiente" if random.random() < 0.02 else "Pagado"
            else:
                estado = "Pendiente" if (pago == "Transferencia" and random.random() < 0.015) else "Pagado"
            lineas.append({
                "fecha": fecha, "id_cliente": cli[0], "sku": prod[0], "cantidad": cantidad,
                "precio_unitario": prod[3], "costo_unitario": prod[4], "descuento_pct": descuento,
                "metodo_pago": pago, "estado_cobro": estado, "canal": canal,
            })
        mes_idx += 1
        mes += 1
        if mes == 13:
            mes, anio = 1, anio + 1
    lineas.sort(key=lambda r: (r["fecha"], r["id_cliente"], r["sku"]))
    filas = []
    for i, r in enumerate(lineas, start=1):
        total = round(r["cantidad"] * r["precio_unitario"] * (1 - r["descuento_pct"]), 2)
        costo = round(r["cantidad"] * r["costo_unitario"], 2)
        filas.append({
            "id_venta": f"V{i:04d}", "fecha": r["fecha"].isoformat(), "id_cliente": r["id_cliente"],
            "sku": r["sku"], "cantidad": r["cantidad"], "precio_unitario": f'{r["precio_unitario"]:.2f}',
            "descuento_pct": f'{r["descuento_pct"]:.2f}', "total": f"{total:.2f}",
            "costo_total": f"{costo:.2f}", "utilidad": f"{total - costo:.2f}",
            "metodo_pago": r["metodo_pago"], "estado_cobro": r["estado_cobro"], "canal": r["canal"],
        })
    return filas


def generar_inventario(ventas):
    vendido = {}
    for v in ventas:
        vendido[v["sku"]] = vendido.get(v["sku"], 0) + v["cantidad"]
    filas = []
    alertas = {"CAF-002": 4, "REG-002": 5}   # dos productos quedan en "Reponer" a propósito
    for sku, nombre, cat, precio, costo, _ in PRODUCTOS:
        vend = vendido.get(sku, 0)
        inicial = random.randint(60, 160)
        if sku in alertas:
            colchon = alertas[sku]
            inicial = min(inicial, vend + colchon)   # así el stock final queda justo en el colchón
            repos = max(0, vend + colchon - inicial)
        else:
            colchon = random.randint(14, 60)
            repos = max(0, vend + colchon - inicial)
            repos = ((repos + 9) // 10) * 10
        reorden = max(8, round(vend / 10))
        filas.append({
            "sku": sku, "producto": nombre, "categoria": cat,
            "precio_venta": f"{precio:.2f}", "costo_unitario": f"{costo:.2f}",
            "stock_inicial": inicial, "reposiciones": repos, "punto_reorden": reorden,
        })
    return filas


def escribir_csv(ruta, filas, columnas):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)


def main():
    ap = argparse.ArgumentParser(description="Genera los CSV de ejemplo (datos inventados).")
    ap.add_argument("--salida", default="datos", help="Carpeta de salida (por defecto: datos)")
    args = ap.parse_args()
    random.seed(SEMILLA)
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    clientes = generar_clientes()
    ventas = generar_ventas(clientes)
    inventario = generar_inventario(ventas)

    escribir_csv(salida / "clientes.csv",
                 [dict(zip(["id_cliente", "nombre", "tipo", "ciudad"], c)) for c in clientes],
                 ["id_cliente", "nombre", "tipo", "ciudad"])
    escribir_csv(salida / "productos.csv", inventario,
                 ["sku", "producto", "categoria", "precio_venta", "costo_unitario",
                  "stock_inicial", "reposiciones", "punto_reorden"])
    escribir_csv(salida / "ventas.csv", ventas,
                 ["id_venta", "fecha", "id_cliente", "sku", "cantidad", "precio_unitario",
                  "descuento_pct", "total", "costo_total", "utilidad", "metodo_pago",
                  "estado_cobro", "canal"])
    print(f"Listo: {len(clientes)} clientes, {len(inventario)} productos, {len(ventas)} ventas en '{salida}/'")


if __name__ == "__main__":
    main()
