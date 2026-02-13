-- Table initialization for demo_206 grid app (run after database exists).
-- Matches misc/schema_design.sql: grid_table with RID + columns A-X (24 grid columns), 24 rows = 24 grid rows.
-- Use: psql -h <DB_HOST> -p <DB_PORT> -U <DB_USERNAME> -d <DB_DATABASE> -f init_tables.sql
-- Or run init_once.sh, which creates the table via Django migrate.

CREATE TABLE IF NOT EXISTS grid_table (
    "RID" SERIAL PRIMARY KEY,
    "A" CHAR(6),
    "B" CHAR(6),
    "C" CHAR(6),
    "D" CHAR(6),
    "E" CHAR(6),
    "F" CHAR(6),
    "G" CHAR(6),
    "H" CHAR(6),
    "I" CHAR(6),
    "J" CHAR(6),
    "K" CHAR(6),
    "L" CHAR(6),
    "M" CHAR(6),
    "N" CHAR(6),
    "O" CHAR(6),
    "P" CHAR(6),
    "Q" CHAR(6),
    "R" CHAR(6),
    "S" CHAR(6),
    "T" CHAR(6),
    "U" CHAR(6),
    "V" CHAR(6),
    "W" CHAR(6),
    "X" CHAR(6)
);
