# GeoJSON Map Visualizer MCP App

Visualize GeoJSON data directly in Claude Desktop. Ask Claude to map information it finds or generates, and see it rendered on an interactive map.

## Requirements

- Python 3.10+
- Claude Desktop (macOS, Windows, or Linux)
- Git

## Set up and use MCP on Claude Desktop

### 1. Download and set up

```bash
git clone https://github.com/benatfroemming/geo-mcp.git
cd geo-mcp
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get the path to your venv's Python

```bash
which python      # Windows: where python
```

Copy the full path it prints, e.g. `/Users/yourname/geo-mcp/.venv/bin/python` (macOS/Linux) or `C:\Users\yourname\geo-mcp\.venv\Scripts\python.exe` (Windows).

### 3. Edit the Claude Desktop config

Open the config file for your platform:

| Platform | Config path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

On macOS, you can open it directly with:

```bash
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add your server under `mcpServers`, using the full absolute paths for both the Python binary and `main.py` from step 2:

```json
{
  "mcpServers": {
    "Map": {
      "command": "/Users/yourname/geo-mcp/.venv/bin/python",
      "args": [
        "/Users/yourname/geo-mcp/main.py"
      ]
    }
  }
}
```

> **Note:** If the file already has other entries under `mcpServers`, merge this in as an additional key rather than replacing the whole file.

### 4. Restart Claude Desktop

Fully quit the app (⌘Q on macOS) and reopen it. Go to **Settings → Connectors** to verify you see `Map` listed as connected, with the type **Desktop** and permission set to **Always Allow**.

### 5. Ask Claude

Ask Claude to visualize GeoJSON data, or to map information it can search for online. For example:

> "Show me a map of national parks in California"
> "Plot the boundary of Yellowstone National Park"
> "Map the top 5 largest cities in Brazil"

Mapping local GeoJSON files is coming soon.