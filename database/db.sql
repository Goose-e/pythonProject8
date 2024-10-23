CREATE IF NOT EXISTS hackaton_admin WITH PASSWORD 'ваш_пароль';
ALTER USER hackaton_admin CREATEDB;



CREATE DATABASE IF NOT EXISTS "Hackaton"
    WITH
    OWNER = hackaton_admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


\c Hackaton;  -- Connect to the Hackaton database

CREATE TABLE IF NOT EXISTS user_info (
    user_info_id BIGINT NOT NULL PRIMARY KEY,
    user_id      BIGINT NOT NULL,
    secret_info  VARCHAR
);

ALTER TABLE user_info
    OWNER TO hackaton_admin;

GRANT DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON user_info TO hackaton_admin;

CREATE TABLE IF NOT EXISTS admin (
    admin_id       BIGINT NOT NULL PRIMARY KEY,
    admin_login    VARCHAR(20) NOT NULL UNIQUE,
    admin_password VARCHAR(255) NOT NULL  -- Specify length for password
);

ALTER TABLE admin
    OWNER TO hackaton_admin;
GRANT ALL PRIVILEGES ON DATABASE Hackaton TO hackaton_admin;