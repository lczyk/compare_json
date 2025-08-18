from compare_json import compare_json


def test_compare_json_functionality() -> None:
    # Example test to check if the compare_json function works as expected
    json1 = {"key": "value"}
    json2 = {"key": "value"}

    ok, message = compare_json(json1, json2)

    assert ok, f"Comparison failed: {message}"
