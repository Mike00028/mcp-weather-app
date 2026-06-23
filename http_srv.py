"""MCP weather server boilerplate over Streamable HTTP transport.

Student starter file. Keep this focused on transport + tool wiring.
"""

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
    # TODO(Assignment 2/3): Wire to data layer and keep behavior equal to stdio tool.
    _ = state
    return "TODO: wire get_alerts tool"


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
    """
    # TODO(Assignment 2/3): Wire to data layer and keep behavior equal to stdio tool.
    _ = (latitude, longitude)
    return "TODO: wire get_forecast tool"


def main() -> None:
    # Keep env reads for assignment discussion around HTTP endpoint config.
    os.getenv("MCP_HOST", "127.0.0.1")
    os.getenv("MCP_PORT", "8000")
    os.getenv("MCP_PATH", "/mcp")

    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
