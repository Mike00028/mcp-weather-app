"""Weather.gov data layer used by MCP server tools.

Student starter file:
- Implement the TODO blocks.
- Keep API/data logic here (not inside transport server files).
"""

from __future__ import annotations

from typing import Any

import httpx

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "mcp-weather-lab/1.0 (student-lab@example.com)"


async def _request_json(url: str) -> dict[str, Any] | None:
    """Fetch JSON from Weather.gov with headers and basic error handling."""
    # TODO(Assignment 1):
    # 1) Add required headers (User-Agent, Accept).
    # 2) Perform GET with timeout.
    # 3) Return parsed JSON on success.
    # 4) Return None on failure.
    # TODO(Assignment 4): Add retry/backoff.
    _ = url
    return None


def _format_alert(feature: dict[str, Any]) -> str:
    """Format a single alert feature into readable text."""
    # TODO(Assignment 1): Format key alert fields into readable multiline text.
    _ = feature
    return "TODO: format alert"


async def get_alerts_for_state(state: str) -> str:
    """Return active alerts for a two-letter US state code."""
    # TODO(Assignment 1):
    # 1) Validate that state is a 2-letter code.
    # 2) Call /alerts/active/area/{state}.
    # 3) Return user-friendly messages for empty/error cases.
    # 4) Format alerts with _format_alert.
    return "TODO: implement get_alerts_for_state"


async def get_forecast_for_coordinates(latitude: float, longitude: float) -> str:
    """Return up to 5 forecast periods for US coordinates."""
    # TODO(Assignment 1):
    # 1) Call /points/{lat},{lon}.
    # 2) Read forecast URL from points response.
    # 3) Request forecast data.
    # 4) Format up to 5 periods.
    # 5) Return user-friendly empty/error messages.
    return "TODO: implement get_forecast_for_coordinates"
