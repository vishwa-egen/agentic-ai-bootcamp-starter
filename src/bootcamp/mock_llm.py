"""A tiny OpenAI-compatible server for tests and for trying the starter without a key.

It understands just enough of the Chat Completions API to exercise the code:
plain replies, tool calls for the two sample tools, and structured output for
the LLM-as-judge. It is not a model. Start it with `python -m bootcamp mock-llm`.
"""

from __future__ import annotations

import json
import re
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

MOCK_MODEL = "mock-model"
DEFAULT_PORT = 4010

# A run of digits, brackets and operators that holds at least one operator.
_ARITHMETIC = re.compile(r"[\d(][\d\s.()]*[-+*/%][\d\s.()+\-*/%]*[\d)]")


def _text(content: Any) -> str:
    """Message content may be a string or a list of content parts."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content if isinstance(part, dict))
    return ""


def _from_schema(schema: dict[str, Any]) -> Any:
    """Build the simplest value that satisfies a JSON schema."""
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if kind == "object":
        properties = schema.get("properties", {})
        return {name: _from_schema(sub) for name, sub in properties.items()}
    if kind == "array":
        return []
    if kind in ("number", "integer"):
        return 1
    if kind == "boolean":
        return True
    return "Mock judge: the answer addresses the question."


def _tool_call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"call_{uuid.uuid4().hex[:12]}",
        "type": "function",
        "function": {"name": name, "arguments": json.dumps(arguments)},
    }


def build_message(body: dict[str, Any]) -> dict[str, Any]:
    """Decide what the mock assistant says for one chat completion request."""
    messages = body.get("messages", [])
    tools = {
        t["function"]["name"]: t["function"] for t in body.get("tools") or [] if "function" in t
    }
    last_user = next(
        (_text(m.get("content")) for m in reversed(messages) if m.get("role") == "user"), ""
    )
    tool_results = [_text(m.get("content")) for m in messages if m.get("role") == "tool"]

    # 1. Structured output through a forced tool call (used by the judge).
    choice = body.get("tool_choice")
    if isinstance(choice, dict) and choice.get("function", {}).get("name") in tools:
        name = choice["function"]["name"]
        arguments = _from_schema(tools[name].get("parameters", {"type": "object"}))
        return {"role": "assistant", "content": None, "tool_calls": [_tool_call(name, arguments)]}

    # 2. Structured output through response_format.
    response_format = body.get("response_format") or {}
    if response_format.get("type") == "json_schema":
        schema = response_format.get("json_schema", {}).get("schema", {"type": "object"})
        return {"role": "assistant", "content": json.dumps(_from_schema(schema))}

    # 3. Call a sample tool once, when the question needs it.
    if not tool_results and choice != "none":
        lowered = last_user.lower()
        arithmetic = _ARITHMETIC.search(last_user)
        if "calculator" in tools and arithmetic:
            call = _tool_call("calculator", {"expression": arithmetic.group(0).strip()})
            return {"role": "assistant", "content": None, "tool_calls": [call]}
        if "get_current_time" in tools and "time" in lowered:
            call = _tool_call("get_current_time", {"timezone": "UTC"})
            return {"role": "assistant", "content": None, "tool_calls": [call]}

    # 4. Final answer.
    if tool_results:
        return {"role": "assistant", "content": f"[mock] The tool returned: {tool_results[-1]}"}
    if "pong" in last_user.lower():
        return {"role": "assistant", "content": "pong"}
    return {"role": "assistant", "content": f"[mock] You said: {last_user[:200]}"}


def build_completion(body: dict[str, Any]) -> dict[str, Any]:
    message = build_message(body)
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:16]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": body.get("model", MOCK_MODEL),
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": "tool_calls" if message.get("tool_calls") else "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
    }


def _as_stream(completion: dict[str, Any]) -> list[dict[str, Any]]:
    """Turn one completion into the chunks a streaming client expects."""
    choice = completion["choices"][0]
    message = choice["message"]
    delta: dict[str, Any] = {"role": "assistant", "content": message.get("content")}
    if message.get("tool_calls"):
        delta["tool_calls"] = [{"index": i, **call} for i, call in enumerate(message["tool_calls"])]
    base = {k: completion[k] for k in ("id", "created", "model")} | {
        "object": "chat.completion.chunk"
    }
    return [
        base | {"choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
        base | {"choices": [{"index": 0, "delta": {}, "finish_reason": choice["finish_reason"]}]},
    ]


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_: Any) -> None:  # keep test output quiet
        return

    def _send_json(self, payload: Any, status: int = 200) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802 - name required by http.server
        if self.path.rstrip("/").endswith("/models"):
            self._send_json({"object": "list", "data": [{"id": MOCK_MODEL, "object": "model"}]})
        else:
            self._send_json({"status": "ok", "server": "bootcamp mock LLM"})

    def do_POST(self) -> None:  # noqa: N802 - name required by http.server
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        if not self.path.rstrip("/").endswith("/chat/completions"):
            self._send_json({"error": {"message": f"mock LLM does not support {self.path}"}}, 404)
            return
        completion = build_completion(body)
        if not body.get("stream"):
            self._send_json(completion)
            return
        chunks = "".join(f"data: {json.dumps(chunk)}\n\n" for chunk in _as_stream(completion))
        data = (chunks + "data: [DONE]\n\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def start_mock_server(port: int = 0, host: str = "127.0.0.1") -> tuple[ThreadingHTTPServer, str]:
    """Start the mock in a background thread. Returns the server and its base URL."""
    server = ThreadingHTTPServer((host, port), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://{host}:{server.server_address[1]}/v1"


def serve_forever(port: int = DEFAULT_PORT) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    print(f"Mock LLM running at http://127.0.0.1:{port}/v1  (Ctrl+C to stop)")
    print("Put these lines in .env to use it:")
    print(f"  OPENAI_BASE_URL=http://127.0.0.1:{port}/v1")
    print("  OPENAI_API_KEY=mock-key")
    print(f"  OPENAI_MODEL={MOCK_MODEL}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMock LLM stopped.")
