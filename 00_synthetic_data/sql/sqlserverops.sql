CREATE TABLE SCHEMA_NAME.historical_orders (
    order_id VARCHAR(256) PRIMARY KEY,
    order_timestamp DATETIME2,
    restaurant_id VARCHAR(256),
    customer_id VARCHAR(256),
    order_type VARCHAR(256),  -- dine_in, takeaway, delivery
    items VARCHAR(MAX),  -- JSON array as string
    total_amount DECIMAL,
    payment_method VARCHAR(256),
    order_status VARCHAR(256)
);

CREATE TABLE SCHEMA_NAME.reviews (
    review_id VARCHAR(256) PRIMARY KEY,
    order_id VARCHAR(256),
    customer_id VARCHAR(256),
    restaurant_id VARCHAR(256),
    review_text VARCHAR(MAX),
    rating INT,
    review_timestamp DATETIME2
);

CREATE TABLE SCHEMA_NAME.customers (
    customer_id VARCHAR(256) PRIMARY KEY,
    name VARCHAR(256),
    email VARCHAR(256),
    phone VARCHAR(256),
    city VARCHAR(256),
    join_date DATE,
);

CREATE TABLE SCHEMA_NAME.menu_items (
    restaurant_id VARCHAR(256),
    item_id VARCHAR(256),
    name VARCHAR(256),
    category VARCHAR(256),
    price DECIMAL(10,2),
    ingredients VARCHAR(256),
    is_vegetarian BIT,
    spice_level VARCHAR(256),  -- None, Mild, Medium, Hot
    PRIMARY KEY (restaurant_id, item_id)
);

CREATE TABLE SCHEMA_NAME.restaurants (
    restaurant_id VARCHAR(256) PRIMARY KEY,
    name VARCHAR(256),
    city VARCHAR(256),
    country VARCHAR(256),
    address VARCHAR(MAX),
    opening_date DATE,
    phone VARCHAR(256)
);