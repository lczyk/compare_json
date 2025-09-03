from compare_json import compare_json
from compare_json.compare_json import _compare_json_values as _compare_json


def test_compare_json_functionality() -> None:
    # Example test to check if the compare_json function works as expected
    json1 = {"key": "value"}
    json2 = {"key": "value"}

    ok, message = compare_json(json1, json2)

    assert ok
    assert message == ""


def test_compare_json_different_types() -> None:
    # Test comparing different types
    json1 = {"key": "value"}
    json2 = ["value"]

    ok, message = compare_json(json1, json2, raise_assertion=False)

    assert not ok
    assert "Type mismatch: expected 'dict', got 'list'" in message


def test_compare_json_unordered_lists() -> None:
    # Test comparing unordered lists
    json1 = {"key": [1, 2, 3]}
    json2 = {"key": [3, 2, 1]}

    ok, _message = compare_json(json1, json2, raise_assertion=False, unordered=False)
    assert not ok
    ok, _message = compare_json(json1, json2, raise_assertion=False, unordered=True)
    assert ok


def test_compare_json_nested_structures() -> None:
    # Test comparing nested structures
    json1 = {"a": {"b": {"c": "d"}}}
    json2 = {"a": {"b": {"c": "d"}}}

    ok, message = compare_json(json1, json2)
    assert ok, f"Comparison failed for nested structures: {message}"

    json3 = {"a": {"b": {"c": "not d"}}}

    ok, message = compare_json(json1, json3, raise_assertion=False)
    assert not ok
    assert "Value mismatch" in message


def test_json_stack() -> None:
    # Test that a stack trace is provided on failure
    json1 = {"key": "value"}
    json2 = {"key": "different_value"}

    msg, stack = _compare_json(json1, json2, False, None)
    assert "Value mismatch" in msg
    assert stack == ["key"]


def test_json_stack_deep() -> None:
    # Test that a stack trace is provided for deep nested structures
    json1 = {"a": {"b": {"c": "value"}}}
    json2 = {"a": {"b": {"c": "different_value"}}}

    msg, stack = _compare_json(json1, json2, False, None)
    assert "Value mismatch" in msg
    assert stack == ["a", "b", "c"]


def test_json_stack_list() -> None:
    # Test that a stack trace is provided for lists
    json1 = {"key": ["value1", "value2"]}
    json2 = {"key": ["value1", "different_value"]}

    msg, stack = _compare_json(json1, json2, False, None)
    assert "Value mismatch" in msg
    assert stack == ["key", 1]
