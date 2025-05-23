CREATE TABLE IF NOT EXISTS preguntas (
    id_pregunta INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pregunta TEXT NOT NULL,
    tipo_pregunta TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS preguntas_res (
    id_res INTEGER PRIMARY KEY,
    respuesta1 TEXT NOT NULL,
    R1_value INTEGER NOT NULL,
    respuesta2 TEXT NOT NULL,
    R2_value INTEGER NOT NULL,
    respuesta3 TEXT NOT NULL,
    R3_value INTEGER NOT NULL,
    respuesta4 TEXT NOT NULL,
    R4_value INTEGER NOT NULL,
    respuesta5 TEXT NOT NULL,
    R5_value INTEGER NOT NULL,
    FOREIGN KEY (id_res) REFERENCES preguntas(id_pregunta)
);

CREATE TABLE IF NOT EXISTS preguntas_sli (
    id_sli INTEGER PRIMARY KEY,
    multiplier REAL NOT NULL,
    smallest TEXT NOT NULL,
    largest TEXT NOT NULL,
    FOREIGN KEY (id_sli) REFERENCES preguntas(id_pregunta)
);

CREATE TABLE IF NOT EXISTS preguntas_num (
    id_num INTEGER PRIMARY KEY,
    min REAL NOT NULL,
    max REAL NOT NULL,
    step REAL NOT NULL,
    multiplier REAL NOT NULL,
    FOREIGN KEY (id_num) REFERENCES preguntas(id_pregunta)
);

CREATE TABLE IF NOT EXISTS respuestas (
    id_pregunta INTEGER NOT NULL,
    respuesta TEXT NOT NULL,
    FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
);


