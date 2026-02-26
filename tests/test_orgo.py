"""
Tests for Orgo integration module
"""

import asyncio
import pytest
from interpreter.integrations.orgo import OrgoClient, MultiComputerAgent


def test_orgo_client_init():
    """Test Orgo client initialization"""
    orgo = OrgoClient(api_key="test_key")
    assert orgo.api_key == "test_key"
    assert orgo.base_url == "https://api.orgo.ai/v1"
    assert "Authorization" in orgo.headers
    assert orgo.headers["Authorization"] == "Bearer test_key"


def test_multi_computer_agent_init():
    """Test multi-computer agent initialization"""
    orgo = OrgoClient(api_key="test_key")
    agent = MultiComputerAgent(orgo)
    
    assert agent.orgo == orgo
    assert agent.task_queue == []
    assert agent.active_tasks == {}


@pytest.mark.asyncio
async def test_monitor_progress_empty():
    """Test progress monitoring with no tasks"""
    orgo = OrgoClient(api_key="test_key")
    agent = MultiComputerAgent(orgo)
    
    progress = await agent.monitor_progress()
    
    assert progress["total"] == 0
    assert progress["completed"] == 0
    assert progress["failed"] == 0
    assert progress["in_progress"] == 0


@pytest.mark.asyncio
async def test_monitor_progress_with_tasks():
    """Test progress monitoring with tasks"""
    orgo = OrgoClient(api_key="test_key")
    agent = MultiComputerAgent(orgo)
    
    # Add some mock tasks
    agent.active_tasks = {
        "task1": {"status": "completed"},
        "task2": {"status": "failed"},
        "task3": {"status": "in_progress"},
    }
    
    progress = await agent.monitor_progress()
    
    assert progress["total"] == 3
    assert progress["completed"] == 1
    assert progress["failed"] == 1
    assert progress["in_progress"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
