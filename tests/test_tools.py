from bootcamp.tools import calculator, get_current_time, record_tool_calls


def test_calculator_handles_arithmetic():
    assert calculator("17 * 23") == "391"
    assert calculator("(125 + 75) / 8") == "25"
    assert calculator("2 ** 10") == "1024"


def test_calculator_rejects_code():
    assert "Could not evaluate" in calculator("__import__('os').system('echo hi')")
    assert "Could not evaluate" in calculator("1 / 0")


def test_current_time_knows_timezones():
    assert get_current_time("UTC").endswith("UTC")
    assert "Unknown timezone" in get_current_time("Not/AZone")


def test_tool_calls_are_recorded():
    with record_tool_calls() as calls:
        calculator(expression="1 + 1")
    assert calls == [{"name": "calculator", "arguments": {"expression": "1 + 1"}, "result": "2"}]


def test_calculator_reports_a_result_too_large_to_show():
    assert "Could not evaluate" in calculator("(10 ** 100) ** 50")
