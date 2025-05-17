-- Borrar datos primero (respetando integridad referencial)
DELETE FROM estanteria;
DELETE FROM almacen;

-- Insertar almacenes
INSERT INTO almacen (id_almacen, nombre, capacidad, ultima_revision) VALUES
('1', 'almacen 1', 144, NOW()),
('2', 'almacen 2', 144, NOW()),
('3', 'almacen 3', 144, NOW());

-- Insertar estanterías
DO $$
DECLARE
    alm_id CHAR(10);
    f INT;
    c INT;
    l CHAR(1);
    est_id INT := 1;
    lados TEXT[] := ARRAY['A', 'B'];
BEGIN
    FOR alm_id IN SELECT id_almacen FROM almacen LOOP
        FOR f IN 1..2 LOOP
            FOR c IN 0..3 LOOP
                FOREACH l IN ARRAY lados LOOP
                    INSERT INTO estanteria (
                        id_estanteria, fila, columna, lado, tipo_queso, status,
                        fecha_inicio, id_almacen, ref_queso
                    ) VALUES (
                        LPAD(est_id::text, 4, '0'), f, c, l, NULL, 'vacia',
                        NOW(), alm_id, NULL
                    );
                    est_id := est_id + 1;
                END LOOP;
            END LOOP;
        END LOOP;
    END LOOP;
END $$;
