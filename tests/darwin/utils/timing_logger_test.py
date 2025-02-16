import pytest
import logging
from rich.console import Console
from time import sleep
from darwin.utils.timing_logger import MaybeConsole

@pytest.fixture
def logger():
    return logging.getLogger("test_logger")

@pytest.fixture
def console():
    return Console()

def test_maybe_console_with_console(logger, console, capfd):
    printer = MaybeConsole(logger, console)
    printer("Test message")
    
    # Check if output contains timing and message
    captured = capfd.readouterr()
    assert "seconds elapsed" in captured.out
    assert "Test message" in captured.out

def test_maybe_console_with_logger(logger, caplog):
    printer = MaybeConsole(logger)
    with caplog.at_level(logging.INFO):
        printer("Test message")
    
    # Check if log contains timing and message
    assert any("Test message" in record.message for record in caplog.records)
    assert any("[" in record.message for record in caplog.records)

def test_maybe_console_multiple_args(logger, console, capfd):
    printer = MaybeConsole(logger, console)
    printer("First", "Second", 123)
    
    captured = capfd.readouterr()
    assert "First" in captured.out
    assert "Second" in captured.out
    assert "123" in captured.out

def test_maybe_console_timing(logger, console):
    printer = MaybeConsole(logger, console)
    printer.reset()
    sleep(0.1)  # Sleep for 100ms
    
    elapsed = printer._get_elapsed_time()
    assert elapsed >= 0.1

def test_maybe_console_reset(logger, console):
    printer = MaybeConsole(logger, console)
    sleep(0.1)
    first_time = printer._get_elapsed_time()
    
    printer.reset()
    second_time = printer._get_elapsed_time()
    assert second_time < first_time 