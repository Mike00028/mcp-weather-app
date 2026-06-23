"""Optional LangChain client for MCP server exercises with Gemini.

This file is for assignment use. It can connect to either stdio or HTTP MCP server.

Student starter file:
- Use this for Assignment 1 and Assignment 2 validation.
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient


async def build_client() -> MultiServerMCPClient:
    mode = os.getenv("MCP_CLIENT_MODE", "stdio").strip().lower()

    if mode == "http":
        url = os.getenv("MCP_HTTP_URL", "http://127.0.0.1:8000/mcp")
        return MultiServerMCPClient(
            {
                "weather_http": {
                    "transport": "streamable_http",
                    "url": url,
                }
            }
        )

    return MultiServerMCPClient(
        {
            "weather_stdio": {
                "transport": "stdio",
                "command": "python",
                "args": ["stdio_srv.py"],
            }
        }
    )


async def main() -> None:
    load_dotenv()

    tools = await (await build_client()).get_tools()
    print("Discovered tools:")
    for tool in tools:
        print(f"- {tool.name}")

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No Gemini key set; listing tools only.")
        return

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.prebuilt import create_react_agent

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=api_key,
    )
    agent = create_react_agent(model, tools)

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Get active alerts for CA and summarize key risks.",
                }
            ]
        }
    )
    print("\nAgent output:\n")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
