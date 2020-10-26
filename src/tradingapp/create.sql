CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    company TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_price (
    id INTEGER PRIMARY KEY,
    stock_id INTEGER,
    date NOT NULL,
    open NOT NULL,
    high NOT NULL,
    low NOT NULL,
    close NOT NULL,
    adjusted_close NOT NULL,
    volume NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock (id)
);

-- INSERT
INSERT INTO stock (symbol, company) VALUES ('AAPL', 'Apple');
INSERT INTO stock (symbol, company) VALUES ('MSFT', 'Microsoft');
INSERT INTO stock (symbol, company) VALUES ('TSLA', 'Tesla');
INSERT INTO stock (symbol, company) VALUES ('AMD', 'Advanced Micro Devices');

-- UPDATE
 UPDATE stock SET company = 'Apple Inc.' WHERE id = 1;

 --DELETE
 DELETE FROM stock WHERE id = 3;