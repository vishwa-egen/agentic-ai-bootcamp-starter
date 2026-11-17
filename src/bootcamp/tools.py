"""Sample tools shared by all three framework starters.

These two tools exist only to prove that tool calling works end to end.
Replace them with the tools your capstone needs. A tool is a plain Python
function with type hints and a docstring: every framework here accepts that.
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from functools import wraps
from typing import Annotated, Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# ---- Tool-call recorder -------------------------------------------------
# Each agent run collects the tool calls it made, whatever the framework.

_recorded: ContextVar[list[dict[str, Any]] | None] = ContextVar("bootcamp_tool_calls", default=None)


@contextmanager
def record_tool_calls() -> Iterator[list[dict[str, Any]]]:
    """Collect tool calls made inside the `with` block."""
    calls: list[dict[str, Any]] = []
    token = _recorded.set(calls)
    try:
        yield calls
    finally:
        _recorded.reset(token)


def recorded(func: Callable[..., str]) -> Callable[..., str]:
    """Decorator that logs a tool call to the current recorder."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        calls = _recorded.get()
        if calls is not None:
            calls.append(
                {"name": func.__name__, "arguments": kwargs or list(args), "result": result}
            )
        return result

    return wrapper


# ---- Sample tools -------------------------------------------------------


@recorded
def get_current_time(
    timezone: Annotated[str, "IANA timezone name, for example UTC or America/Chicago"] = "UTC",
) -> str:
    """Return the current date and time in the given timezone."""
    try:
        zone = ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError):
        return f"Unknown timezone '{timezone}'. Use an IANA name such as UTC or America/Chicago."
    return datetime.now(zone).strftime("%Y-%m-%d %H:%M:%S %Z")


_OPERATORS: dict[type, Callable[..., float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return _OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("only numbers and + - * / // % ** ( ) are allowed")


@recorded
def calculator(
    expression: Annotated[str, "Arithmetic expression, for example (17 * 23) + 4"],
) -> str:
    """Evaluate an arithmetic expression and return the result."""
    try:
        value = _evaluate(ast.parse(expression.strip(), mode="eval").body)
        # str() of a huge integer raises ValueError, so it stays inside the try.
        return str(int(value) if isinstance(value, float) and value.is_integer() else value)
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as exc:
        return f"Could not evaluate '{expression}': {exc}"


#: The tools every starter agent receives. Add your capstone tools here.
SAMPLE_TOOLS: list[Callable[..., str]] = [get_current_time, calculator]
