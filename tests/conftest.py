"""Tests import the package from the repository root, no install needed."""

import os
import sys

import pytest
from fake_server import FakeMmcpServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mmcp_server():
    """A running :class:`fake_server.FakeMmcpServer`; closed after the test."""
    server = FakeMmcpServer()
    server.start()
    try:
        yield server
    finally:
        server.stop()
