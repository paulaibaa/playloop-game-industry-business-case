# Corrección de fechas — 15/10/2026

Se sustituyó la inferencia mixta por formatos explícitos: `%Y-%m-%d`, `%d/%m/%Y` y meses escritos convertidos a números. La conversión falla si encuentra valores no reconocidos.

Se ejecutó de nuevo la limpieza, se regeneraron los siete CSV y se actualizaron las seis tablas con fechas en PostgreSQL dentro de una transacción. Se conservaron todas las filas y los criterios de limpieza. El catálogo no tiene fechas.

La selección de usuarios por última instalación cambió también version_app en 10 registros. Se sincronizaron estas versiones con el CSV regenerado. Las demás columnas se compararon antes de actualizar.

No quedan fechas nulas ni posteriores al corte 22/07/2024. Desaparecieron las dos combinaciones repetidas de canal-fecha en gasto_ua.

DAU verificado: 601,4821429, redondeado 601, en 56 días (28/05–22/07). Sin el filtro de duración, las sesiones deduplicadas dan 602,1071429, redondeado 602. Las 60 sesiones excluidas por duración representan 35 combinaciones usuario-día adicionales. Se conserva el criterio acordado.

El script scripts/actualizar_fechas.py permite sincronizar estas fechas con tablas ya cargadas sin borrar registros.
