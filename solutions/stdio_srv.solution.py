"""MCP weather server boilerplate over STDIO transport."""

from __future__ import annotations

import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from src.weather_data import get_alerts_for_state, get_forecast_for_coordinates

load_dotenv()

mcp = FastMCP("weather-stdio-lab")


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
    # For stdio servers, logging must avoid stdout.
    print("Starting weather MCP stdio server", file=sys.stderr)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
