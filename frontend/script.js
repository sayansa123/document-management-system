// Configuration
const API_BASE_URL = 'http://localhost:8000';
let currentPage = 1;
let totalFiles = 0;
let filesPerPage = 50;

// Tab switching
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');
    });
});

// File input display
document.getElementById('fileInput').addEventListener('change', function(e) {
    if (this.files.length > 0) {
        document.getElementById('fileName').textContent = `Selected: ${this.files[0].name}`;
    }
});

// Upload form submission
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const description = document.getElementById('description').value;
    const tags = document.getElementById('tags').value;
    const uploadBtn = document.getElementById('uploadBtn');
    const resultDiv = document.getElementById('uploadResult');
    
    if (!fileInput.files.length) {
        showMessage(resultDiv, 'Please select a file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('files', fileInput.files[0]);
    formData.append('description', description);
    formData.append('tags', tags.split(',').map(tag => tag.trim()).filter(tag => tag));
    
    try {
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        uploadBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/document/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage(resultDiv, result.message || 'File uploaded successfully!', 'success');
            document.getElementById('uploadForm').reset();
            document.getElementById('fileName').textContent = '';
        } else {
            showMessage(resultDiv, result.detail || 'Upload failed', 'error');
        }
    } catch (error) {
        showMessage(resultDiv, 'Network error: ' + error.message, 'error');
    } finally {
        uploadBtn.innerHTML = '<i class="fas fa-upload"></i> Upload Document';
        uploadBtn.disabled = false;
    }
});

// Load files
document.getElementById('loadFilesBtn').addEventListener('click', loadFiles);
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        loadFiles();
    }
});
document.getElementById('nextPage').addEventListener('click', () => {
    if (currentPage * filesPerPage < totalFiles) {
        currentPage++;
        loadFiles();
    }
});
document.getElementById('pageLimit').addEventListener('change', () => {
    filesPerPage = parseInt(document.getElementById('pageLimit').value);
    currentPage = 1;
    loadFiles();
});
document.getElementById('pageNumber').addEventListener('change', () => {
    currentPage = parseInt(document.getElementById('pageNumber').value);
    loadFiles();
});

async function loadFiles() {
    const container = document.getElementById('filesContainer');
    const pagination = document.getElementById('pagination');
    const pageInfo = document.getElementById('pageInfo');
    
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><p>Loading files...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/document/retrival?page=${currentPage}&limit=${filesPerPage}`);
        const files = await response.json();
        
        if (files.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <h3>No files found</h3>
                    <p>Upload some files to get started</p>
                </div>
            `;
            pagination.style.display = 'none';
            return;
        }
        
        let html = '<div class="files-grid">';
        files.forEach(file => {
            const uploadDate = new Date(file.uploaded_at).toLocaleDateString();
            const fileSizeMB = (file.file_size / (1024 * 1024)).toFixed(2);
            const tags = file.mongo?.tags || [];
            
            html += `
                <div class="file-card">
                    <div class="file-header">
                        <div class="file-type">${getFileTypeIcon(file.file_type)} ${file.file_type.split('/')[1] || 'File'}</div>
                        <span style="color: #64748b; font-size: 0.9rem;">ID: ${file.id}</span>
                    </div>
                    <div class="file-name">${file.file_name}</div>
                    <div class="file-meta">
                        <div><i class="fas fa-calendar"></i> ${uploadDate}</div>
                        <div><i class="fas fa-weight-hanging"></i> ${fileSizeMB} MB</div>
                    </div>
                    ${file.mongo?.description ? `<p style="margin: 10px 0; color: #475569;">${file.mongo.description}</p>` : ''}
                    ${tags.length > 0 ? `
                        <div class="file-tags">
                            ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    <div class="file-actions">
                        <button class="btn" onclick="downloadFile(${file.id})">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <button class="btn btn-secondary" onclick="viewFileDetails(${file.id})">
                            <i class="fas fa-eye"></i> Details
                        </button>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        
        container.innerHTML = html;
        
        // Update pagination
        totalFiles = files.length * currentPage; // Simplified estimation
        pageInfo.textContent = `Page ${currentPage}`;
        document.getElementById('pageNumber').value = currentPage;
        pagination.style.display = 'flex';
        
    } catch (error) {
        container.innerHTML = `<div class="error"><i class="fas fa-exclamation-triangle"></i> Failed to load files: ${error.message}</div>`;
        pagination.style.display = 'none';
    }
}

// Download file
async function downloadFile(id) {
    try {
        window.open(`${API_BASE_URL}/document/download/${id}`, '_blank');
    } catch (error) {
        alert('Failed to download file: ' + error.message);
    }
}

// View file details
function viewFileDetails(id) {
    alert(`File ID: ${id}\n\nViewing detailed information...\n\nYou can implement a modal or detailed view here.`);
}

// Search form
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileType = document.getElementById('searchFileType').value;
    const fileName = document.getElementById('searchFileName').value;
    const tag = document.getElementById('searchTag').value;
    const minSize = document.getElementById('minSize').value;
    const maxSize = document.getElementById('maxSize').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    let url = `${API_BASE_URL}/document/searching_Filtering?`;
    const params = [];
    
    if (fileType) params.push(`file_type=${encodeURIComponent(fileType)}`);
    if (fileName) params.push(`file_name=${encodeURIComponent(fileName)}`);
    if (tag) params.push(`tag=${encodeURIComponent(tag)}`);
    if (minSize) params.push(`min_size=${minSize}`);
    if (maxSize) params.push(`max_size=${maxSize}`);
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);
    
    url += params.join('&');
    
    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><p>Searching...</p></div>';
    
    try {
        const response = await fetch(url);
        const files = await response.json();
        
        if (files.length === 0) {
            resultsDiv.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <h3>No files found</h3>
                    <p>Try different search criteria</p>
                </div>
            `;
            return;
        }
        
        let html = `<h3 style="margin-bottom: 20px;">Found ${files.length} files:</h3><div class="files-grid">`;
        files.forEach(file => {
            const uploadDate = new Date(file.uploaded_at).toLocaleDateString();
            const fileSizeMB = (file.file_size / (1024 * 1024)).toFixed(2);
            const tags = file.mongo?.tags || [];
            
            html += `
                <div class="file-card">
                    <div class="file-header">
                        <div class="file-type">${getFileTypeIcon(file.file_type)} ${file.file_type.split('/')[1] || 'File'}</div>
                        <span style="color: #64748b; font-size: 0.9rem;">ID: ${file.id}</span>
                    </div>
                    <div class="file-name">${file.file_name}</div>
                    <div class="file-meta">
                        <div><i class="fas fa-calendar"></i> ${uploadDate}</div>
                        <div><i class="fas fa-weight-hanging"></i> ${fileSizeMB} MB</div>
                    </div>
                    ${file.mongo?.description ? `<p style="margin: 10px 0; color: #475569;">${file.mongo.description}</p>` : ''}
                    ${tags.length > 0 ? `
                        <div class="file-tags">
                            ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    <div class="file-actions">
                        <button class="btn" onclick="downloadFile(${file.id})">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <button class="btn btn-danger" onclick="deleteFile(${file.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error"><i class="fas fa-exclamation-triangle"></i> Search failed: ${error.message}</div>`;
    }
});

// Reset search
document.getElementById('resetSearch').addEventListener('click', function() {
    document.getElementById('searchForm').reset();
    document.getElementById('searchResults').innerHTML = '';
});

// Delete file
document.getElementById('deleteBtn').addEventListener('click', async function() {
    const fileId = document.getElementById('deleteFileId').value;
    const resultDiv = document.getElementById('deleteResult');
    
    if (!fileId) {
        showMessage(resultDiv, 'Please enter a file ID', 'error');
        return;
    }
    
    if (!confirm(`Are you sure you want to soft delete file ID ${fileId}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/document/delete/${fileId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage(resultDiv, `File ID ${fileId} soft deleted successfully`, 'success');
            document.getElementById('deleteFileId').value = '';
        } else {
            const error = await response.json();
            showMessage(resultDiv, error.detail || 'Delete failed', 'error');
        }
    } catch (error) {
        showMessage(resultDiv, 'Network error: ' + error.message, 'error');
    }
});

// Reset MongoDB
document.getElementById('resetMongoBtn').addEventListener('click', async function() {
    if (!confirm('WARNING: This will delete ALL data from MongoDB. Are you sure?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/files/hard_delete?select_db=mongodb`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('MongoDB reset successfully');
        } else {
            alert('Reset failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Reset MySQL
document.getElementById('resetMySQLBtn').addEventListener('click', async function() {
    if (!confirm('WARNING: This will delete ALL data from MySQL (files table). Are you sure?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/files/hard_delete?select_db=mysql`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('MySQL table reset successfully');
        } else {
            alert('Reset failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Reset Local Files
document.getElementById('resetLocalBtn').addEventListener('click', async function() {
    if (!confirm('WARNING: This will delete ALL local uploaded files. Are you sure?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/files/hard_delete?select_db=local_files`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Local files reset successfully');
        } else {
            alert('Reset failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Helper function to show messages
function showMessage(container, message, type) {
    container.innerHTML = `
        <div class="${type}">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
            ${message}
        </div>
    `;
}

// Helper function to get file type icon
function getFileTypeIcon(fileType) {
    if (fileType.includes('pdf')) return '<i class="fas fa-file-pdf" style="color: #ef4444;"></i>';
    if (fileType.includes('image')) return '<i class="fas fa-file-image" style="color: #10b981;"></i>';
    if (fileType.includes('csv')) return '<i class="fas fa-file-csv" style="color: #f59e0b;"></i>';
    return '<i class="fas fa-file" style="color: #64748b;"></i>';
}

// Initialize by loading files
loadFiles();