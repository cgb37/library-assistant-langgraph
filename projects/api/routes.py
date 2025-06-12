# API routes for project CRUD (JSON endpoints)

from quart import Blueprint, request, jsonify
from shared.database_service import get_db
from projects.services.project_service import ProjectService

api = Blueprint('projects_api', __name__, url_prefix='/api/projects')

@api.route('/', methods=['GET'])
async def list_projects():
    async for db in get_db():
        projects = await ProjectService.get_projects(db)
        return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in projects])

@api.route('/', methods=['POST'])
async def create_project():
    data = await request.get_json()
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    async for db in get_db():
        project = await ProjectService.create_project(db, name, description)
        return jsonify({'id': project.id, 'name': project.name, 'description': project.description}), 201

@api.route('/<int:project_id>', methods=['PUT'])
async def update_project(project_id):
    data = await request.get_json()
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    async for db in get_db():
        project = await ProjectService.update_project(db, project_id, name, description)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify({'id': project.id, 'name': project.name, 'description': project.description})

@api.route('/<int:project_id>', methods=['DELETE'])
async def delete_project(project_id):
    async for db in get_db():
        project = await ProjectService.delete_project(db, project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify({'result': 'success'})
