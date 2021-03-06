h1 = (
    """
CREATE TABLE IF NOT EXISTS PRODUCTS(
name VARCHAR(20) NOT NULL UNIQUE,
description VARCHAR(30) NOT NULL,
price INTEGER NOT NULL,
category VARCHAR(50) NOT NULL,
product_id VARCHAR PRIMARY KEY
)
""")

h3 = (
    """
CREATE TABLE IF NOT EXISTS SALES(
sale_id VARCHAR PRIMARY KEY NOT NULL,
user_id VARCHAR ,
user_email VARCHAR ,
cost INTEGER NOT NULL,
description VARCHAR NOT NULL,
FOREIGN KEY(user_id) REFERENCES users(id),
FOREIGN KEY(user_email) REFERENCES users(email)


)
""")

h2 = ("""
CREATE TABLE IF NOT EXISTS USERS(
id VARCHAR primary key,
email VARCHAR(20) NOT NULL UNIQUE,
password VARCHAR NOT NULL,
role VARCHAR(20) NOT NULL
)
""")


commands = [h1, h2, h3]
