# Notes MCP Server

A Model Context Protocol (MCP) server for managing notes with full CRUD (Create, Read, Update, Delete) operations. This server allows AI assistants and MCP-compatible applications to create, retrieve, list, and delete notes stored as JSON data.

## Features

-   **Create Notes**: Add new notes with title and optional content
-   **List Notes**: Retrieve all stored notes
-   **Get Note**: Fetch a specific note by its unique ID
-   **Delete Notes**: Remove notes by their ID
-   **Persistent Storage**: Notes are stored in a JSON file for persistence across sessions
-   **Multiple Transport Options**: Supports stdio, HTTP, and SSE transports
-   **Configurable**: Environment variable configuration for flexibility

## Installation

1. **Clone or download this repository**
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The server can be configured using environment variables. Create a `.env` file in the project root:

```bash
# Server Configuration
SERVER_NAME=notes-server
SERVER_VERSION=1.0.0
NOTES_DIR=./data

# Transport Configuration (stdio, http, sse)
SERVER_TRANSPORT=stdio
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

### Configuration Options

| Variable           | Default        | Description                               |
| ------------------ | -------------- | ----------------------------------------- |
| `SERVER_NAME`      | `notes-server` | Name of the MCP server                    |
| `SERVER_VERSION`   | `1.0.0`        | Version of the server                     |
| `NOTES_DIR`        | `./data`       | Directory where notes.json will be stored |
| `SERVER_TRANSPORT` | `stdio`        | Transport method (`stdio`, `http`, `sse`) |
| `SERVER_HOST`      | `127.0.0.1`    | Host for HTTP/SSE transport               |
| `SERVER_PORT`      | `8000`         | Port for HTTP/SSE transport               |

## Usage

### Running the Server

#### Option 1: stdio (Default - for MCP clients)

```bash
python server.py
```

#### Option 2: HTTP Transport

```bash
SERVER_TRANSPORT=http python server.py
```

#### Option 3: SSE Transport

```bash
SERVER_TRANSPORT=sse python server.py
```

### MCP Client Configuration

To use this server with MCP-compatible applications (like Claude Desktop, GitHub Copilot, etc.), add it to your MCP client configuration.

#### Example for Claude Desktop (`claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "notes-server": {
            "command": "python",
            "args": ["/path/to/your/notes-mcp-server/server.py"],
            "env": {
                "SERVER_NAME": "notes-server"
            }
        }
    }
}
```

#### Example for VS Code with MCP extension:

```json
{
    "mcp.servers": {
        "notes-server": {
            "command": "python",
            "args": ["/path/to/your/notes-mcp-server/server.py"]
        }
    }
}
```

## Available Tools

The server exposes the following MCP tools:

### `create_note`

Creates a new note with a title and optional content.

**Parameters:**

-   `title` (string, required): The title of the note
-   `content` (string, optional): The content/body of the note

**Returns:** The created note object with generated ID and timestamps

### `list_notes`

Retrieves all stored notes.

**Parameters:** None

**Returns:** Array of all note objects

### `get_note`

Fetches a specific note by its ID.

**Parameters:**

-   `note_id` (string, required): The unique identifier of the note

**Returns:** The note object or error message if not found

### `delete_note`

Removes a note by its ID.

**Parameters:**

-   `note_id` (string, required): The unique identifier of the note to delete

**Returns:** Success confirmation or error message if not found

## Data Structure

Notes are stored with the following structure:

```json
{
    "id": "abc123def456",
    "title": "My Note Title",
    "content": "Note content goes here...",
    "createdAt": "2024-01-01T12:00:00.000Z",
    "updatedAt": "2024-01-01T12:00:00.000Z"
}
```

### Fields

-   `id`: Unique 16-character hexadecimal identifier
-   `title`: User-provided title for the note
-   `content`: User-provided content/body of the note
-   `createdAt`: ISO timestamp of when the note was created
-   `updatedAt`: ISO timestamp of when the note was last modified

## File Structure

```
notes-mcp-server/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
├── data/
│   └── notes.json     # Notes storage file (auto-created)
├── .env               # Environment configuration (optional)
└── README.md          # This file
```

## Dependencies

-   **fastmcp**: Framework for building MCP servers
-   **python-dotenv**: Environment variable management

## Transport Modes

### stdio (Default)

Perfect for MCP clients like Claude Desktop, GitHub Copilot, and other AI assistants. The server communicates via standard input/output.

### HTTP

Exposes the MCP server over HTTP at `http://HOST:PORT/mcp`. Useful for web-based integrations.

### SSE (Server-Sent Events)

Provides real-time communication via Server-Sent Events at `http://HOST:PORT`. Good for streaming applications.

## Error Handling

The server includes robust error handling:

-   **File Management**: Automatically creates the data directory and notes.json if they don't exist
-   **Note Not Found**: Returns appropriate error messages when attempting to access non-existent notes
-   **Invalid Transport**: Validates transport configuration and provides clear error messages

## Example Usage with MCP Client

Once configured with an MCP client, you can use natural language to interact with your notes:

-   "Create a new note titled 'Shopping List' with content 'milk, eggs, bread'"
-   "Show me all my notes"
-   "Get the note with ID abc123def456"
-   "Delete the note about shopping"
-   "List all notes created today"

## Development

To extend or modify the server:

1. **Add new tools**: Define new functions with the `@mcp.tool()` decorator
2. **Modify data structure**: Update the `_new_note()` function and JSON schema
3. **Add validation**: Implement parameter validation in the tool functions
4. **Enhance storage**: Replace JSON file storage with a database

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Support

For issues or questions about this MCP server, please check the FastMCP documentation or create an issue in the project repository.
