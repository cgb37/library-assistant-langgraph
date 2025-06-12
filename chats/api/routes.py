# API routes for chat CRUD (JSON endpoints)

from quart import Blueprint, request, jsonify
from shared.database_service import get_database
from chats.services.chat_service import ChatService
from chats.models.chat import ChatCreate

api = Blueprint('chats_api', __name__, url_prefix='/api/chats')

@api.route('/', methods=['GET'])
async def list_chats():
    database = await get_database()
    chat_service = ChatService(database)
    chats = await chat_service.get_chats()
    return jsonify([{
        'id': str(chat.id), 
        'user_query': chat.user_query, 
        'ai_response': chat.ai_response,
        'model_used': chat.model_used,
        'support_level': chat.support_level,
        'routing_reason': chat.routing_reason,
        'created_at': chat.created_at.isoformat()
    } for chat in chats])

@api.route('/', methods=['POST'])
async def create_chat():
    data = await request.get_json()
    user_query = data.get('user_query')
    ai_response = data.get('ai_response')
    model_used = data.get('model_used', 'llama3.3')
    support_level = data.get('support_level')
    routing_reason = data.get('routing_reason')
    
    if not user_query or not ai_response:
        return jsonify({'error': 'user_query and ai_response are required'}), 400
    
    database = await get_database()
    chat_service = ChatService(database)
    chat_data = ChatCreate(
        user_query=user_query, 
        ai_response=ai_response,
        model_used=model_used,
        support_level=support_level,
        routing_reason=routing_reason
    )
    chat = await chat_service.create_chat(chat_data)
    return jsonify({
        'id': str(chat.id), 
        'user_query': chat.user_query, 
        'ai_response': chat.ai_response,
        'model_used': chat.model_used,
        'support_level': chat.support_level,
        'routing_reason': chat.routing_reason,
        'created_at': chat.created_at.isoformat()
    }), 201

@api.route('/<chat_id>', methods=['DELETE'])
async def delete_chat(chat_id):
    database = await get_database()
    chat_service = ChatService(database)
    success = await chat_service.delete_chat(chat_id)
    if not success:
        return jsonify({'error': 'Chat not found'}), 404
    return jsonify({'result': 'success'})
