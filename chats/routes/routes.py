# Web routes for chat history (for rendering chat history page)

from quart import Blueprint, render_template
from shared.database_service import get_database
from chats.services.chat_service import ChatService

chats_routes = Blueprint('chats_routes', __name__)

@chats_routes.route('/chats')
async def chats_list():
    database = await get_database()
    chat_service = ChatService(database)
    chats = await chat_service.get_chats()
    return await render_template('chats_list.html', chats=chats)
