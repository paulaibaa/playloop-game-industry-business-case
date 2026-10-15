"""Actualiza solo fechas desde los CSV corregidos, con transacción."""
from pathlib import Path
import pandas as pd
from dotenv import dotenv_values
from sqlalchemy import URL, create_engine, text

raiz = Path(__file__).resolve().parent.parent
c = dotenv_values(raiz / '.env')
engine = create_engine(URL.create('postgresql+psycopg2', username=c['DB_USER'],
    password=c['DB_PASSWORD'], host=c['DB_HOST'], port=int(c['DB_PORT']),
    database=c['DB_NAME']), connect_args={'connect_timeout': 5})
claves = {'usuarios':'user_id', 'sesiones':'evento_id', 'partidas':'partida_id',
          'compras':'compra_id', 'ingresos_ads':'id', 'gasto_ua':'id'}

# Una única transacción: cualquier error deshace todas las actualizaciones.
with engine.begin() as conexion:
    for nombre, clave in claves.items():
        columna = 'fecha_instalacion' if nombre == 'usuarios' else 'fecha'
        actual = pd.read_sql(text(f'SELECT * FROM public.{nombre}'), conexion)
        nuevo = pd.read_csv(raiz / 'data/processed' / f'{nombre}_limpio.csv')
        assert len(actual) == len(nuevo), f'Recuento diferente en {nombre}'
        # gasto_ua tiene un ID generado en PostgreSQL: recuperamos ese ID
        # usando las cantidades y el canal, que no han cambiado.
        if nombre == 'gasto_ua':
            campos = ['canal','gasto','instalaciones','impresiones','clics']
            assert not actual.duplicated(campos).any()
            assert not nuevo.duplicated(campos).any()
            nuevo = nuevo.merge(actual[campos + ['id']], on=campos,
                                 how='left', validate='one_to_one')
            assert nuevo.id.notna().all()
        assert set(nuevo[clave]) == set(actual[clave])
        # Verificamos que todos los campos distintos de fecha se conservan.
        excluir = [columna, 'version_app'] if nombre == 'usuarios' else [columna]
        a = actual.drop(columns=excluir).sort_values(clave).reset_index(drop=True)
        b = nuevo.drop(columns=excluir)[a.columns].sort_values(clave).reset_index(drop=True)
        pd.testing.assert_frame_equal(a, b, check_dtype=False, check_exact=False)
        campos_actualizar = [columna, 'version_app'] if nombre == 'usuarios' else [columna]
        fechas = nuevo[[clave] + campos_actualizar].copy()
        fechas[columna] = pd.to_datetime(fechas[columna], format='%Y-%m-%d').dt.date
        # La tabla temporal contiene solo las claves y fechas que vamos a aplicar.
        columnas_sql = ', '.join([clave] + campos_actualizar)
        conexion.execute(text(f'CREATE TEMP TABLE fechas_actualizar ON COMMIT DROP AS SELECT {columnas_sql} FROM public.{nombre} WITH NO DATA'))
        esquema_temp = conexion.execute(text('SELECT nspname FROM pg_namespace WHERE oid = pg_my_temp_schema()')).scalar_one()
        fechas.to_sql('fechas_actualizar', conexion, schema=esquema_temp,
                      if_exists='append', index=False, chunksize=2000)
        asignaciones = ', '.join(f'{campo} = s.{campo}' for campo in campos_actualizar)
        diferencias = ' OR '.join(f'd.{campo} IS DISTINCT FROM s.{campo}' for campo in campos_actualizar)
        cambio = conexion.execute(text(f'''
            UPDATE public.{nombre} AS d SET {asignaciones}
            FROM pg_temp.fechas_actualizar AS s
            WHERE d.{clave} = s.{clave} AND ({diferencias})
        '''))
        print(nombre, 'fechas actualizadas:', cambio.rowcount)
        conexion.execute(text('DROP TABLE pg_temp.fechas_actualizar'))
    resultado = conexion.execute(text('''
        WITH diarios AS (
            SELECT fecha, COUNT(DISTINCT user_id) AS activos
            FROM public.sesiones GROUP BY fecha
        )
        SELECT ROUND(AVG(activos), 0), COUNT(*), MIN(fecha), MAX(fecha) FROM diarios
    ''')).one()
print('Fechas guardadas. DAU, días y rango:', resultado)
engine.dispose()
