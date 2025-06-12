# Web routes for project CRUD (for rendering in sidebar, etc.)

from quart import Blueprint, render_template
from shared.database_service import get_db
from projects.services.project_service import ProjectService

routes = Blueprint('projects_routes', __name__)

@routes.route('/projects')
async def projects_list():
    async for db in get_db():
        projects = await ProjectService.get_projects(db)
        return await render_template('projects_list.html', projects=projects)
