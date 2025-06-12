from quart import Quart, render_template, request, jsonify
from main import get_library_assistant_response
from projects.api.routes import api as projects_api
from projects.routes.routes import routes as projects_routes
from shared.database_service import close_database

app = Quart(__name__)

@app.after_serving
async def close_db():
    """Close database connection after app shutdown"""
    await close_database()

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/chat", methods=["POST"])
async def chat():
    data = await request.get_json()
    user_query = data.get("prompt", "")
    if not user_query:
        return jsonify({"error": "No prompt provided."}), 400
    try:
        result = get_library_assistant_response(user_query)
        return jsonify({
            "response": result["response"],
            "support_level": result["support_level"],
            "routing_reason": result["routing_reason"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.register_blueprint(projects_api)
app.register_blueprint(projects_routes)

if __name__ == "__main__":
    app.run()
