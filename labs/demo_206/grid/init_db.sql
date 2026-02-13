-- Database initialization for demo_206 (run once).
-- Creates the database only. For table creation see init_tables.sql, or run init_once.sh (uses Django migrate).
-- Use: psql -h <DB_HOST> -p <DB_PORT> -U <DB_USERNAME> -d postgres -f init_db.sql
-- (PostgreSQL has no IF NOT EXISTS for CREATE DATABASE; init_once.sh creates it only if missing.)

CREATE DATABASE grid_db ENCODING 'UTF8';
