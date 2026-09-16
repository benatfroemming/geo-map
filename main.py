from pathlib import Path
from mcp.server.apps import Apps, ResourceCsp
from mcp.server.mcpserver import MCPServer

apps = Apps()

VIEW_URI = "ui://geojson/map.html"

@apps.tool(
    resource_uri=VIEW_URI,
    description="Create an interactive map visualizing the supplied GeoJSON data.",
)
def visualize_raw_geojson(geojson: str) -> str:
    """
    Visualize arbitrary GeoJSON (Feature, FeatureCollection, or Geometry).
    The UI renders points, lines and polygons and fits the map to the data.
    """
    return geojson

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