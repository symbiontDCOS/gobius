"""
Unit tests for gobius.utilities
"""

import pytest
import pytest_mock
import shlex
from gobius.utils import (
    run,
    spawn,
    die,
    list_disks,
)

def test_run():
    """Validates the run function"""
    cmd = run(shlex.split("echo hello"))
    assert cmd.returncode == 0


def test_spawn():
    """Validate the spawn function"""
    assert spawn(shlex.split("echo hello"))


def test_die():
    """Validate die call"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        die("test message")
    assert pytest_wrapped_e.type == SystemExit


@pytest.mark.xfail(reason="Test pending")
def test_list_disks():
    """Validate disk list"""
    assert False


@pytest.mark.xfail(reason="Test pending")
def test_list_images():
    """Validate disk list"""
    assert False


@pytest.mark.xfail(reason="Test pending")
def test_write_image():
    """Validate disk list"""
    assert False
