-- PyroCast PostgreSQL + PostGIS initialization script
-- Executed automatically on first container startup.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Schema for geospatial simulation data (tables created in Phase 2+)
CREATE SCHEMA IF NOT EXISTS pyrocast;

COMMENT ON SCHEMA pyrocast IS 'PyroCast wildfire prediction platform schema';
