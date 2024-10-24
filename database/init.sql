-- Создание пользователя
CREATE ROLE hackaton_admin WITH LOGIN PASSWORD 'admin';
ALTER ROLE hackaton_admin CREATEDB;

-- Создание базы данных
CREATE DATABASE hackaton
    WITH
    OWNER = hackaton_admin  -- Установите владельцем пользователя hackaton_admin
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Установка привилегий
GRANT TEMPORARY, CONNECT ON DATABASE hackaton TO PUBLIC;
GRANT ALL ON DATABASE hackaton TO hackaton_admin;

-- Используем базу данных
\c hackaton;

-- Создание таблиц
CREATE TABLE IF NOT EXISTS public.admin_table
(
    admin_id serial NOT NULL,
    admin_login character varying(20) COLLATE pg_catalog."default" NOT NULL,
    admin_password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT admin_table_pkey PRIMARY KEY (admin_id),
    CONSTRAINT admin_table_admin_login_key UNIQUE (admin_login)
);

CREATE TABLE IF NOT EXISTS public.full_user
(
    user_id bigint NOT NULL,
    email character varying COLLATE pg_catalog."default",
    login character varying COLLATE pg_catalog."default",
    support_level character varying COLLATE pg_catalog."default",
    age integer,
    birthdate date,
    first_name character varying COLLATE pg_catalog."default",
    phone_number character varying COLLATE pg_catalog."default",
    second_name character varying COLLATE pg_catalog."default",
    gender character varying COLLATE pg_catalog."default",
    last_name character varying COLLATE pg_catalog."default",
    CONSTRAINT full_user_pkey PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public.regular
(
    regular_id serial NOT NULL,
    regular_expression character varying COLLATE pg_catalog."default" NOT NULL,
    expression_status integer NOT NULL,
    CONSTRAINT regular_pkey PRIMARY KEY (regular_id)
);

CREATE TABLE IF NOT EXISTS public.source
(
    source_id serial NOT NULL,
    source_adress character varying COLLATE pg_catalog."default" NOT NULL,
    source_status integer NOT NULL,
    CONSTRAINT source_pkey PRIMARY KEY (source_id)
);

CREATE TABLE IF NOT EXISTS public.user_info
(
    user_info_id serial NOT NULL,
    user_id bigint NOT NULL,
    secret_info character varying COLLATE pg_catalog."default",
    endpoint_place character varying COLLATE pg_catalog."default",
    message_time timestamp without time zone,
    CONSTRAINT user_info_pkey PRIMARY KEY (user_info_id)
);

-- Установка внешнего ключа
ALTER TABLE IF EXISTS public.user_info
    ADD CONSTRAINT user_info_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public.full_user (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

-- Установка владельцев таблиц
ALTER TABLE admin_table OWNER TO hackaton_admin;
ALTER TABLE regular OWNER TO hackaton_admin;
ALTER TABLE source OWNER TO hackaton_admin;
ALTER TABLE user_info OWNER TO hackaton_admin;
ALTER TABLE full_user OWNER TO hackaton_admin;

-- Предоставление всех привилегий
GRANT ALL PRIVILEGES ON TABLE admin_table TO hackaton_admin;
GRANT ALL PRIVILEGES ON TABLE regular TO hackaton_admin;
GRANT ALL PRIVILEGES ON TABLE source TO hackaton_admin;
GRANT ALL PRIVILEGES ON TABLE user_info TO hackaton_admin;
GRANT ALL PRIVILEGES ON TABLE full_user TO hackaton_admin;
