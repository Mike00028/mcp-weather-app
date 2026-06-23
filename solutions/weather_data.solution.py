"""Weather.gov data layer used by MCP server tools.

This module keeps API access separate from transport/server concerns.
"""

from __future__ import annotations

from typing import Any

import httpx

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "mcp-weather-lab/1.0 (student-lab@example.com)"


async def _request_json(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def _format_alert(feature: dict[str, Any]) -> str:
    props = feature.get("properties", {})
    return "\n".join(
        [
            f"Event: {props.get('event', 'Unknown')}",
            f"Area: {props.get('areaDesc', 'Unknown')}",
            f"Severity: {props.get('severity', 'Unknown')}",
            f"Status: {props.get('status', 'Unknown')}",
            f"Headline: {props.get('headline', 'No headline')}",
            f"Description: {props.get('description', 'No description')}",
        ]
    )


async def get_alerts_for_state(state: str) -> str:
    """Return active alerts for a two-letter US state code."""
    state_code = state.strip().upper()
    if len(state_code) != 2:
        return "State must be a 2-letter US code, for example CA or NY."

    url = f"{NWS_API_BASE}/alerts/active/area/{state_code}"
    data = await _request_json(url)
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    features = data.get("features", [])
    if not features:
        return f"No active alerts for {state_code}."

    return "\n---\n".join(_format_alert(feature) for feature in features)


async def get_forecast_for_coordinates(latitude: float, longitude: float) -> str:
    """Return up to 5 forecast periods for US coordinates."""
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await _request_json(points_url)
    if not points_data:
        return "Unable to fetch point data for this location."

    forecast_url = points_data.get("properties", {}).get("forecast")
    if not forecast_url:
        return "Forecast URL missing from point data."

    forecast_data = await _request_json(forecast_url)
    if not forecast_data:
        return "Unable to fetch forecast data."

    periods = forecast_data.get("properties", {}).get("periods", [])
    if not periods:
        return "No forecast periods available."

    lines: list[str] = []
    for period in periods[:5]:
        lines.append(
            "\n".join(
                [
                    f"{period.get('name', 'Unknown')}",
                    f"Temperature: {period.get('temperature', 'Unknown')} {period.get('temperatureUnit', '')}",
                    f"Wind: {period.get('windSpeed', 'Unknown')} {period.get('windDirection', '')}",
                    f"Forecast: {period.get('detailedForecast', 'No forecast')}",
                ]
            )
        )

    return "\n---\n".join(lines)
