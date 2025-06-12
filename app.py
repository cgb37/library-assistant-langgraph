from quart import Quart, render_template, request, jsonify, g
from main import get_library_assistant_response
from projects.api.routes import api as projects_api
from projects.routes.routes import routes as projects_routes
from chats.api.routes import api as chats_api
from chats.routes.routes import chats_routes
from chats.services.chat_service import ChatService
from shared.database_service import close_database, get_database

app = Quart(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

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

@app.context_processor
async def inject_recent_chats():
    # Provide last 10 chats to all templates
    database = await get_database()
    chat_service = ChatService(database)
    recent_chats = await chat_service.get_chats(limit=10)
    return dict(recent_chats=recent_chats)

app.register_blueprint(projects_api)
app.register_blueprint(projects_routes)
app.register_blueprint(chats_api)
app.register_blueprint(chats_routes)

if __name__ == "__main__":
    app.run()
