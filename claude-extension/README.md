# Claude AI Chrome Extension

A Chrome extension to interact with Claude AI, compatible with Chrome and Arc browsers.

## Features

- Chat with Claude AI directly from your browser
- Right-click context menu to ask Claude about selected text
- Summarize web pages with one click
- Dark mode interface
- Conversation history persistence
- Multiple Claude model options (Sonnet 4, Opus 4.5, Haiku 3.5)

## Installation

### Step 1: Generate Icons

1. Open `generate-icons.html` in your browser
2. Click "Download All Icons"
3. Move the downloaded files to the `icons/` folder
4. Rename them to: `icon16.png`, `icon32.png`, `icon48.png`, `icon128.png`

### Step 2: Load the Extension

**For Chrome:**
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `claude-extension` folder

**For Arc Browser:**
1. Open Arc and go to `arc://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `claude-extension` folder

### Step 3: Configure API Key

1. Click the Claude extension icon in your browser toolbar
2. Click the settings (gear) icon
3. Enter your Anthropic API key
4. Select your preferred model
5. Click "Save Settings"

## Getting an API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into the extension settings

## Usage

### Chat Interface
- Click the extension icon to open the chat popup
- Type your message and press Enter or click Send
- Use the "+" button to start a new conversation

### Context Menu
- Select text on any webpage
- Right-click and choose:
  - "Ask Claude about [text]" - Ask a question
  - "Explain with Claude" - Get an explanation
- Right-click anywhere on a page and select "Summarize this page with Claude"

### Keyboard Shortcuts
- Press Enter to send a message
- Shift+Enter for new line in message

## File Structure

```
claude-extension/
├── manifest.json       # Extension configuration
├── popup.html          # Main popup UI
├── popup.css           # Popup styles
├── popup.js            # Popup functionality
├── background.js       # Service worker
├── content.js          # Content script
├── content.css         # Content styles
├── generate-icons.html # Icon generator
├── README.md           # This file
└── icons/
    ├── icon.svg        # Source SVG icon
    ├── icon16.png      # 16x16 icon
    ├── icon32.png      # 32x32 icon
    ├── icon48.png      # 48x48 icon
    └── icon128.png     # 128x128 icon
```

## Troubleshooting

### Extension not loading
- Make sure all icon files exist in the `icons/` folder
- Check the browser console for errors

### API errors
- Verify your API key is correct
- Ensure you have sufficient API credits
- Check your internet connection

### CORS errors
- The extension uses the `anthropic-dangerous-direct-browser-access` header
- This is required for browser-based API calls

## Privacy

- Your API key is stored locally in Chrome storage
- Conversation history is stored locally
- No data is sent to any server except Anthropic's API

## License

MIT License
