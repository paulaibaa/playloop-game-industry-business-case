# Importamos librerias
# Path permite construir y manejar rutas
# dotenv_values lee le archivo .env y devuelve sus datos en un diccionario
# Herraamientas para preparar la conexion y ejecutar consultas SQL en sqlalchemy
# Pandas leerá los CSV y enviará sus datos a PostgreSQL.
from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy import URL, create_engine, text
import pandas as pd

# Obtenemos la carpeta raiz del proyecto a partir de la ubi del scrip
raiz_proyecto = Path(__file__).resolve().parent.parent

# Construimos la ruta al archivo .env
ruta_env = raiz_proyecto / '.env'

# Leemos el contenido y guardamos como dic
configuracion = dotenv_values(ruta_env)

# Comprobamos la ruta y el nombre de la base de datos, no mostramos la contraaseña
print("Archivo de configuración:",ruta_env)
print("Base de daots:",configuracion.get('DB_NAME'))


# Construimos la direccion de conexión con los valores del .env
# PostgreSQL es la base de datos y psycopg2 el controlador
url = URL.create(
    'postgresql+psycopg2',
    username=configuracion['DB_USER'],
    password=configuracion['DB_PASSWORD'],
    host=configuracion['DB_HOST'],
    port=int(configuracion['DB_PORT']),
    database=configuracion['DB_NAME']
)

# Creamos el gestor de conexiones usando la dirección que hemos preparado.
# Limitamos a 5 segundos la espera para establecer la conexión.
engine = create_engine(url, connect_args={'connect_timeout': 5})

# Carpeta donde guardamos los siete CSV limpios.
ruta_datos = raiz_proyecto / 'data' / 'processed'

# Cada elemento contiene:
# nombre de la tabla, nombre del CSV y columnas que debemos leer como fechas.
# Usuarios y productos van primero porque otras tablas dependen de ellos.
tablas = [
    ('usuarios', 'usuarios_limpio.csv', ['fecha_instalacion']),
    ('productos_iap', 'productos_iap_limpio.csv', []),
    ('sesiones', 'sesiones_limpio.csv', ['fecha']),
    ('partidas', 'partidas_limpio.csv', ['fecha']),
    ('compras', 'compras_limpio.csv', ['fecha']),
    ('ingresos_ads', 'ingresos_ads_limpio.csv', ['fecha']),
    ('gasto_ua', 'gasto_ua_limpio.csv', ['fecha'])
]

# Ejecutamos la carga dentro de una transacción:
# si alguna tabla falla, se deshacen las inserciones de este bloque.
with engine.begin() as conexion:
    for nombre_tabla, nombre_csv, columnas_fecha in tablas:
        # Construimos la ruta al CSV de esta vuelta.
        ruta_csv = ruta_datos / nombre_csv

        # Leemos el archivo y convertimos las columnas de fecha indicadas.
        df = pd.read_csv(ruta_csv, parse_dates=columnas_fecha)

        # Comprobamos si la tabla ya contiene datos.
        # El nombre procede de nuestra lista fija de tablas.
        filas_actuales = conexion.execute(
            text(f'SELECT COUNT(*) FROM public.{nombre_tabla}')
        ).scalar_one()

        if filas_actuales > 0:
            print(f'{nombre_tabla}: ya contiene datos; se omite.')
            continue

        # Añadimos los datos conservando la estructura y las claves de la tabla.
        df.to_sql(
            nombre_tabla,
            conexion,
            schema='public',
            if_exists='append',
            index=False
        )

        print(f'{nombre_tabla}: {len(df)} filas insertadas, pendientes de confirmar.')

# Al salir del with sin errores, PostgreSQL confirma los cambios.
print('Carga finalizada y cambios guardados.')