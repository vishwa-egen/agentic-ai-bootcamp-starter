from bootcamp.agents import FRAMEWORKS
from bootcamp.cli import main
from bootcamp.config import Settings
from bootcamp.doctor import check_arize, check_llm, format_checks, run_checks


def test_offline_checks_pass_in_this_environment():
    checks = run_checks(network=False)
    by_name = {check.name: check for check in checks}
    assert by_name["Python version"].status == "ok"
    for label, _module in FRAMEWORKS.values():
        assert by_name[label].status == "ok"


def test_llm_check_passes_against_the_endpoint(settings):
    check = check_llm(settings)
    assert check.status == "ok"
    assert "mock-key-for-tests" not in check.detail


def test_llm_check_explains_missing_values(monkeypatch):
    monkeypatch.setenv("OPENAI_MODEL", "")
    check = check_llm(Settings(_env_file=None))
    assert check.status == "fail" and "OPENAI_MODEL" in check.detail


def test_arize_is_a_warning_when_not_configured(settings):
    assert check_arize(settings).status == "warn"


def test_report_is_plain_text(settings):
    report = format_checks(run_checks(settings))
    assert "[ OK ] LLM endpoint" in report


def test_cli_ask_prints_the_answer(capsys):
    assert main(["ask", "What is 17 * 23?", "--framework", list(FRAMEWORKS)[-1]]) == 0
    assert "391" in capsys.readouterr().out


def test_packages_of_a_removed_framework_are_not_required(monkeypatch):
    from bootcamp import agents
    from bootcamp.doctor import check_packages

    kept = dict(list(agents.FRAMEWORKS.items())[:1])
    monkeypatch.setattr(agents, "FRAMEWORKS", kept)
    names = {check.name for check in check_packages()}
    removed = {label for key, (label, _) in FRAMEWORKS.items() if key not in kept}
    assert not names & removed
    assert {"Arize tracing (arize-otel)", "Arize Phoenix evals"} <= names
