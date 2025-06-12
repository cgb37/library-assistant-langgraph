# Web routes for project CRUD (for rendering in sidebar, etc.)

from quart import Blueprint, render_template, redirect
from shared.database_service import get_database
from projects.services.project_service import ProjectService

routes = Blueprint('projects_routes', __name__)

@routes.route('/projects')
async def projects_list():
    database = await get_database()
    project_service = ProjectService(database)
    projects = await project_service.get_projects()
    return await render_template('projects/list.html', projects=projects)

@routes.route('/projects/create')
async def project_create():
    return await render_template('projects/create.html')

@routes.route('/projects/edit/<project_id>')
async def project_edit(project_id):
    database = await get_database()
    project_service = ProjectService(database)
    project = await project_service.get_project(project_id)
    return await render_template('projects/edit.html', project=project)
