from refactored_code import InputHandler
from pytest import MonkeyPatch


def test_int_input(monkeypatch: MonkeyPatch):
    inputs = ["string", 1]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    assert InputHandler.int_input(message="", header="") == 1


def test_str_input(monkeypatch: MonkeyPatch):
    inputs = ["string", 1]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    assert InputHandler.str_input(message="", header="") == "string"



