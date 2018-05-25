CREATE TABLE users_tbl (
  id SERIAL PRIMARY KEY,
  _id VARCHAR(32) NOT NULL
);

CREATE TABLE properties_tbl (
--   id SERIAL PRIMARY KEY,
  users_tbl_id INTEGER REFERENCES users_tbl (id) ON DELETE CASCADE,
  _text TEXT,
  userID VARCHAR(32),
  userName VARCHAR(32),
  _timestamp TIMESTAMP NOT NULL,
  source VARCHAR(32),
  sentiStrings TEXT,
  labelledSentiment VARCHAR(32),
  crowder VARCHAR(32)
);

CREATE TABLE coordinate_tbl (
--   id SERIAL PRIMARY KEY,
  users_tbl_id INTEGER REFERENCES users_tbl (id) ON DELETE CASCADE,
  coordinate POINT
);

CREATE TABLE sessions_tbl (
  token text,
  users_tbl_id INTEGER REFERENCES users_tbl(id) ON DELETE CASCADE
);