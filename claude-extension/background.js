// Claude AI Chrome Extension - Background Service Worker

// Install event - set up initial state
chrome.runtime.onInstalled.addListener((details) => {
  console.log('Claude Extension installed:', details.reason);

  // Set default settings
  chrome.storage.local.get(['apiKey', 'model'], (result) => {
    if (!result.model) {
      chrome.storage.local.set({ model: 'claude-sonnet-4-20250514' });
    }
  });

  // Create context menu items
  createContextMenus();
});

// Create context menu items
function createContextMenus() {
  // Remove existing menus first
  chrome.contextMenus.removeAll(() => {
    // Ask Claude about selected text
    chrome.contextMenus.create({
      id: 'ask-claude',
      title: 'Ask Claude about "%s"',
      contexts: ['selection']
    });

    // Explain selected text
    chrome.contextMenus.create({
      id: 'explain-claude',
      title: 'Explain with Claude',
      contexts: ['selection']
    });

    // Summarize page
    chrome.contextMenus.create({
      id: 'summarize-page',
      title: 'Summarize this page with Claude',
      contexts: ['page']
    });
  });
}

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  switch (info.menuItemId) {
    case 'ask-claude':
      await handleAskClaude(info.selectionText, tab);
      break;
    case 'explain-claude':
      await handleExplainClaude(info.selectionText, tab);
      break;
    case 'summarize-page':
      await handleSummarizePage(tab);
      break;
  }
});

// Handle "Ask Claude" context menu action
async function handleAskClaude(selectedText, tab) {
  const prompt = `Please help me understand or answer questions about the following text:\n\n"${selectedText}"`;
  await storePromptAndOpenPopup(prompt, tab);
}

// Handle "Explain" context menu action
async function handleExplainClaude(selectedText, tab) {
  const prompt = `Please explain the following text in simple terms:\n\n"${selectedText}"`;
  await storePromptAndOpenPopup(prompt, tab);
}

// Handle "Summarize Page" context menu action
async function handleSummarizePage(tab) {
  try {
    // Inject content script to get page content
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        // Get the main content of the page
        const article = document.querySelector('article') || document.body;
        const text = article.innerText.substring(0, 10000); // Limit to 10k chars
        return text;
      }
    });

    if (results && results[0] && results[0].result) {
      const pageContent = results[0].result;
      const prompt = `Please summarize the following webpage content:\n\n${pageContent}`;
      await storePromptAndOpenPopup(prompt, tab);
    }
  } catch (error) {
    console.error('Error getting page content:', error);
  }
}

// Store prompt and open popup
async function storePromptAndOpenPopup(prompt, tab) {
  // Store the pending prompt
  await chrome.storage.local.set({ pendingPrompt: prompt });

  // Open the popup (this will trigger the popup to check for pending prompt)
  chrome.action.openPopup();
}

// Handle messages from popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case 'getPendingPrompt':
      chrome.storage.local.get(['pendingPrompt'], (result) => {
        sendResponse({ prompt: result.pendingPrompt || null });
        // Clear the pending prompt
        chrome.storage.local.remove('pendingPrompt');
      });
      return true; // Required for async sendResponse

    case 'getSettings':
      chrome.storage.local.get(['apiKey', 'model'], (result) => {
        sendResponse(result);
      });
      return true;

    case 'saveSettings':
      chrome.storage.local.set({
        apiKey: request.apiKey,
        model: request.model
      }, () => {
        sendResponse({ success: true });
      });
      return true;

    default:
      sendResponse({ error: 'Unknown action' });
  }
});

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
  if (command === 'open-claude') {
    chrome.action.openPopup();
  }
});

// Keep service worker alive for better responsiveness
chrome.alarms.create('keepAlive', { periodInMinutes: 4 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive') {
    console.log('Claude Extension: Service worker heartbeat');
  }
});
