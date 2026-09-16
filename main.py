import json
from pathlib import Path

import requests
from mcp.server.apps import Apps, ResourceCsp
from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult, TextContent

apps = Apps()

VIEW_URI = "ui://geojson/map.html"


@apps.tool(
    resource_uri=VIEW_URI,
    description="Create an interactive map visualizing the supplied GeoJSON data.",
)
def visualize_raw_geojson(geojson: str) -> CallToolResult:
    """
    Visualize arbitrary GeoJSON (Feature, FeatureCollection, or Geometry).
    The UI renders points, lines and polygons and fits the map to the data.
    """
    try:
        parsed = json.loads(geojson) if isinstance(geojson, str) else geojson
    except json.JSONDecodeError as e:
        return CallToolResult(content=[TextContent(type="text", text=f"Invalid GeoJSON: {e}")])

    # Invalid geojson, alert agent
    if not isinstance(parsed, dict) or "type" not in parsed:
        return CallToolResult(content=[TextContent(type="text", text="Not valid GeoJSON (missing top-level 'type').")])

    feature_count = len(parsed.get("features", [parsed]))
    return CallToolResult(
        content=[TextContent(type="text", text=f"Rendered a map with {feature_count} feature(s).")], # response for the agent
        structuredContent=parsed, # full geojson used in the map
    )


@apps.tool(
    resource_uri=VIEW_URI,
    description="Create an interactive map visualizing the GeoJSON data from the supplied url.",
)
def visualize_url_geojson(url: str) -> CallToolResult:
    """
    Fetches GeoJSON from a URL and visualizes it (Feature, FeatureCollection, or Geometry).
    The UI renders points, lines and polygons and fits the map to the data.
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        geojson = resp.json()
    except Exception as e:
        return CallToolResult(content=[TextContent(type="text", text=f"Error fetching GeoJSON: {e}")])

    # Invalid geojson, alert agent
    if not isinstance(geojson, dict) or "type" not in geojson:
        return CallToolResult(content=[TextContent(type="text", text="Fetched content is not valid GeoJSON (missing top-level 'type').")])

    feature_count = len(geojson.get("features", [geojson]))
    return CallToolResult(
        content=[TextContent(type="text", text=f"Rendered a map with {feature_count} feature(s) from {url}.")], # response for the agent
        structuredContent=geojson, # full geojson used in the map
    )


html = Path(__file__).parent.joinpath("map.html").read_text(encoding="utf-8")

apps.add_html_resource(
    VIEW_URI,
    html,
    title="GeoJSON Map",
    csp=ResourceCsp(
        resource_domains=[
            "https://unpkg.com",
            "https://tiles.openfreemap.org",
            "https://*.openfreemap.org",
        ],
        connect_domains=[
            "https://unpkg.com",
            "https://tiles.openfreemap.org",
            "https://*.openfreemap.org",
        ],
    ),
)

mcp = MCPServer("Map", extensions=[apps])

if __name__ == "__main__":
    mcp.run()