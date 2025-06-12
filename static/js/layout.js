// Toggle functionality
        document.addEventListener('DOMContentLoaded', function() {
            const sidebarToggle = document.getElementById('sidebarToggle');
            const projectFilesToggle = document.getElementById('projectFilesToggle');
            const sidebar = document.getElementById('sidebar');
            const projectFiles = document.getElementById('projectFiles');
            const mainContent = document.getElementById('mainContent');
            const mobileOverlay = document.getElementById('mobileOverlay');
            const chatFooter = document.getElementById('chatFooter');
            const sidebarToggleIcon = document.querySelector('.sidebar-toggle-icon');
            const projectToggleIcon = document.querySelector('.project-toggle-icon');
            
            let sidebarOpen = window.innerWidth >= 1024; // lg breakpoint
            let projectFilesOpen = window.innerWidth >= 1024;
            
            function updateLayout() {
                const isLargeScreen = window.innerWidth >= 1024;
                
                // Update sidebar and its icon
                if (sidebarOpen) {
                    sidebar.classList.remove('sidebar-closed');
                    sidebar.classList.add('sidebar-open');
                    if (sidebarToggleIcon) {
                        sidebarToggleIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>`; // Shows ">" pointing right when open
                    }
                } else {
                    sidebar.classList.remove('sidebar-open');
                    sidebar.classList.add('sidebar-closed');
                    if (sidebarToggleIcon) {
                        sidebarToggleIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>`; // Shows ">" pointing right when closed
                    }
                }
                
                // Update project files and its icon
                if (projectFilesOpen) {
                    projectFiles.classList.remove('project-files-closed');
                    projectFiles.classList.add('project-files-open');
                    if (projectToggleIcon) {
                        projectToggleIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>`; // Shows "<" pointing left when open
                    }
                } else {
                    projectFiles.classList.remove('project-files-open');
                    projectFiles.classList.add('project-files-closed');
                    if (projectToggleIcon) {
                        projectToggleIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>`; // Shows "<" pointing left when closed
                    }
                }
                
                // Update footer positioning for large screens
                if (isLargeScreen) {
                    // Update footer positioning
                    let footerLeft = sidebarOpen ? 'lg:left-64' : 'lg:left-0';
                    let footerRight = projectFilesOpen ? 'lg:right-64' : 'lg:right-0';
                    if (chatFooter) {
                        chatFooter.className = `fixed bottom-0 left-0 right-0 bg-gray-800 text-gray-100 px-4 py-4 z-30 shadow-lg transition-all duration-300 ${footerLeft} ${footerRight}`;
                    }
                    
                    mobileOverlay.classList.add('hidden');
                } else {
                    if (chatFooter) {
                        chatFooter.className = 'fixed bottom-0 left-0 right-0 bg-gray-800 text-gray-100 px-4 py-4 z-30 shadow-lg transition-all duration-300';
                    }
                    
                    // Show overlay if any panel is open on mobile
                    if (sidebarOpen || projectFilesOpen) {
                        mobileOverlay.classList.remove('hidden');
                    } else {
                        mobileOverlay.classList.add('hidden');
                    }
                }
            }
            
            // Sidebar toggle
            if (sidebarToggle) {
                sidebarToggle.addEventListener('click', function() {
                    sidebarOpen = !sidebarOpen;
                    updateLayout();
                });
            }
            
            // Project files toggle
            if (projectFilesToggle) {
                projectFilesToggle.addEventListener('click', function() {
                    projectFilesOpen = !projectFilesOpen;
                    updateLayout();
                });
            }
            
            // Mobile overlay click to close panels
            if (mobileOverlay) {
                mobileOverlay.addEventListener('click', function() {
                    sidebarOpen = false;
                    projectFilesOpen = false;
                    updateLayout();
                });
            }
            
            // Handle window resize
            window.addEventListener('resize', function() {
                const isLargeScreen = window.innerWidth >= 1024;
                if (isLargeScreen) {
                    sidebarOpen = true;
                    projectFilesOpen = true;
                } else {
                    sidebarOpen = false;
                    projectFilesOpen = false;
                }
                updateLayout();
            });
            
            // Initialize
            updateLayout();
        });