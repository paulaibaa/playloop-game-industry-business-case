-- PlayLoop: estructura de las siete tablas del proyecto.
-- Ejecutar conectado a la base de datos playloop, en un esquema sin estas tablas.
-- Este archivo crea las tablas; no crea la base de datos ni carga los CSV.
-- Las tablas se ordenan para crear primero las referenciadas por claves foráneas.
-- Si las tablas ya existen, no es necesario volver a ejecutar este archivo.

-- Usuarios: un registro por jugador.
CREATE TABLE usuarios (
    user_id INTEGER PRIMARY KEY,
    fecha_instalacion DATE,
    canal_adquisicion TEXT,
    pais TEXT,
    plataforma TEXT,
    -- La versión es texto (por ejemplo, 3.0.1) y puede ser desconocida.
    version_app TEXT
);

-- Sesiones: cada evento pertenece a un usuario existente.
CREATE TABLE sesiones (
    evento_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    fecha DATE,
    duracion_segundos INTEGER,
    plataforma TEXT,
    CONSTRAINT fk_sesiones_usuario
        FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
);

-- Partidas: conservamos los valores ausentes de movimientos y boosters.
CREATE TABLE partidas (
    partida_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nivel INTEGER,
    fecha DATE,
    -- 0 = derrota; 1 = victoria.
    resultado INTEGER CHECK (resultado IN (0, 1)),
    movimientos INTEGER,
    boosters_usados INTEGER,
    CONSTRAINT fk_partidas_usuario
        FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
);

-- Catálogo: debe existir antes de crear y cargar compras.
CREATE TABLE productos_iap (
    producto_id INTEGER PRIMARY KEY,
    nombre TEXT,
    tipo TEXT,
    -- NUMERIC conserva decimales exactos para los importes monetarios.
    precio_base NUMERIC(10, 2),
    -- NULL cuando la cantidad de monedas no aplica al producto.
    monedas INTEGER
);

-- Compras: cada operación referencia un usuario y un producto existentes.
CREATE TABLE compras (
    compra_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    fecha DATE,
    importe NUMERIC(10, 2),
    moneda TEXT,
    plataforma TEXT,
    -- El CSV limpio contiene solo ventas en EUR con reembolso = 0.
    reembolso INTEGER CHECK (reembolso IN (0, 1)),
    CONSTRAINT fk_compras_usuario
        FOREIGN KEY (user_id) REFERENCES usuarios(user_id),
    CONSTRAINT fk_compras_producto
        FOREIGN KEY (producto_id) REFERENCES productos_iap(producto_id)
);

-- Publicidad: cuatro decimales para conservar ingresos pequeños.
CREATE TABLE ingresos_ads (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    fecha DATE,
    tipo_ad TEXT,
    red_ad TEXT,
    -- Se admiten NULL para los ingresos desconocidos.
    ingreso NUMERIC(12, 4),
    CONSTRAINT fk_ingresos_ads_usuario
        FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
);

-- Adquisición: datos agregados por canal y fecha, sin relación por usuario.
CREATE TABLE gasto_ua (
    -- No existe en el CSV: omitir esta columna al cargar los datos.
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    canal TEXT,
    fecha DATE,
    gasto NUMERIC(12, 2),
    instalaciones INTEGER,
    impresiones INTEGER,
    -- Se admiten NULL para los clics desconocidos.
    clics INTEGER
);

-- gasto_ua conserva su ID generado. Tras corregir las fechas, no hay
-- combinaciones canal-fecha repetidas. Los gastos elevados siguen pendientes de validación.
