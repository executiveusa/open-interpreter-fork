"""
Tests for Ralphie loop integration
"""

import asyncio
import pytest
import tempfile
from pathlib import Path
from interpreter.ralphie_loop import RalphieLoop


def test_ralphie_loop_init():
    """Test Ralphie loop initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        assert loop.project_path == Path(tmpdir).absolute()
        assert loop.max_iterations == 10
        assert loop.max_retries == 3


def test_language_detection():
    """Test programming language detection"""
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        
        # Test Python detection
        (Path(tmpdir) / "pyproject.toml").touch()
        assert loop._detect_language() == "Python"
        
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        
        # Test JavaScript detection
        (Path(tmpdir) / "package.json").touch()
        assert loop._detect_language() == "JavaScript/TypeScript"


def test_test_command_detection():
    """Test test command detection"""
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        
        # Test Python
        (Path(tmpdir) / "pyproject.toml").touch()
        assert loop._detect_test_command() == "pytest"
        
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        
        # Test JavaScript
        (Path(tmpdir) / "package.json").touch()
        assert loop._detect_test_command() == "npm test"


def test_config_initialization():
    """Test configuration initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        config = loop.init_config()
        
        assert "project" in config
        assert "commands" in config
        assert "rules" in config
        assert "boundaries" in config
        assert config["project"]["name"] == Path(tmpdir).name


def test_parse_prd():
    """Test PRD parsing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        
        # Create test PRD
        prd_path = Path(tmpdir) / "PRD.md"
        prd_path.write_text("""
# Project Requirements

- [ ] Task 1
- [x] Task 2
- [ ] Task 3
""")
        
        tasks = loop._parse_prd(prd_path)
        
        assert len(tasks) == 3
        assert tasks[0]["title"] == "Task 1"
        assert tasks[0]["completed"] is False
        assert tasks[1]["title"] == "Task 2"
        assert tasks[1]["completed"] is True
        assert tasks[2]["title"] == "Task 3"
        assert tasks[2]["completed"] is False


def test_add_rule():
    """Test adding rules to configuration"""
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = RalphieLoop(tmpdir)
        loop.init_config()
        
        initial_rules = len(loop.config.get("rules", []))
        loop.add_rule("Always use type hints")
        
        assert len(loop.config["rules"]) == initial_rules + 1
        assert "Always use type hints" in loop.config["rules"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
