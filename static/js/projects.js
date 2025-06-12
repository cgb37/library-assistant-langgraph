// Enhanced Projects CRUD functionality with better UX
document.addEventListener('DOMContentLoaded', function() {
    const projectForm = document.getElementById('project-form');
    const projectsList = document.getElementById('projects-list');
    const formTitle = document.getElementById('form-title');
    const submitButton = document.getElementById('submit-button');
    const submitText = document.getElementById('submit-text');
    const cancelButton = document.getElementById('cancel-button');
    const projectIdInput = document.getElementById('project-id');
    const projectNameInput = document.getElementById('project-name');
    const projectDescriptionInput = document.getElementById('project-description');

    let isEditing = false;
    let currentProjectId = null;

    // Reset form to create mode
    function resetForm() {
        isEditing = false;
        currentProjectId = null;
        projectIdInput.value = '';
        projectNameInput.value = '';
        projectDescriptionInput.value = '';
        formTitle.textContent = 'Create New Project';
        submitText.textContent = 'Create Project';
        cancelButton.classList.add('hidden');
        submitButton.className = submitButton.className.replace('bg-green-600 hover:bg-green-700', 'bg-blue-600 hover:bg-blue-700');
    }

    // Switch to edit mode
    function switchToEditMode(projectId, name, description) {
        isEditing = true;
        currentProjectId = projectId;
        projectIdInput.value = projectId;
        projectNameInput.value = name;
        projectDescriptionInput.value = description || '';
        formTitle.textContent = 'Edit Project';
        submitText.textContent = 'Update Project';
        cancelButton.classList.remove('hidden');
        submitButton.className = submitButton.className.replace('bg-blue-600 hover:bg-blue-700', 'bg-green-600 hover:bg-green-700');
        
        // Scroll to form and focus on name input
        projectNameInput.focus();
        projectNameInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Show loading state
    function setLoadingState(loading) {
        const originalText = submitText.textContent;
        if (loading) {
            submitButton.disabled = true;
            submitText.textContent = isEditing ? 'Updating...' : 'Creating...';
            submitButton.className = submitButton.className.replace(/bg-(blue|green)-600/, 'bg-gray-500').replace(/hover:bg-(blue|green)-700/, '');
        } else {
            submitButton.disabled = false;
            submitText.textContent = originalText;
            submitButton.className = submitButton.className.replace('bg-gray-500', isEditing ? 'bg-green-600' : 'bg-blue-600');
            if (isEditing) {
                submitButton.className += ' hover:bg-green-700';
            } else {
                submitButton.className += ' hover:bg-blue-700';
            }
        }
    }

    // Show success message
    function showMessage(message, type = 'success') {
        const alertClass = type === 'success' ? 'bg-green-100 border-green-400 text-green-700' : 'bg-red-100 border-red-400 text-red-700';
        const alert = document.createElement('div');
        alert.className = `fixed top-20 right-4 p-4 border-l-4 ${alertClass} rounded-md shadow-md z-50 max-w-md`;
        alert.innerHTML = `
            <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    }

    // Handle form submission (create or update)
    if (projectForm) {
        projectForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = projectNameInput.value.trim();
            const description = projectDescriptionInput.value.trim();
            
            if (!name) {
                projectNameInput.focus();
                return;
            }

            setLoadingState(true);
            
            try {
                const url = isEditing ? `/api/projects/${currentProjectId}` : '/api/projects/';
                const method = isEditing ? 'PUT' : 'POST';
                
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, description })
                });
                
                if (response.ok) {
                    const action = isEditing ? 'updated' : 'created';
                    showMessage(`Project ${action} successfully!`);
                    
                    if (isEditing) {
                        // If editing, we might stay on the same page
                        resetForm();
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        // If creating new project, redirect to projects list
                        setTimeout(() => location.href = '/projects', 1000);
                    }
                } else {
                    const error = await response.json();
                    showMessage('Error: ' + (error.error || 'Unknown error'), 'error');
                }
            } catch (error) {
                showMessage('Network error: ' + error.message, 'error');
            } finally {
                setLoadingState(false);
            }
        });
    }

    // Handle cancel button
    if (cancelButton) {
        cancelButton.addEventListener('click', function() {
            // If we're on the create page and cancel, go back to projects list
            if (window.location.pathname === '/projects/create') {
                window.location.href = '/projects';
            } else {
                resetForm();
            }
        });
    }

    // Handle edit and delete buttons
    if (projectsList) {
        projectsList.addEventListener('click', async function(e) {
            const button = e.target.closest('button');
            if (!button) return;

            const projectId = button.dataset.projectId;
            
            if (button.classList.contains('edit-project')) {
                const name = button.dataset.projectName;
                const description = button.dataset.projectDescription;
                
                // On the projects list page, redirect to edit
                // Navigate to edit page with the project ID
                window.location.href = `/projects/edit/${projectId}`;
            }
            
            if (button.classList.contains('delete-project')) {
                const projectName = button.closest('.project-item').querySelector('.project-name').textContent.trim();
                
                if (confirm(`Are you sure you want to delete "${projectName}"? This action cannot be undone.`)) {
                    // Show loading state for delete button
                    const originalHTML = button.innerHTML;
                    button.innerHTML = '<svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>';
                    button.disabled = true;
                    
                    try {
                        const response = await fetch(`/api/projects/${projectId}`, {
                            method: 'DELETE'
                        });
                        
                        if (response.ok) {
                            showMessage('Project deleted successfully!');
                            // Reset form if we were editing this project
                            if (currentProjectId === projectId) {
                                resetForm();
                            }
                            setTimeout(() => location.reload(), 1000);
                        } else {
                            const error = await response.json();
                            showMessage('Error: ' + (error.error || 'Unknown error'), 'error');
                            button.innerHTML = originalHTML;
                            button.disabled = false;
                        }
                    } catch (error) {
                        showMessage('Network error: ' + error.message, 'error');
                        button.innerHTML = originalHTML;
                        button.disabled = false;
                    }
                }
            }
        });
    }

    // Initialize form based on the current page
    if (projectForm) {
        const pathname = window.location.pathname;
        
        if (pathname === '/projects/create') {
            // Create mode
            resetForm();
        } else if (pathname.startsWith('/projects/edit/')) {
            // Edit mode - extract the project ID from the URL
            const projectId = pathname.split('/').pop();
            
            if (projectId && projectIdInput) {
                // Get existing values from the form (already populated by the template)
                const name = projectNameInput.value;
                const description = projectDescriptionInput.value;
                
                // Setup form for edit mode
                isEditing = true;
                currentProjectId = projectId;
                
                // Make sure the submit button has the right styling
                if (submitButton) {
                    submitButton.className = submitButton.className.replace('bg-blue-600 hover:bg-blue-700', 'bg-green-600 hover:bg-green-700');
                }
                
                if (submitText) {
                    submitText.textContent = 'Update Project';
                }
                
                if (cancelButton) {
                    cancelButton.classList.remove('hidden');
                }
            }
        }
    }
});
