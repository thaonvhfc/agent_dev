class ChatbotApp {
    constructor() {
        this.uploadedFiles = new Set();
        this.isProcessing = false;
        this.initializeElements();
        this.bindEvents();
        this.loadUploadedFiles(); // Thêm dòng này
    }

    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.uploadProgress = document.getElementById('uploadProgress');
        this.fileList = document.getElementById('fileList');
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.notificationToast = new bootstrap.Toast(document.getElementById('notificationToast'));
        this.toastBody = document.getElementById('toastBody');
    }

    bindEvents() {
        // Upload events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Chat events
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    // Drag and Drop handlers
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileUpload(files[0]);
        }
    }

    // File handling
    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.handleFileUpload(file);
        }
    }

    async handleFileUpload(file) {
        if (!file.type.includes('pdf')) {
            this.showNotification('Chỉ chấp nhận file PDF!', 'error');
            return;
        }

        if (file.size > 10 * 1024 * 1024) { // 10MB
            this.showNotification('File quá lớn! Tối đa 10MB.', 'error');
            return;
        }

        if (this.uploadedFiles.has(file.name)) {
            this.showNotification('File này đã được tải lên!', 'warning');
            return;
        }

        this.showUploadProgress(true);
        
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                this.uploadedFiles.add(file.name);
                this.addFileToList(file.name, result.chunks_created);
                this.enableChat();
                this.showNotification(`File "${file.name}" đã được tải lên thành công! Tạo được ${result.chunks_created} đoạn văn bản.`, 'success');
            } else {
                this.showNotification(result.detail || 'Lỗi khi tải file!', 'error');
            }
        } catch (error) {
            this.showNotification('Lỗi kết nối! Vui lòng thử lại.', 'error');
            console.error('Upload error:', error);
        } finally {
            this.showUploadProgress(false);
            this.fileInput.value = '';
        }
    }

    showUploadProgress(show) {
        this.uploadProgress.style.display = show ? 'block' : 'none';
        if (show) {
            const progressBar = this.uploadProgress.querySelector('.progress-bar');
            let width = 0;
            const interval = setInterval(() => {
                width += Math.random() * 30;
                if (width >= 90) {
                    clearInterval(interval);
                    width = 90;
                }
                progressBar.style.width = width + '%';
            }, 200);
        }
    }

    // Thêm method mới để load danh sách file
    async loadUploadedFiles() {
        try {
            const response = await fetch('/api/files');
            const files = await response.json();
            
            if (files.length > 0) {
                this.fileList.innerHTML = '';
                files.forEach(file => {
                    this.addFileToList(file.filename, file.size);
                });
            }
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }

    // Cập nhật method addFileToList
    addFileToList(filename, filesize) {
        if (this.fileList.querySelector('p')) {
            this.fileList.innerHTML = '';
        }

        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        const size = (filesize / 1024 / 1024).toFixed(2); // Convert to MB
        
        fileItem.innerHTML = `
            <i class="fas fa-file-pdf"></i>
            <div class="file-info">
                <span>${filename}</span>
                <small>${size} MB</small>
            </div>
            <div class="file-actions">
                <button onclick="window.open('/uploads/${filename}', '_blank')" title="Xem">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        `;
        
        this.fileList.appendChild(fileItem);
    }

    enableChat() {
        this.messageInput.disabled = false;
        this.sendButton.disabled = false;
        this.messageInput.placeholder = 'Nhập câu hỏi của bạn...';
        this.messageInput.focus();
    }

    // Chat functionality
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isProcessing) return;

        this.isProcessing = true;
        this.messageInput.value = '';
        this.sendButton.disabled = true;

        // Add user message
        this.addMessage(message, 'user');

        // Show typing indicator
        const typingId = this.showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const result = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator(typingId);

            if (response.ok) {
                this.addMessage(result.response, 'bot', result.sources);
            } else {
                this.addMessage(result.detail || 'Lỗi khi xử lý câu hỏi!', 'bot');
            }
        } catch (error) {
            this.removeTypingIndicator(typingId);
            this.addMessage('Lỗi kết nối! Vui lòng thử lại.', 'bot');
            console.error('Chat error:', error);
        } finally {
            this.isProcessing = false;
            this.sendButton.disabled = false;
            this.messageInput.focus();
        }
    }

    addMessage(content, sender, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatar = sender === 'user' ? 
            '<i class="fas fa-user"></i>' : 
            '<i class="fas fa-robot"></i>';

        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = `
                <div class="message-sources">
                    <strong>Nguồn tham khảo:</strong>
                    ${sources.map(source => `<div class="source-item"><i class="fas fa-file-pdf"></i> ${source}</div>`).join('')}
                </div>
            `;
        }

        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <p>${this.formatMessage(content)}</p>
                ${sourcesHtml}
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(message) {
        // Simple formatting for line breaks
        return message.replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        const typingId = 'typing-' + Date.now();
        typingDiv.id = typingId;
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <div class="message-avatar"><i class="fas fa-robot"></i></div>
            <div class="message-content typing-indicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        return typingId;
    }

    removeTypingIndicator(typingId) {
        const typingElement = document.getElementById(typingId);
        if (typingElement) {
            typingElement.remove();
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showNotification(message, type = 'info') {
        const iconMap = {
            'success': 'fas fa-check-circle text-success',
            'error': 'fas fa-exclamation-circle text-danger',
            'warning': 'fas fa-exclamation-triangle text-warning',
            'info': 'fas fa-info-circle text-info'
        };

        this.toastBody.innerHTML = `
            <i class="${iconMap[type]} me-2"></i>
            ${message}
        `;

        this.notificationToast.show();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotApp();
});