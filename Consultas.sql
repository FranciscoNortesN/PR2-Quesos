SELECT 
    p.id_pregunta,
    p.pregunta,
    p.tipo_pregunta,

    -- Datos tipo RES
    pr.respuesta1,
    pr.R1_value,
    pr.respuesta2,
    pr.R2_value,
    pr.respuesta3,
    pr.R3_value,
    pr.respuesta4,
    pr.R4_value,
    pr.respuesta5,
    pr.R5_value,

    -- Datos tipo SLI
    ps.smallest,
    ps.largest,
    ps.multiplier AS sli_multiplier,

    -- Datos tipo NUM
    pn.min,
    pn.max,
    pn.step,
    pn.multiplier AS num_multiplier

FROM preguntas p
LEFT JOIN preguntas_res pr ON pr.id_res = p.id_pregunta AND p.tipo_pregunta = 'res'
LEFT JOIN preguntas_sli ps ON ps.id_sli = p.id_pregunta AND p.tipo_pregunta = 'sli'
LEFT JOIN preguntas_num pn ON pn.id_num = p.id_pregunta AND p.tipo_pregunta = 'num'
WHERE p.id_pregunta = <ID_AQUI>;



-----------------------------------------------------------------------------------------------

INSERT INTO respuestas (id_pregunta, respuesta)
VALUES (1, 'Azul');



