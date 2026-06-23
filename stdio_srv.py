"""MCP weather server boilerplate over STDIO transport.

Student starter file. Keep this focused on transport + tool wiring.
"""

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
    # TODO(Assignment 1): Call get_alerts_for_state(state) and return its result.
    _ = state
    return "TODO: wire get_alerts tool"


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
    """
    # TODO(Assignment 1): Call get_forecast_for_coordinates(latitude, longitude).
    _ = (latitude, longitude)
    return "TODO: wire get_forecast tool"


def main() -> None:
    # For stdio servers, logging must avoid stdout.
    print("Starting weather MCP stdio server", file=sys.stderr)
    # TODO(Assignment 6): Add a separate stdio file-inspector server file.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
