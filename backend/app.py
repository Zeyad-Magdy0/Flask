from flask import Flask, jsonify, request
from config import Config
from db import get_db_connection
from cache import get_redis_client
import json


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/health", methods=["GET"])
    def health():
        
        """
        Return a JSON containing the status of the application.
        The status is always "ok".
        """
        return jsonify({"status": "ok"}), 200
    
    @app.route("/items/<int:item_id>", methods=["GET"])
    def get_item(item_id):
        
        cache_key = f"item:{item_id}"
        redis_client = get_redis_client(app)
        cached_item = redis_client.get(cache_key)
    
        if cached_item:
            return jsonify(json.loads(cached_item)), 200
        
        conn = get_db_connection(app)
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, name, description FROM items WHERE id = %s;", (item_id,)
        )

        row = cur.fetchone()

        cur.close()
        conn.close()
        
        if row is None:
            return jsonify({"error": "Item not found"}), 404
        
        item = {
            "id": row[0],
            "name": row[1],
            "description": row[2]
        }
        
        redis_client.set(cache_key, json.dumps(item), ex= 60)

        return jsonify(item), 200

    @app.route("/items", methods=["POST"])
    def create_item():
        data = request.get_json()
        
        if not data or "name" not in data:
            return jsonify({"error": "Name is required"}), 400
        
        name = data["name"]
        description = data.get("description", "")
        
        conn = get_db_connection(app)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;",
            (name, description)
        )

        item_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()
              
        item = {
            "id": item_id,
            "name": name,
            "description": description
        }
        
        return jsonify(item), 201
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)