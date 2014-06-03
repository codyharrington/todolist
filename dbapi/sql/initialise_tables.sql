CREATE TABLE IF NOT EXISTS "user" (
  id SERIAL PRIMARY KEY,
  username VARCHAR(10) NOT NULL UNIQUE,
  email VARCHAR(20) UNIQUE,
  password VARCHAR(100),
  salt VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS task (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  points INT,
  start TIMESTAMP,
  "end" TIMESTAMP,
  "desc" VARCHAR(1000),
  "enabled" BOOLEAN,
  "userid" INT REFERENCES "user"(id)
);