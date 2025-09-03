"""
Single-file Micro JSON Comparison Library to use in tests.

Compares two JSON objects (multiply nested dicts or lists) element by element
recursively, and returns a message describing the differences in a human-friendly way.

Stops on the first difference found.
"""

# spell-checker: words tracebackhide Marcin Konowalczyk lczyk

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import TypeAlias
else:
    TypeAlias = str  # type: ignore[assignment]


__version__ = "0.2.2"

__author__ = "Marcin Konowalczyk"

__all__ = ["compare_json"]

__changelog__ = [
    ("0.2.2", "simplify internals + nicer types in messages", "@lczyk"),
    ("0.2.1", "fix `_compare_json_lists` false positive", "@lczyk"),
    ("0.2.0", ("reduced and simplified interface to just `compare_json`"), "@lczyk"),
    ("0.1.5", "add `unordered` option", "@lczyk"),
    ("0.1.4", "add generic interface (`compare_json`)", "@lczyk"),
    ("0.1.3", "add json stack", "@lczyk"),
    ("0.1.2", "add recursive comparison and `compare_json_lists`", "@lczyk"),
    ("0.1.0", "initial version with `compare_json_dicts`", "@lczyk"),
]


def compare_json(
    expected: object,
    actual: object,
    *,
    raise_assertion: bool = True,
    unordered: bool = False,
) -> tuple[bool, str]:
    """Compare two JSON objects (dict or list) in a way which is friendly to the test output.
    Returns a tuple of (ok: bool, message: str)."""
    __tracebackhide__ = True
    msg, stack = _compare_json_values(expected, actual, unordered=unordered, stack=None)
    if msg:  # attach the stack
        msg = f"{msg}{'. At: ' + '.'.join(stack) if stack else ''}"
    if raise_assertion and msg:
        raise AssertionError(msg)
    if msg:
        return False, msg
    return True, ""


### Internal ###########################################################################################################

_Stack: TypeAlias = "list[str] | None"


def _compare_json_dicts(
    expected: dict[str, Any], actual: dict[str, Any], unordered: bool, stack: _Stack
) -> tuple[str, _Stack]:
    if not isinstance(expected, dict):
        return f"Expected a dictionary, got '{type(expected)}'", stack
    if not isinstance(actual, dict):
        return f"Expected a dictionary, got '{type(actual)}'", stack

    expected_keys = list(expected.keys())
    actual_keys = list(actual.keys())
    if unordered:
        expected_keys.sort()
        actual_keys.sort()
    if len(expected_keys) != len(actual_keys):
        return f"Key lengths do not match: expected {len(expected_keys)}, got {len(actual_keys)}", stack
    for key in expected_keys:
        stack = [*stack, key] if stack else [key]
        if key not in actual:
            return f"Key '{key}' not found in actual dictionary", stack
        expected_item = expected[key]
        actual_item = actual[key]
        msg, _stack = _compare_json_values(expected_item, actual_item, unordered=unordered, stack=stack)
        if msg:
            return msg, _stack
        stack.pop()
    return "", stack  # No differences found


def _compare_json_values(expected_value: Any, actual_value: Any, unordered: bool, stack: _Stack) -> tuple[str, _Stack]:
    expected_type = type(expected_value)
    actual_type = type(actual_value)
    if expected_type != actual_type:
        return f"Type mismatch: expected '{expected_type.__name__}', got '{actual_type.__name__}'", stack
    if expected_type is dict:
        return _compare_json_dicts(expected_value, actual_value, unordered=unordered, stack=stack)
    elif expected_type is list:
        return _compare_json_lists(expected_value, actual_value, unordered=unordered, stack=stack)
    elif expected_value != actual_value:
        return f"Value mismatch: expected '{expected_value}', got '{actual_value}'", stack
    return "", stack  # No differences found


def _compare_json_lists(expected: list[Any], actual: list[Any], unordered: bool, stack: _Stack) -> tuple[str, _Stack]:
    if not isinstance(expected, list):
        return f"Expected a list, got '{type(expected)}'", stack
    if not isinstance(actual, list):
        return f"Expected a list, got '{type(actual)}'", stack

    if len(expected) != len(actual):
        return f"List lengths do not match: {len(expected)} != {len(actual)}", stack

    if unordered:
        for i, expected_value in enumerate(expected):
            stack = [*stack, f"[{i}]"] if stack else [f"[{i}]"]
            # Find the actual value that matches the expected value
            # NOTE: This is expensive for large lists! For deeply nested lists we're doing *exponential* work here!
            index = -1
            for j, actual_value in enumerate(actual):
                msg, _ = _compare_json_values(expected_value, actual_value, unordered=unordered, stack=stack)
                if not msg:  # No difference found
                    index = j
                    break
            if index == -1:
                return f"Value '{expected_value}' not found in actual list", stack
            # Remove the found value from the actual list to avoid duplicates
            actual.pop(index)
            stack.pop()

    else:
        for i, (expected_value, actual_value) in enumerate(zip(expected, actual)):
            stack = [*stack, f"[{i}]"] if stack else [f"[{i}]"]
            msg, _stack = _compare_json_values(expected_value, actual_value, unordered=unordered, stack=stack)
            if msg:
                return msg, _stack
            stack.pop()
    return "", stack  # No differences found


__license__ = """
Copyright 2025 Marcin Konowalczyk

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
