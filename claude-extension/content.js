// Claude AI Chrome Extension - Content Script

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case 'getSelectedText':
      const selectedText = window.getSelection().toString().trim();
      sendResponse({ text: selectedText });
      break;

    case 'getPageContent':
      const pageContent = getMainContent();
      sendResponse({ content: pageContent });
      break;

    case 'showNotification':
      showFloatingNotification(request.message, request.type);
      sendResponse({ success: true });
      break;

    default:
      sendResponse({ error: 'Unknown action' });
  }
  return true;
});

// Extract main content from the page
function getMainContent() {
  // Try to find the main content area
  const selectors = [
    'article',
    'main',
    '[role="main"]',
    '.post-content',
    '.article-content',
    '.entry-content',
    '#content',
    '.content'
  ];

  let contentElement = null;

  for (const selector of selectors) {
    contentElement = document.querySelector(selector);
    if (contentElement) break;
  }

  // Fall back to body if no main content found
  if (!contentElement) {
    contentElement = document.body;
  }

  // Get text content, limiting to reasonable size
  let text = contentElement.innerText;

  // Clean up the text
  text = text
    .replace(/\s+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
    .substring(0, 15000); // Limit to ~15k characters

  return text;
}

// Show a floating notification on the page
function showFloatingNotification(message, type = 'info') {
  // Remove existing notification if any
  const existing = document.getElementById('claude-notification');
  if (existing) {
    existing.remove();
  }

  // Create notification element
  const notification = document.createElement('div');
  notification.id = 'claude-notification';
  notification.className = `claude-notification claude-notification-${type}`;
  notification.innerHTML = `
    <div class="claude-notification-icon">
      <svg width="20" height="20" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="14" fill="#D97706"/>
        <path d="M10 16C10 12.6863 12.6863 10 16 10C19.3137 10 22 12.6863 22 16C22 19.3137 19.3137 22 16 22" stroke="white" stroke-width="2" stroke-linecap="round"/>
        <circle cx="16" cy="16" r="3" fill="white"/>
      </svg>
    </div>
    <span class="claude-notification-message">${escapeHtml(message)}</span>
    <button class="claude-notification-close">&times;</button>
  `;

  // Add close functionality
  notification.querySelector('.claude-notification-close').addEventListener('click', () => {
    notification.classList.add('claude-notification-hiding');
    setTimeout(() => notification.remove(), 300);
  });

  // Append to page
  document.body.appendChild(notification);

  // Auto-hide after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.classList.add('claude-notification-hiding');
      setTimeout(() => notification.remove(), 300);
    }
  }, 5000);
}

// Helper function to escape HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Optional: Add keyboard shortcut listener for quick actions
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + Shift + C to send selected text to Claude
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      chrome.runtime.sendMessage({
        action: 'quickAsk',
        text: selectedText
      });
    }
  }
});

console.log('Claude AI Extension: Content script loaded');
