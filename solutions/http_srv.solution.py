"""MCP weather server boilerplate over Streamable HTTP transport."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from src.weather_data import get_alerts_for_state, get_forecast_for_coordinates

load_dotenv()

mcp = FastMCP("weather-http-lab")


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get active weather alerts for a US state.

    Args:
        state: Two-letter US state code, for example CA or NY.
    """
    return await get_alerts_for_state(state)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
    """
    return await get_forecast_for_coordinates(latitude, longitude)


def main() -> None:
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", "8000"))
    path = os.getenv("MCP_PATH", "/mcp")

    try:
        mcp.run(transport="streamable-http", host=host, port=port, path=path)
    except TypeError:
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
