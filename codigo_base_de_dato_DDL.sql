
CREATE TABLE habitacion (
    habitacion_id     NUMBER(9) NOT NULL,
    disponibilidad    CHAR(1) NOT NULL,
    numero_habitacion NUMBER(4) NOT NULL,
    tipo              VARCHAR2(15) NOT NULL,
    capacidad         NUMBER(2) NOT NULL,
    precio            NUMBER(9) NOT NULL,
    hotel_hotel_id    NUMBER(9) NOT NULL
);

CREATE UNIQUE INDEX habitacion__idx ON
    habitacion (
        hotel_hotel_id
    ASC );

ALTER TABLE habitacion ADD CONSTRAINT habitacion_pk PRIMARY KEY ( habitacion_id );

CREATE TABLE hotel (
    hotel_id  NUMBER(9) NOT NULL,
    nombre    VARCHAR2(25) NOT NULL,
    direccion VARCHAR2(100) NOT NULL
);

ALTER TABLE hotel ADD CONSTRAINT hotel_pk PRIMARY KEY ( hotel_id );

CREATE TABLE metodo_pago (
    pago_id     NUMBER(9) NOT NULL,
    descripcion VARCHAR2(25) NOT NULL,
    fecha_pago  DATE NOT NULL
);

ALTER TABLE metodo_pago ADD CONSTRAINT metodo_pago_pk PRIMARY KEY ( pago_id );

CREATE TABLE reserva (
    reserva_id               NUMBER(10) NOT NULL,
    fecha_entrada            DATE NOT NULL,
    fecha_salida             DATE NOT NULL,
    cantidad_personas        NUMBER(2) NOT NULL,
    precio_final             NUMBER(9) NOT NULL,
    usuario_usuario_id       NUMBER(10) NOT NULL,
    metodo_pago_pago_id      NUMBER(9) NOT NULL,
    habitacion_habitacion_id NUMBER(9) NOT NULL
);

CREATE UNIQUE INDEX reserva__idx ON
    reserva (
        habitacion_habitacion_id
    ASC );

ALTER TABLE reserva ADD CONSTRAINT reserva_pk PRIMARY KEY ( reserva_id );

CREATE TABLE usuario (
    usuario_id NUMBER(10) NOT NULL,
    username   VARCHAR2(25) NOT NULL,
    password   VARCHAR2(25) NOT NULL,
    nombre     VARCHAR2(25) NOT NULL,
    apellido   VARCHAR2(25) NOT NULL,
    correo     VARCHAR2(50) NOT NULL,
    telefono   NUMBER(9) NOT NULL,
    user_type  VARCHAR2(25) NOT NULL
);

ALTER TABLE usuario ADD CONSTRAINT usuario_pk PRIMARY KEY ( usuario_id );

ALTER TABLE habitacion
    ADD CONSTRAINT habitacion_hotel_fk FOREIGN KEY ( hotel_hotel_id )
        REFERENCES hotel ( hotel_id );

ALTER TABLE reserva
    ADD CONSTRAINT reserva_habitacion_fk FOREIGN KEY ( habitacion_habitacion_id )
        REFERENCES habitacion ( habitacion_id );

ALTER TABLE reserva
    ADD CONSTRAINT reserva_metodo_pago_fk FOREIGN KEY ( metodo_pago_pago_id )
        REFERENCES metodo_pago ( pago_id );

ALTER TABLE reserva
    ADD CONSTRAINT reserva_usuario_fk FOREIGN KEY ( usuario_usuario_id )
        REFERENCES usuario ( usuario_id );
