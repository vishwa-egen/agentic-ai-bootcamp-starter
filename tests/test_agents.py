import pytest

from bootcamp.agents import FRAMEWORKS, run_agent


@pytest.mark.parametrize("framework", list(FRAMEWORKS))
def test_each_framework_answers_and_calls_a_tool(framework, settings):
    result = run_agent(framework, "What is 17 * 23?", settings)
    assert "391" in result.text
    assert [call.name for call in result.tool_calls] == ["calculator"]
    assert result.framework == FRAMEWORKS[framework][0]
    assert result.latency_seconds > 0


@pytest.mark.parametrize("framework", list(FRAMEWORKS))
def test_each_framework_answers_without_tools(framework, settings):
    result = run_agent(framework, "Say hello", settings)
    assert result.text and not result.tool_calls


def test_unknown_framework_is_rejected(settings):
    with pytest.raises(ValueError, match="Unknown framework"):
        run_agent("not-a-framework", "hi", settings)
