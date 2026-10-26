import pytest
from elastic_security_intel_connector.config_variables import ConfigConnector


@pytest.fixture(autouse=True)
def no_config_file(monkeypatch):
    monkeypatch.setattr(ConfigConnector, "_load_config", staticmethod(lambda: {}))


def test_default_score_should_be_50_when_not_configured(monkeypatch):
    monkeypatch.delenv("ELASTIC_SECURITY_DEFAULT_SCORE", raising=False)

    config = ConfigConnector()

    assert config.default_score == 50


def test_default_score_should_be_read_from_environment(monkeypatch):
    monkeypatch.setenv("ELASTIC_SECURITY_DEFAULT_SCORE", "20")

    config = ConfigConnector()

    assert config.default_score == 20


@pytest.mark.parametrize("value", ["-1", "101"])
def test_default_score_should_be_rejected_when_out_of_range(monkeypatch, value):
    monkeypatch.setenv("ELASTIC_SECURITY_DEFAULT_SCORE", value)

    with pytest.raises(ValueError, match="ELASTIC_SECURITY_DEFAULT_SCORE"):
        ConfigConnector()
