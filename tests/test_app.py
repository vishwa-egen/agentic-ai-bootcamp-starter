from pathlib import Path

from streamlit.testing.v1 import AppTest

from bootcamp.agents import FRAMEWORKS

APP = str(Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py")


def test_app_loads_without_errors():
    app = AppTest.from_file(APP, default_timeout=60).run()
    assert not app.exception
    assert app.title[0].value == "Agentic AI Bootcamp"


def test_connection_checks_run():
    app = AppTest.from_file(APP, default_timeout=60).run()
    app.button(key="run_checks").click().run()
    assert not app.exception
    text = " ".join(box.value for box in app.success)
    assert "LLM endpoint" in text


def test_prompt_runs_and_is_judged():
    app = AppTest.from_file(APP, default_timeout=90).run()
    app.selectbox(key="framework").select(list(FRAMEWORKS)[-1]).run()
    app.button(key="run_prompt").click().run()
    assert not app.exception
    assert not app.error
    assert any("391" in block.value for block in app.markdown)
    assert any("relevance" in box.value for box in [*app.success, *app.warning])
