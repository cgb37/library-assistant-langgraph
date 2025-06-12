from quart import Quart, render_template, request, jsonify
from main import get_library_assistant_response

app = Quart(__name__)

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

if __name__ == "__main__":
    app.run()
