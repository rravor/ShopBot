CREATE OR REPLACE FUNCTION SelectAllProducts()
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand = brand.id
JOIN category ON product.category = category.id;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION product_insert(
    title TEXT,
    price INTEGER,
    category INTEGER,
    brand INTEGER
)
RETURNS VOID
AS $$
INSERT INTO product (title, price, category, brand)
VALUES (title, price, brand, category);
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION GetTenProducts()
RETURNS TABLE (
    product_id INT,
    title TEXT,
    price INTEGER)
AS $$
    SELECT product_id, title, price
    FROM product
    ORDER BY product_id DESC
    LIMIT 10;
$$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION Delete_product(
    product_uuid UUID
)
RETURNS VOID
AS $$
DELETE FROM product WHERE product_uuid = Delete_product.product_uuid;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION UpdateProduct(
    title TEXT,
    price INTEGER,
    brand INTEGER,
    category INTEGER,
    product_uuid UUID
)
RETURNS VOID
AS $$
UPDATE product
SET
    title = UpdateProduct.title,
    price = UpdateProduct.price,
    brand = UpdateProduct.brand,
    category = UpdateProduct.category
WHERE product_uuid = UpdateProduct.product_uuid;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION SelectProductInfo(
    product_uuid UUID
)
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand = brand.id
JOIN category ON product.category = category.id
WHERE product_uuid = SelectProductInfo.product_uuid;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION SelectProductsByCategory(
    category_id INTEGER
)
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand = brand.id
JOIN category ON product.category = category.id
WHERE product.category = SelectProductsByCategory.category_id;
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION SelectProductsByBrand(
    brand_id INTEGER
)
RETURNS TABLE (
    product_uuid UUID,
    title TEXT,
    price NUMERIC,
    brand_title TEXT,
    category_title TEXT
)
AS $$
SELECT product.product_uuid, product.title, product.price, brand.title AS brand_title, category.title AS category_title
FROM product
JOIN brand ON product.brand = brand.id
JOIN category ON product.category = category.id
WHERE product.brand = SelectProductsByBrand.brand_id;
$$ LANGUAGE SQL;