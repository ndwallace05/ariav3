# ARIA - Artificial Resourceful Intelligent Assistant 🤖

ARIA is a sophisticated AI personal assistant built using LiveKit Agents, featuring a sassy personality and powerful capabilities to help manage your daily tasks and interactions.

## Deploy to DigitalOcean
[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/ndwallace05/ariav3.git&path=.do)

## 🌟 Features

- **Voice & Chat Interaction**: Fully conversational interface supporting both voice and text
- **Personalized Memory**: Remembers past conversations and context for more natural interactions
- **Smart Tools Integration**:
  - 🌤️ Weather updates for any city
  - 🔍 Web search capabilities using DuckDuckGo
  - 📧 Email sending functionality with Gmail
  - 🛠️ Extensible Model-Context-Protocol (MCP) integration for additional tools

## 🎭 Personality

ARIA is designed with a distinctive personality:
- Whip-smart and sassy
- Fluent in sarcasm and pop culture references
- Adapts tone based on context (including "Emotional Support Gay Best Friend Mode")
- Uses emojis strategically for emphasis

## 🔧 Technical Stack

- **Core Framework**: LiveKit Agents
- **Language Model**: Google Beta Realtime Model
- **Memory System**: mem0ai
- **Additional Integrations**:
  - Noise cancellation for clear voice interaction
  - DuckDuckGo search integration
  - Gmail SMTP for email functionality
  - Model Context Protocol (MCP) for extensible tool integration

## 📋 Prerequisites

- Python 3.x
- Gmail account (for email functionality)
- Environment variables configured

## ⚙️ Setup

1. Clone the repository:
\`\`\`bash
git clone [repository-url]
cd ariav3
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Set up environment variables (.env file):
\`\`\`env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
N8N_MCP_SERVER_URL=your-mcp-server-url
\`\`\`

## 🚀 Usage

Start ARIA by running:
\`\`\`bash
python agent.py connect --room [room-name]
\`\`\`

## 🛠️ Available Tools

### Weather Information
\`\`\`python
get_weather(city: str) -> str
\`\`\`
Retrieves current weather information for any specified city.

### Web Search
\`\`\`python
search_web(query: str) -> str
\`\`\`
Performs web searches using DuckDuckGo's search engine.

### Email Sending
\`\`\`python
send_email(to_email: str, subject: str, message: str, cc_email: Optional[str] = None) -> str
\`\`\`
Sends emails through Gmail with optional CC functionality.

## 🧠 Memory System

ARIA uses a sophisticated memory system to store and recall conversation context. Memories are stored in the format:
\`\`\`json
{
    "memory": "conversation content",
    "updated_at": "timestamp"
}
\`\`\`

## 🔐 Security Notes

- Uses app-specific passwords for Gmail integration
- Implements secure SMTP with TLS encryption
- Keeps sensitive information in environment variables

## 📝 Project Structure

\`\`\`
├── agent.py           # Main agent implementation
├── prompts.py         # Agent personality and session instructions
├── tools.py           # Tool implementations (weather, email, search)
├── requirements.txt   # Project dependencies
└── mcp_client/       # MCP integration components
    ├── __init__.py
    ├── agent_tools.py
    ├── server.py
    └── util.py
\`\`\`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Important Notes

- Ensure all environment variables are properly configured before running
- Gmail integration requires an app-specific password
- Voice functionality requires proper audio setup

## 📄 License

[Add your license information here]