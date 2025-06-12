# API routes for project CRUD (JSON endpoints)

from quart import Blueprint, request, jsonify
from shared.database_service import get_database
from projects.services.project_service import ProjectService
from projects.models.project import ProjectCreate, ProjectUpdate

api = Blueprint('projects_api', __name__, url_prefix='/api/projects')

@api.route('/', methods=['GET'])
async def list_projects():
    database = await get_database()
    project_service = ProjectService(database)
    projects = await project_service.get_projects()
    return jsonify([{'id': str(p.id), 'name': p.name, 'description': p.description} for p in projects])

@api.route('/', methods=['POST'])
async def create_project():
    data = await request.get_json()
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    database = await get_database()
    project_service = ProjectService(database)
    project_data = ProjectCreate(name=name, description=description)
    project = await project_service.create_project(project_data)
    return jsonify({'id': str(project.id), 'name': project.name, 'description': project.description}), 201

@api.route('/<project_id>', methods=['PUT'])
async def update_project(project_id):
    data = await request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    database = await get_database()
    project_service = ProjectService(database)
    project_data = ProjectUpdate(name=name, description=description)
    project = await project_service.update_project(project_id, project_data)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({'id': str(project.id), 'name': project.name, 'description': project.description})

@api.route('/<project_id>', methods=['DELETE'])
async def delete_project(project_id):
    database = await get_database()
    project_service = ProjectService(database)
    success = await project_service.delete_project(project_id)
    if not success:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({'result': 'success'})
