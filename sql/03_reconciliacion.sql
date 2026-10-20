-- Todo registro de Bronze debe terminar en Silver o en cuarentena.
SELECT (SELECT COUNT(*) FROM brz_erp_oc_linea)        AS bronze,
       (SELECT COUNT(*) FROM slv_oc_linea)            AS silver,
       (SELECT COUNT(*) FROM slv_oc_linea_cuarentena) AS cuarentena;
