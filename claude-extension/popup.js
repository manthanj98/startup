// Claude AI Chrome Extension - Popup Script

class ClaudeExtension {
  constructor() {
    this.apiKey = '';
    this.model = 'claude-sonnet-4-20250514';
    this.conversationHistory = [];
    this.isLoading = false;

    this.init();
  }

  async init() {
    await this.loadSettings();
    this.bindElements();
    this.bindEvents();
    this.checkApiKey();
  }

  bindElements() {
    // Panels
    this.settingsPanel = document.getElementById('settings-panel');
    this.chatPanel = document.getElementById('chat-panel');

    // Settings elements
    this.apiKeyInput = document.getElementById('api-key');
    this.modelSelect = document.getElementById('model-select');
    this.saveSettingsBtn = document.getElementById('save-settings');
    this.openSettingsBtn = document.getElementById('open-settings');
    this.closeSettingsBtn = document.getElementById('close-settings');
    this.toggleKeyBtn = document.getElementById('toggle-key');

    // Chat elements
    this.messagesContainer = document.getElementById('messages');
    this.userInput = document.getElementById('user-input');
    this.sendBtn = document.getElementById('send-btn');
    this.newChatBtn = document.getElementById('new-chat');

    // Status bar
    this.statusBar = document.getElementById('status-bar');
    this.statusText = document.getElementById('status-text');
  }

  bindEvents() {
    // Settings events
    this.openSettingsBtn.addEventListener('click', () => this.showSettings());
    this.closeSettingsBtn.addEventListener('click', () => this.hideSettings());
    this.saveSettingsBtn.addEventListener('click', () => this.saveSettings());
    this.toggleKeyBtn.addEventListener('click', () => this.toggleApiKeyVisibility());

    // Chat events
    this.sendBtn.addEventListener('click', () => this.sendMessage());
    this.newChatBtn.addEventListener('click', () => this.startNewChat());

    // Input events
    this.userInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    this.userInput.addEventListener('input', () => this.autoResizeTextarea());
  }

  async loadSettings() {
    return new Promise((resolve) => {
      chrome.storage.local.get(['apiKey', 'model', 'conversationHistory'], (result) => {
        if (result.apiKey) {
          this.apiKey = result.apiKey;
        }
        if (result.model) {
          this.model = result.model;
        }
        if (result.conversationHistory) {
          this.conversationHistory = result.conversationHistory;
        }
        resolve();
      });
    });
  }

  async saveSettings() {
    this.apiKey = this.apiKeyInput.value.trim();
    this.model = this.modelSelect.value;

    await chrome.storage.local.set({
      apiKey: this.apiKey,
      model: this.model
    });

    this.updateStatus('Settings saved!', 'success');
    setTimeout(() => {
      this.hideSettings();
      this.updateStatus('Ready');
    }, 1000);
  }

  checkApiKey() {
    if (!this.apiKey) {
      this.showSettings();
      this.updateStatus('Please enter your API key', 'error');
    } else {
      this.apiKeyInput.value = this.apiKey;
      this.modelSelect.value = this.model;
      this.restoreConversation();
    }
  }

  showSettings() {
    this.settingsPanel.classList.remove('hidden');
    this.chatPanel.classList.add('hidden');
    this.apiKeyInput.value = this.apiKey;
    this.modelSelect.value = this.model;
  }

  hideSettings() {
    if (!this.apiKey) {
      this.updateStatus('API key is required', 'error');
      return;
    }
    this.settingsPanel.classList.add('hidden');
    this.chatPanel.classList.remove('hidden');
  }

  toggleApiKeyVisibility() {
    const type = this.apiKeyInput.type === 'password' ? 'text' : 'password';
    this.apiKeyInput.type = type;
  }

  autoResizeTextarea() {
    this.userInput.style.height = 'auto';
    this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
  }

  async sendMessage() {
    const message = this.userInput.value.trim();

    if (!message || this.isLoading) return;

    if (!this.apiKey) {
      this.showSettings();
      this.updateStatus('Please enter your API key', 'error');
      return;
    }

    // Clear welcome message if it exists
    const welcomeMessage = this.messagesContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
      welcomeMessage.remove();
    }

    // Add user message to UI
    this.addMessage(message, 'user');
    this.userInput.value = '';
    this.autoResizeTextarea();

    // Add to conversation history
    this.conversationHistory.push({
      role: 'user',
      content: message
    });

    // Show loading state
    this.setLoading(true);
    this.showTypingIndicator();

    try {
      const response = await this.callClaudeAPI(message);
      this.removeTypingIndicator();

      // Add assistant response to history and UI
      this.conversationHistory.push({
        role: 'assistant',
        content: response
      });

      this.addMessage(response, 'assistant');

      // Save conversation
      await chrome.storage.local.set({
        conversationHistory: this.conversationHistory
      });

      this.updateStatus('Ready');
    } catch (error) {
      this.removeTypingIndicator();
      this.addMessage(`Error: ${error.message}`, 'error');
      this.updateStatus('Error occurred', 'error');
    } finally {
      this.setLoading(false);
    }
  }

  async callClaudeAPI(message) {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': this.apiKey,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true'
      },
      body: JSON.stringify({
        model: this.model,
        max_tokens: 4096,
        messages: this.conversationHistory
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'API request failed');
    }

    const data = await response.json();
    return data.content[0].text;
  }

  addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = this.formatMessage(content);
    this.messagesContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }

  formatMessage(content) {
    // Basic markdown-like formatting
    let formatted = content
      // Escape HTML
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // Code blocks
      .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
      // Inline code
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      // Bold
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      // Line breaks
      .replace(/\n/g, '<br>');

    return formatted;
  }

  showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message assistant typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    this.messagesContainer.appendChild(indicator);
    this.scrollToBottom();
  }

  removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  setLoading(loading) {
    this.isLoading = loading;
    this.sendBtn.disabled = loading;
    this.userInput.disabled = loading;

    if (loading) {
      this.updateStatus('Claude is thinking...');
    }
  }

  startNewChat() {
    this.conversationHistory = [];
    this.messagesContainer.innerHTML = `
      <div class="welcome-message">
        <p>Hello! I'm Claude, an AI assistant made by Anthropic.</p>
        <p>How can I help you today?</p>
      </div>
    `;

    chrome.storage.local.set({ conversationHistory: [] });
    this.updateStatus('New conversation started');
    setTimeout(() => this.updateStatus('Ready'), 1500);
  }

  restoreConversation() {
    if (this.conversationHistory.length > 0) {
      // Clear welcome message
      this.messagesContainer.innerHTML = '';

      // Restore messages
      this.conversationHistory.forEach((msg) => {
        this.addMessage(msg.content, msg.role);
      });
    }
  }

  updateStatus(message, type = '') {
    this.statusText.textContent = message;
    this.statusBar.className = 'status-bar';
    if (type) {
      this.statusBar.classList.add(type);
    }
  }
}

// Initialize the extension when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new ClaudeExtension();
});
