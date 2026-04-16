# GitHub MCP Agent

A minimal example showing how to connect the **Microsoft Agent Framework** to an external data source via the **Model Context Protocol (MCP)** — using GitHub as the MCP server.

The agent connects to GitHub's remote MCP server and can answer natural language questions about repositories, issues, pull requests, files, and more.

## What this project demonstrates

- **MCP integration** — connecting an agent to a remote MCP server via `client.get_mcp_tool()`
- **Tool discovery** — the agent automatically discovers available tools from the MCP server at runtime
- **Creating an agent** with `FoundryChatClient` and `Agent(client=..., instructions=...)`
- **Multi-turn conversation** with `agent.create_session()` and `InMemoryHistoryProvider`
- **Keyless authentication** via `AzureCliCredential` — no API keys required for Azure resources

## What is MCP?

Model Context Protocol (MCP) is an open standard that allows agents to connect to external tools and data sources in a standardized way. Instead of writing custom tool code, you point the agent at an MCP-compliant server — and the agent automatically discovers and uses the tools it provides.

This makes it easy to swap out data sources without changing agent code.

## Project structure

```
├── github_agent.py     # Agent with GitHub MCP tool
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
└── LICENSE
```

## Prerequisites

- Python 3.11+
- [Azure CLI](https://aka.ms/installazurecli) — used for keyless authentication
- An [Azure subscription](https://azure.microsoft.com/free/)
- An **Azure AI Foundry** project with a deployed `gpt-4o` model
- A **GitHub Personal Access Token** with `repo` and `read:user` scopes
  - Create one at [github.com/settings/tokens](https://github.com/settings/tokens)

## Setup

**1. Clone the repository and install dependencies**

```bash
git clone https://github.com/MaximilianRogath/GitHub-MCP-Agent
cd GitHub-MCP-Agent
python -m pip install -r requirements.txt
```

**2. Log in to Azure**

```bash
az login
```

**3. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your Foundry endpoint and GitHub PAT.

**4. Start the agent**

```bash
python github_agent.py
```

## Example interaction

```
You: What is my GitHub username and tell me about my account?
Agent: Your GitHub username is MaximilianRogath. Here's some information
       about your account: Name: Maximilian Rogath, Public Repositories: 7 ...

You: List all my repositories
Agent: Here's the list of your public repositories: 1. MAI-Image-2-Agent ...

You: Show me the open issues in my Contoso-FAQ-Agent repo
Agent: Here are the open issues in MaximilianRogath/Contoso-FAQ-Agent ...
```

## Further reading

- [MCP and Foundry Agents Documentation](https://learn.microsoft.com/en-us/agent-framework/agents/tools/hosted-mcp-tools)
- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Microsoft Foundry](https://ai.azure.com/)

## Credits

The MCP integration pattern in this project is based on the official Microsoft Agent Framework documentation:

- [MCP and Foundry Agents](https://learn.microsoft.com/en-us/agent-framework/agents/tools/hosted-mcp-tools) — Microsoft Learn

## License

This project is licensed under the [MIT License](LICENSE).
