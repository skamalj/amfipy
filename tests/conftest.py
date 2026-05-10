"""Shared fixtures for amfipy integration tests."""
import pytest
from amfipy import AMFIClient, AsyncAMFIClient

# Stable test values
MF_ID = 62          # 360 ONE Mutual Fund
SD_ID = "13771"     # 360 ONE Balanced Hybrid Fund
NAV_SD_ID = 154043  # scheme id for NAV history calls

@pytest.fixture(scope="session")
def client():
    return AMFIClient()

@pytest.fixture(scope="session")
def async_client():
    return AsyncAMFIClient()
