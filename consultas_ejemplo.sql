-- ============================================================================
-- Consultas de ejemplo para practicar con los CSV de esta plantilla (BigQuery)
-- ----------------------------------------------------------------------------
-- 1. Carga los tres CSV a un dataset de BigQuery como tablas: ventas, productos, clientes
--    (en la carga, elige "Detectar esquema automáticamente" y "Omitir 1 fila de encabezado").
-- 2. Cambia `mi_proyecto.control_ventas` por tu proyecto y dataset.
-- Nota: estas consultas no se ejecutaron en BigQuery al prepararlas; revísalas antes de usarlas.
-- Datos 100 % inventados.
-- ============================================================================

-- 1) Ventas y utilidad por mes
SELECT
  DATE_TRUNC(fecha, MONTH)                  AS mes,
  COUNT(*)                                  AS n_ventas,
  ROUND(SUM(total), 2)                      AS ventas,
  ROUND(SUM(utilidad), 2)                   AS utilidad,
  ROUND(SAFE_DIVIDE(SUM(utilidad), SUM(total)), 3) AS margen
FROM `mi_proyecto.control_ventas.ventas`
GROUP BY mes
ORDER BY mes;

-- 2) Ventas, utilidad y margen por categoría
SELECT
  p.categoria,
  ROUND(SUM(v.total), 2)                    AS ventas,
  ROUND(SUM(v.utilidad), 2)                 AS utilidad,
  ROUND(SAFE_DIVIDE(SUM(v.utilidad), SUM(v.total)), 3) AS margen
FROM `mi_proyecto.control_ventas.ventas`   AS v
JOIN `mi_proyecto.control_ventas.productos` AS p USING (sku)
GROUP BY p.categoria
ORDER BY ventas DESC;

-- 3) Top 5 productos por ventas
SELECT
  p.producto,
  SUM(v.cantidad)                           AS unidades,
  ROUND(SUM(v.total), 2)                    AS ventas
FROM `mi_proyecto.control_ventas.ventas`   AS v
JOIN `mi_proyecto.control_ventas.productos` AS p USING (sku)
GROUP BY p.producto
ORDER BY ventas DESC
LIMIT 5;

-- 4) Participación de cada canal en las ventas
SELECT
  canal,
  ROUND(SUM(total), 2)                      AS ventas,
  ROUND(SUM(total) / SUM(SUM(total)) OVER (), 3) AS participacion
FROM `mi_proyecto.control_ventas.ventas`
GROUP BY canal
ORDER BY ventas DESC;

-- 5) Cuentas por cobrar por cliente (solo ventas pendientes)
SELECT
  c.id_cliente,
  c.nombre,
  c.tipo,
  COUNT(*)                                  AS ventas_pendientes,
  ROUND(SUM(v.total), 2)                    AS por_cobrar
FROM `mi_proyecto.control_ventas.ventas`   AS v
JOIN `mi_proyecto.control_ventas.clientes` AS c USING (id_cliente)
WHERE v.estado_cobro = 'Pendiente'
GROUP BY c.id_cliente, c.nombre, c.tipo
ORDER BY por_cobrar DESC;

-- 6) Productos a reponer (stock actual <= punto de reorden)
WITH vendido AS (
  SELECT sku, SUM(cantidad) AS unidades_vendidas
  FROM `mi_proyecto.control_ventas.ventas`
  GROUP BY sku
)
SELECT
  p.sku,
  p.producto,
  p.stock_inicial + p.reposiciones - COALESCE(v.unidades_vendidas, 0) AS stock_actual,
  p.punto_reorden
FROM `mi_proyecto.control_ventas.productos` AS p
LEFT JOIN vendido AS v USING (sku)
WHERE p.stock_inicial + p.reposiciones - COALESCE(v.unidades_vendidas, 0) <= p.punto_reorden
ORDER BY stock_actual;

-- 7) Crecimiento de ventas frente al mes anterior (función de ventana)
WITH mensual AS (
  SELECT DATE_TRUNC(fecha, MONTH) AS mes, SUM(total) AS ventas
  FROM `mi_proyecto.control_ventas.ventas`
  GROUP BY mes
)
SELECT
  mes,
  ROUND(ventas, 2)                          AS ventas,
  ROUND(SAFE_DIVIDE(ventas - LAG(ventas) OVER (ORDER BY mes),
                    LAG(ventas) OVER (ORDER BY mes)), 3) AS cambio_vs_mes_anterior
FROM mensual
ORDER BY mes;

-- 8) Minoristas vs. mayoristas: ticket promedio y peso en el total
SELECT
  c.tipo,
  COUNT(*)                                  AS n_ventas,
  ROUND(AVG(v.total), 2)                    AS ticket_promedio,
  ROUND(SUM(v.total) / SUM(SUM(v.total)) OVER (), 3) AS participacion
FROM `mi_proyecto.control_ventas.ventas`   AS v
JOIN `mi_proyecto.control_ventas.clientes` AS c USING (id_cliente)
GROUP BY c.tipo;
