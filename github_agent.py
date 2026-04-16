"""
github_agent.py
---------------
GitHub agent built on the Microsoft Agent Framework.
Uses the GitHub MCP server to interact with GitHub repositories,
issues, pull requests, and more via natural language.

Usage:
    python github_agent.py
"""

import asyncio
import os

from agent_framework import Agent, InMemoryHistoryProvider
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FOUNDRY_ENDPOINT = os.environ["AZURE_FOUNDRY_ENDPOINT"]
FOUNDRY_MODEL = os.environ.get("AZURE_FOUNDRY_MODEL", "gpt-4o")
GITHUB_PAT = os.environ["GITHUB_PAT"]

# ---------------------------------------------------------------------------
# Interactive console loop
# ---------------------------------------------------------------------------
async def run_interactive() -> None:
    print("=" * 60)
    print("  GitHub Agent (Microsoft Agent Framework + GitHub MCP)")
    print("  Ask me anything about GitHub repositories and more.")
    print("  Type 'exit' or press Ctrl+C to quit")
    print("=" * 60)

    async with AzureCliCredential() as credential:
        client = FoundryChatClient(
            project_endpoint=FOUNDRY_ENDPOINT,
            model=FOUNDRY_MODEL,
            credential=credential,
        )

        github_mcp_tool = client.get_mcp_tool(
            name="GitHub",
            url="https://api.githubcopilot.com/mcp/",
            headers={"Authorization": f"Bearer {GITHUB_PAT}"},
            approval_mode="never_require",
        )

        async with Agent(
            client=client,
            name="GitHubAgent",
            instructions=(
                "You are a helpful assistant that can help users interact with GitHub. "
                "You can search for repositories, read file contents, check issues, and more. "
                "Always be clear about what operations you are performing."
            ),
            tools=[github_mcp_tool],
            context_providers=[
                InMemoryHistoryProvider(load_messages=True),
            ],
        ) as agent:
            session = agent.create_session()

            while True:
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    break

                if not user_input:
                    continue
                if user_input.lower() in {"exit", "quit"}:
                    print("Goodbye!")
                    break

                result = await agent.run(user_input, session=session)
                print(f"\nAgent: {result.text}")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(run_interactive())
    except KeyboardInterrupt:
        pass