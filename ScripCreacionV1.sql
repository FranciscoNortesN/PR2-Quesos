-- Nombre: Script Creacion.sql
-- Script Creacion.sql para PostgreSQL V0.1 Proyecto Queso
-- VICENTE BURDEUS SANCHEZ
-- Fecha: 2023-10-05
-- HORA : 17:08

-- Almacenes --------------------------------------------------------------

CREATE TABLE IF NOT EXISTS almacen (
    "id_almacen" char(10) PRIMARY KEY,
    "nombre" char(50) NOT NULL,
    "capacidad" integer NOT NULL CHECK ("capacidad" >= 0),
    "ultima_revision" date
);

CREATE TABLE IF NOT EXISTS estanteria (
    "id_estanteria" char(10) PRIMARY KEY,
    "localizacion" char(10) NOT NULL,
    "tipo_queso" char(10) NOT NULL,
    "fecha_inicio" date NOT NULL, -- solo el día de instalación
    "id_almacen" char(10),
    CONSTRAINT id_almacen_estanteria_fk FOREIGN KEY ("id_almacen") REFERENCES almacen 
    ON DELETE CASCADE ON UPDATE CASCADE    
);

-- Nodos de temperatura y humedad -----------------------------------------------

CREATE TABLE IF NOT EXISTS nodotemperaturainfo (
    "id_nodo" char(10) PRIMARY KEY,
    "localizacion" char(10) NOT NULL,
    "ultima_revision" date NOT NULL,
    "id_almacen" char(10),
    CONSTRAINT id_almacen_nti_fk FOREIGN KEY ("id_almacen") REFERENCES almacen
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS ntdato (
    "id_nodo" char(10) NOT NULL,
    "temperatura" real NOT NULL,
    "humedad" integer NOT NULL,
    "bateria" integer,
    "fecha" timestamp NOT NULL DEFAULT NOW(),
    CONSTRAINT id_nodo_ntdato_fk FOREIGN KEY ("id_nodo") REFERENCES nodotemperaturainfo
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- Info de los quesos ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS queso (
    "id_queso" char(10) PRIMARY KEY,
    "localizacion" char(10) NOT NULL,
    "peso" real NOT NULL CHECK ("peso" >= 0),
    "fecha_produccion" date NOT NULL,
    "estado" char(10) NOT NULL,
    CONSTRAINT id_estanteria_queso_fk FOREIGN KEY ("localizacion") REFERENCES estanteria
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS lote (
    "id_lote" char(10) PRIMARY KEY,
    "nombre" char(50) NOT NULL,
    "fecha_inicio" date NOT NULL,
    "fecha_fin" date NOT NULL,
    "estado" integer NOT NULL CHECK ("estado" >= 0),
    "cantidad" integer NOT NULL CHECK ("cantidad" >= 0),
    "tipo_queso" char(10) NOT NULL,
    "tipo_leche" char(10) NOT NULL,
    CONSTRAINT id_queso_lote_fk FOREIGN KEY ("tipo_queso") REFERENCES queso
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- Clientes ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cliente (
    "id_cliente" char(10) PRIMARY KEY,
    "nombre" char(50) NOT NULL,
    "tipo_cliente" char(10) NOT NULL,
    "informacion_contacto" char(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    "id_identificador" char(10) PRIMARY KEY,
    "cliente" char(10) NOT NULL,
    "fecha_pedido" date NOT NULL,
    "fecha_entrega" date NOT NULL,
    "estado_pedido" char(10) NOT NULL,
    "monto_total" real NOT NULL CHECK ("monto_total" >= 0),
    CONSTRAINT id_cliente_pedido_fk FOREIGN KEY ("cliente") REFERENCES cliente
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS pedidostatus (
    "id_pedido" char(10) NOT NULL,
    "estado_pedido" char(10) NOT NULL,
    "fecha" timestamp NOT NULL DEFAULT NOW(),
    CONSTRAINT id_pedido_pedidostatus_fk FOREIGN KEY ("id_pedido") REFERENCES pedido
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS pedidoinfo (
    "id_detalle" char(10) PRIMARY KEY,
    "id_pedido" char(10) NOT NULL,
    "id_queso" char(10) NOT NULL,
    "cantidad" real NOT NULL CHECK ("cantidad" >= 0),
    "precio_unitario" real NOT NULL CHECK ("precio_unitario" >= 0),
    "subtotal" real NOT NULL CHECK ("subtotal" >= 0),
    CONSTRAINT id_pedido_pedidoinfo_fk FOREIGN KEY ("id_pedido") REFERENCES pedido
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT id_queso_pedidoinfo_fk FOREIGN KEY ("id_queso") REFERENCES queso
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- Proveedores ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS proveedor (
    "id_proveedor" char(10) PRIMARY KEY,
    "nombre" char(50) NOT NULL,
    "tipo_insumo" char(10) NOT NULL,
    "correo" char(50) NOT NULL,
    "telefono" char(15) NOT NULL
);

-- AGVs ------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS robotagvinfo (
    "id_robot" char(10) PRIMARY KEY,
    "estado" char(10) NOT NULL,
    "carga" integer
);

CREATE TABLE IF NOT EXISTS rutas (
    "id_robot" char(10) NOT NULL,
    "inicio" char(10) NOT NULL,
    "destino" char(10) NOT NULL,
    "fecha" timestamp NOT NULL DEFAULT NOW(),
    CONSTRAINT id_robot_rutas_fk FOREIGN KEY ("id_robot") REFERENCES robotagvinfo
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT inicio_rutas_fk FOREIGN KEY ("inicio") REFERENCES estanteria
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT destino_rutas_fk FOREIGN KEY ("destino") REFERENCES estanteria
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- Usuarios ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS userinfo (
    "id_usuario" char(10) PRIMARY KEY,
    "nombre" char(25) NOT NULL,
    "apellido" char(50) NOT NULL,
    "tipo_usuario" char(15) NOT NULL CHECK ("tipo_usuario" IN ('admin', 'operador', 'mantenimiento', 'supervisor')),
    "correo" char(50) NOT NULL,
    "telefono" char(15) NOT NULL,
    "contrasena" char(50) NOT NULL,
    "dataid" char(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS userlogin (
    "id_usuario" char(10) NOT NULL,
    "fecha_login" timestamp NOT NULL DEFAULT NOW(),
    "ip" char(15) NOT NULL,
    CONSTRAINT id_usuario_userslogin_fk FOREIGN KEY ("id_usuario") REFERENCES userinfo
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- Preguntas-Web -------------------------------------------------------------

CREATE SEQUENCE formulario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS formularios (
    "id_formularuio" integer PRIMARY KEY DEFAULT nextval('formulario_seq'),
    "nombre" char(50),
    "correo" char(50) NOT NULL,
    "mensaje" char(500) NOT NULL,
    "fecha" timestamp NOT NULL DEFAULT NOW()
);

--Datos MQTT -------------------------------------------------------------


CREATE SEQUENCE topic_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS mqtt_topics (
    "id_topic" integer PRIMARY KEY DEFAULT nextval('topic_seq'),
    "topic" char(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS mqtt_datos (
    "id_dato" integer NOT NULL,
    "fecha" timestamp NOT NULL DEFAULT NOW(),
    "payload" char(500) NOT NULL,
    CONSTRAINT id_topic_mqtt_datos_fk FOREIGN KEY ("id_topic") REFERENCES mqtt_topics
    ON DELETE CASCADE ON UPDATE CASCADE
);
