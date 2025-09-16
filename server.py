from dotenv import load_dotenv
import os
import json
from pathlib import Path
from fastmcp import FastMCP
from datetime import datetime, timezone
from secrets import token_hex

load_dotenv()

# Variable from .env file
SERVER_NAME = os.getenv("SERVER_NAME", "notes-server")
SERVER_VERSION = os.getenv("SERVER_VERSION", "1.0.0")
NOTES_DIR = Path(os.getenv("NOTES_DIR", "./data"))

TRANSPORT = os.getenv("SERVER_TRANSPORT", "stdio").lower()
HOST = os.getenv("SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("SERVER_PORT", "8000"))

NOTES_FILE = NOTES_DIR / "notes.json"

# Initialize mcp
mcp = FastMCP(SERVER_NAME, version=SERVER_VERSION)

# Helper functions
def _ensure_file():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    if not NOTES_FILE.exists():
        NOTES_FILE.write_text(json.dumps({"notes": []}, indent=2), encoding="utf-8")


def _load_notes() -> list[dict]:
    _ensure_file()
    return json.loads(NOTES_FILE.read_text(encoding="utf-8"))["notes"]


def _save_notes(notes: list[dict]):
    _ensure_file()
    NOTES_FILE.write_text(json.dumps({"notes": notes}, indent=2), encoding="utf-8")

def _new_note(title: str, content: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "id": token_hex(8),
        "title": title,
        "content": content,
        "createdAt": now,
        "updatedAt": now,
    }


@mcp.tool()
def create_note(title: str, content: str = "") -> dict:
    """Create a new note with the given title and content."""
    notes = _load_notes()
    note = _new_note(title, content)
    notes.append(note)
    _save_notes(notes)
    return note  # ✅ return dict directly


@mcp.tool()
def list_notes() -> list[dict]:
    """List all notes."""
    notes = _load_notes()
    return notes  # ✅ return list[dict] directly


@mcp.tool()
def get_note(note_id: str) -> dict:
    """Get a note by its ID."""
    notes = _load_notes()
    for note in notes:
        if note["id"] == note_id:
            return note  # ✅ return dict directly
    return {"error": f"Note with ID {note_id} not found."}  # ✅ consistent dict

@mcp.tool()
def delete_note(note_id: str) -> dict:
    """Delete a note by its ID."""
    notes = _load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[i]
            _save_notes(notes)
            return {"success": True}  # ✅ consistent dict
    return {"error": f"Note with ID {note_id} not found."}  # ✅ consistent dict

if __name__ == "__main__":
    transport = os.getenv("SERVER_TRANSPORT", "stdio").lower()

    if transport in ("stdio", "", None):
        # default for MCP clients (Copilot, Claude, etc.)
        mcp.run()  # same as app.run(transport="stdio")
    elif transport in ("http", "streamable-http"):
        mcp.run(transport="http", host=HOST, port=PORT, path="/mcp")
        # If your FastMCP complains about "http", try:
        # app.run(transport="streamable-http", host=HOST, port=PORT, path="/mcp")
    elif transport == "sse":
        mcp.run(transport="sse", host=HOST, port=PORT)
    else:
        raise ValueError(f"Unknown SERVER_TRANSPORT: {transport}")
