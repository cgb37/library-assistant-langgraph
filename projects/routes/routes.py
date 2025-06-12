# Web routes for project CRUD (for rendering in sidebar, etc.)

from quart import Blueprint, render_template
from shared.database_service import get_database
from projects.services.project_service import ProjectService

routes = Blueprint('projects_routes', __name__)

@routes.route('/projects')
async def projects_list():
    database = await get_database()
    project_service = ProjectService(database)
    projects = await project_service.get_projects()
    return await render_template('projects_list.html', projects=projects)
