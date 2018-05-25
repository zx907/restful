CREATE TABLE coordinate_tbl (
  id SERIAL PRIMARY KEY,
  users_tbl_id INTEGER REFERENCES users_tbl (id),
  coordinate POINT
);