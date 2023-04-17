CREATE TABLE IF NOT EXISTS 'registrants' ('id' INTEGER PRIMARY KEY, 'email' TEXT NOT NULL UNIQUE , 'username' TEXT NOT NULL UNIQUE, 'hash' TEXT NOT NULL, 'wallet' NUMERIC NOT NULL DEFAULT 1000.00, 'timestamp' DEFAULT CURRENT_TIMESTAMP);