-- OTD correcto: a tiempo / TODAS las líneas vencidas (incluidas las no recibidas).
-- Parámetro :corte  (fecha de corte, formato AAAA-MM-DD)
SELECT id_proveedor,
       COUNT(*) AS vencidas,
       SUM(CASE WHEN fecha_recepcion IS NOT NULL AND fecha_recepcion <= fecha_prometida
                THEN 1 ELSE 0 END) AS a_tiempo,
       ROUND(100.0 * SUM(CASE WHEN fecha_recepcion IS NOT NULL AND fecha_recepcion <= fecha_prometida
                              THEN 1 ELSE 0 END) / COUNT(*), 1) AS otd_correcto
FROM slv_oc_linea
WHERE fecha_prometida <= :corte
GROUP BY id_proveedor
ORDER BY id_proveedor;
