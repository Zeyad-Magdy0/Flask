import psycopg2


def get_db_connection(app):
    return psycopg2.connect(
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        dbname=app.config["DB_NAME"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        )


CREATE_ITEMS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
