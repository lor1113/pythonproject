DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS tags;

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  colour VARCHAR(255),
  deactivated BOOLEAN
);

CREATE TABLE merchants (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  colour VARCHAR(255),
  tags INT[],
  deactivated BOOLEAN
);

CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  name TEXT,
  amount INT,
  timestamp TIMESTAMP,
  tags INT[],
  merchant int,
  deactivated BOOLEAN,
  CONSTRAINT fk_merchant
    FOREIGN KEY(merchant)
      REFERENCES merchants(id)
      ON DELETE CASCADE
);