CREATE TABLE properties_tbl (
  id SERIAL PRIMARY KEY,
  users_tbl_id INTEGER REFERENCES users_tbl (id),
  _text TEXT,
  userID VARCHAR(32),
  userName VARCHAR(32),
  _timestamp TIMESTAMP NOT NULL,
  source VARCHAR(32),
  sentiStrings TEXT,
  labelledSentiment VARCHAR(32),
  crowder VARCHAR(32)
);