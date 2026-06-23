# MCP Weather Lab

Hands-on lab for learning MCP servers, transport protocols, and data-layer design using the National Weather Service API: https://api.weather.gov/

## Learning goals

1. Build MCP tools that call external APIs.
2. Understand STDIO vs Streamable HTTP transport.
3. Separate server transport logic from data-layer code.
4. Connect an MCP client to your server.
5. Add resilience for production-style behavior.

## Required Weather Tools (Core Scope)

To avoid confusion, the required MCP weather tool set is exactly two tools:

1. get_alerts(state: str)
2. get_forecast(latitude: float, longitude: float)

Students can be creative with output format and implementation details, but these two tools must exist and be functional in both transports.

## Folder layout

- stdio_srv.py: MCP server over stdio transport.
- http_srv.py: MCP server over streamable HTTP transport.
- src/weather_data.py: shared Weather.gov data layer.
- gemini_client.py: optional Gemini + LangChain MCP client.
- solutions/: reference implementations (use only after attempting assignments).
- requirements.txt: lab dependencies.
- .env.example: environment variable template.

## Starter vs Solution

1. The main files in this folder are student starter files with TODO markers.
2. Full reference implementations are in the solutions folder.
3. Recommended flow: attempt assignments first, then compare with solutions if blocked.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies: pip install -r requirements.txt
3. Copy .env.example to .env and set values if needed.

Windows PowerShell example:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Run

### Start STDIO server

```bash
python stdio_srv.py
```

Note: The stdio server is normally launched by an MCP client process. Running it directly is useful only for smoke checks.

### Start HTTP server

```bash
python http_srv.py
```

Default HTTP endpoint is http://127.0.0.1:8000/mcp

### Run optional Gemini client exercise

```bash
python gemini_client.py
```

To use HTTP mode in the client, set:

- MCP_CLIENT_MODE=http
- MCP_HTTP_URL=http://127.0.0.1:8000/mcp

PowerShell example:

```powershell
$env:MCP_CLIENT_MODE="http"
$env:MCP_HTTP_URL="http://127.0.0.1:8000/mcp"
python gemini_client.py
```

## Assignments

Implement assignments in these starter files only:

1. src/weather_data.py
2. stdio_srv.py
3. http_srv.py
4. gemini_client.py

### Assignment 1: Data Layer Implementation (src/weather_data.py)

Goal: implement all Weather.gov API logic in one shared place.

What to do in this file:
1. Implement _request_json(url) with headers, timeout, and error handling.
2. Implement _format_alert(feature) into readable multiline output.
3. Implement get_alerts_for_state(state):
	- validate 2-letter state code,
	- call /alerts/active/area/{state},
	- return user-friendly messages for no data/errors.
4. Implement get_forecast_for_coordinates(latitude, longitude):
	- call /points/{lat},{lon},
	- read forecast URL,
	- fetch forecast periods,
	- return up to 5 periods with readable formatting.

Deliverable:
- A working src/weather_data.py that returns useful text for both required tools.

Success criteria:
- No transport-specific code here.
- Functions return stable output for valid and invalid input.

### Assignment 2: STDIO MCP Wiring (stdio_srv.py)

Goal: expose the two required tools over stdio transport.

What to do in this file:
1. Wire get_alerts tool to call get_alerts_for_state.
2. Wire get_forecast tool to call get_forecast_for_coordinates.
3. Keep logging on stderr only.
4. Keep mcp.run(transport="stdio") in main().

Deliverable:
- A working stdio server with both required tools.

Success criteria:
- Tool names and signatures match required scope.
- No Weather.gov request logic duplicated here.

### Assignment 3: HTTP MCP Wiring (http_srv.py)

Goal: expose the same two tools over streamable HTTP transport.

What to do in this file:
1. Wire get_alerts tool to call get_alerts_for_state.
2. Wire get_forecast tool to call get_forecast_for_coordinates.
3. Ensure behavior/output is consistent with stdio server.
4. Run with streamable HTTP transport.

Deliverable:
- A working HTTP server with both required tools.

Success criteria:
- Same tool behavior as stdio server.
- No Weather.gov request logic duplicated here.

### Assignment 4: Client Validation Flow (gemini_client.py)

Goal: use client-side checks to verify your server tools in both transports.

What to do in this file:
1. Keep stdio and http client modes functional.
2. Confirm tool discovery works in both modes.
3. Use Gemini mode only after tool discovery succeeds.
4. Update prompt text so it demonstrates both required weather tools.

Deliverable:
- A client script that can validate tools in stdio and HTTP modes.

Success criteria:
- Tools are listed in both modes.
- Gemini call (if key is set) produces weather-related output.

### Assignment 5: Reliability Pass (src/weather_data.py)

Goal: make upstream API calls more resilient.

What to do in this file:
1. Add retry with backoff for transient failures.
2. Improve timeout/error messaging.
3. Keep output user-friendly when Weather.gov fails.

Deliverable:
- Improved resilience behavior in src/weather_data.py.

Success criteria:
- Retry behavior is visible in code.
- Failures do not crash server tools.

### Assignment 6: Extra Practice - Separate File Inspector Server

Goal: practice stdio MCP with strict local file access boundaries.

What to build:
1. Create a new file: file_inspector_stdio_server.py.
2. Add tool 1: list file names in configured folder.
3. Add tool 2: list file sizes for files in configured folder.
4. Folder path must be set in server config only (not client input).
5. Log to stderr only.

Deliverable:
- A separate working stdio MCP file-inspector server.

Success criteria:
- Folder boundary enforced on server side.
- Tools return both file names and sizes clearly.

## Troubleshooting

### 1) ModuleNotFoundError or import errors

Symptom:
- Running a server or client fails with missing package errors.

Fix:
1. Ensure the venv is activated.
2. Reinstall dependencies with pip install -r requirements.txt.
3. Confirm python and pip point to the same environment.

### 2) HTTP MCP server unreachable

Symptom:
- Client cannot connect to http://127.0.0.1:8000/mcp.

Fix:
1. Start http_srv.py first.
2. Confirm MCP_PORT and MCP_PATH values.
3. Check for port conflicts and change MCP_PORT if needed.

### 3) No tools discovered in client

Symptom:
- Client prints no tools or fails during discovery.

Fix:
1. For stdio mode, run client from this folder so it can launch stdio_srv.py.
2. For http mode, verify MCP_HTTP_URL exactly matches the server endpoint.
3. Check server logs for startup failures.

### 4) Gemini key not detected

Symptom:
- Client says no Gemini key set.

Fix:
1. Set GEMINI_API_KEY or GOOGLE_API_KEY in .env.
2. Restart terminal or rerun process after updating environment.
3. Verify there are no extra quotes or spaces in key values.

### 5) Weather.gov errors or empty responses

Symptom:
- Alerts/forecast return no data or request failures.

Fix:
1. Use valid US state codes and US coordinates.
2. Retry after a short delay; transient issues can happen.
3. Verify outbound internet access from your environment.

### 6) STDIO server behaves strangely

Symptom:
- JSON-RPC parsing errors or unstable client-server interaction.

Fix:
1. Do not print to stdout in stdio server code.
2. Use stderr for logs.
3. Keep tool return values as structured text only.

## Suggested grading rubric

1. Correctness of MCP tools and schemas: 30%
2. Transport understanding and comparison quality: 20%
3. Data-layer design and reuse: 25%
4. Error handling and resilience: 20%
5. Documentation and maintainability: 5%
