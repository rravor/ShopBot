CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100)
);

CREATE INDEX category_index ON category (title);

CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100)
);

CREATE INDEX brand_index ON brand (title);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_uuid UUID NOT NULL DEFAULT public.uuid_generate_v4(),
    title VARCHAR(100),
    price INT,
    category INT,
    FOREIGN KEY (category) REFERENCES category (id) ON DELETE CASCADE,
    brand INT,
    FOREIGN KEY (brand) REFERENCES brand (id) ON DELETE CASCADE
);

CREATE INDEX product_index ON product (product_id);

CREATE TABLE shop_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(100),
    phone_number VARCHAR(100),
    email VARCHAR(100),
    address VARCHAR(100)
);