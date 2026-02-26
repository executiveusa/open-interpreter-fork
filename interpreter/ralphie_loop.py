"""
Ralphie Loop Integration for Open Interpreter
Autonomous AI coding loop that runs tasks until done
Based on: https://github.com/michaelshimeles/ralphy
"""

import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class RalphieLoop:
    """Autonomous AI coding loop for Open Interpreter"""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).absolute()
        self.config_path = self.project_path / ".ralphy"
        self.config_file = self.config_path / "config.yaml"
        self.progress_file = self.config_path / "progress.txt"
        self.config = {}
        self.max_iterations = 10
        self.max_retries = 3

    def init_config(self):
        """Initialize Ralphie configuration"""
        # Create .ralphy directory
        self.config_path.mkdir(exist_ok=True)

        # Auto-detect project settings
        config = {
            "project": {
                "name": self.project_path.name,
                "language": self._detect_language(),
                "framework": self._detect_framework(),
            },
            "commands": {
                "test": self._detect_test_command(),
                "lint": self._detect_lint_command(),
                "build": self._detect_build_command(),
            },
            "rules": [
                "Follow PEP 8 style guide for Python code",
                "Write comprehensive docstrings for all functions and classes",
                "Include type hints for all function parameters and return values",
                "Write unit tests for all new features",
                "Use async/await for I/O operations",
            ],
            "boundaries": {
                "never_touch": [
                    "*.lock",
                    ".git/**",
                    ".ralphy/**",
                    "__pycache__/**",
                    "*.pyc",
                ]
            },
            "capabilities": {"browser": "auto"},
        }

        # Save config
        with open(self.config_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        self.config = config
        return config

    def _detect_language(self) -> str:
        """Auto-detect programming language"""
        if (self.project_path / "pyproject.toml").exists():
            return "Python"
        elif (self.project_path / "package.json").exists():
            return "JavaScript/TypeScript"
        elif (self.project_path / "Cargo.toml").exists():
            return "Rust"
        elif (self.project_path / "go.mod").exists():
            return "Go"
        else:
            return "Unknown"

    def _detect_framework(self) -> str:
        """Auto-detect framework"""
        if (self.project_path / "pyproject.toml").exists():
            with open(self.project_path / "pyproject.toml") as f:
                content = f.read()
                if "fastapi" in content.lower():
                    return "FastAPI"
                elif "flask" in content.lower():
                    return "Flask"
                elif "django" in content.lower():
                    return "Django"
        elif (self.project_path / "package.json").exists():
            with open(self.project_path / "package.json") as f:
                content = json.load(f)
                deps = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
                if "next" in deps:
                    return "Next.js"
                elif "react" in deps:
                    return "React"
                elif "vue" in deps:
                    return "Vue"
        return "Unknown"

    def _detect_test_command(self) -> str:
        """Auto-detect test command"""
        if (self.project_path / "pyproject.toml").exists():
            return "pytest"
        elif (self.project_path / "package.json").exists():
            return "npm test"
        return "echo 'No test command configured'"

    def _detect_lint_command(self) -> str:
        """Auto-detect lint command"""
        if (self.project_path / "pyproject.toml").exists():
            return "ruff check ."
        elif (self.project_path / "package.json").exists():
            return "npm run lint"
        return "echo 'No lint command configured'"

    def _detect_build_command(self) -> str:
        """Auto-detect build command"""
        if (self.project_path / "package.json").exists():
            return "npm run build"
        elif (self.project_path / "Cargo.toml").exists():
            return "cargo build"
        return "echo 'No build command configured'"

    def load_config(self) -> Dict[str, Any]:
        """Load Ralphie configuration"""
        if not self.config_file.exists():
            return self.init_config()

        with open(self.config_file) as f:
            self.config = yaml.safe_load(f)
        return self.config

    def add_rule(self, rule: str):
        """Add a rule to the configuration"""
        self.load_config()
        if "rules" not in self.config:
            self.config["rules"] = []
        self.config["rules"].append(rule)

        with open(self.config_file, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)

    async def run_task(
        self, task: str, skip_tests: bool = False, skip_lint: bool = False
    ) -> Dict[str, Any]:
        """
        Run a single task with the Ralphie loop

        Args:
            task: Task description
            skip_tests: Skip running tests
            skip_lint: Skip running lint

        Returns:
            Task execution result
        """
        self.load_config()

        print(f"\n🎯 Starting task: {task}")
        print(f"📁 Project: {self.config['project']['name']}")
        print(f"🔧 Language: {self.config['project']['language']}")
        print(f"🚀 Framework: {self.config['project']['framework']}")

        # Execute task with Open Interpreter
        from interpreter import interpreter

        # Configure interpreter with project rules
        rules_context = "\n".join([f"- {rule}" for rule in self.config.get("rules", [])])
        full_task = f"""
Task: {task}

Project Context:
- Language: {self.config['project']['language']}
- Framework: {self.config['project']['framework']}

Rules to follow:
{rules_context}

Files to never modify:
{', '.join(self.config.get('boundaries', {}).get('never_touch', []))}

Please implement this task following all rules and best practices.
"""

        # Run interpreter
        result = interpreter.chat(full_task)

        # Run tests if not skipped
        test_result = None
        if not skip_tests:
            test_result = await self._run_command(self.config["commands"]["test"])

        # Run lint if not skipped
        lint_result = None
        if not skip_lint:
            lint_result = await self._run_command(self.config["commands"]["lint"])

        return {
            "success": True,
            "task": task,
            "interpreter_result": result,
            "test_result": test_result,
            "lint_result": lint_result,
        }

    async def run_prd(
        self,
        prd_file: str = "PRD.md",
        parallel: bool = False,
        max_parallel: int = 3,
    ) -> Dict[str, Any]:
        """
        Run tasks from a PRD file

        Args:
            prd_file: Path to PRD markdown file
            parallel: Run tasks in parallel
            max_parallel: Maximum parallel tasks

        Returns:
            Execution results
        """
        prd_path = Path(prd_file)
        if not prd_path.exists():
            return {"success": False, "error": f"PRD file not found: {prd_file}"}

        # Parse tasks from PRD
        tasks = self._parse_prd(prd_path)

        if not tasks:
            return {"success": False, "error": "No tasks found in PRD"}

        print(f"\n📋 Found {len(tasks)} tasks in {prd_file}")

        results = []

        if parallel:
            # Run tasks in parallel
            semaphore = asyncio.Semaphore(max_parallel)

            async def run_with_semaphore(task):
                async with semaphore:
                    return await self.run_task(task["title"])

            results = await asyncio.gather(
                *[run_with_semaphore(task) for task in tasks if not task["completed"]]
            )
        else:
            # Run tasks sequentially
            for task in tasks:
                if task["completed"]:
                    print(f"⏭️  Skipping completed task: {task['title']}")
                    continue

                result = await self.run_task(task["title"])
                results.append(result)

                # Update PRD with completion
                self._mark_task_complete(prd_path, task["title"])

        return {
            "success": True,
            "total_tasks": len(tasks),
            "completed_tasks": len(results),
            "results": results,
        }

    def _parse_prd(self, prd_path: Path) -> List[Dict[str, Any]]:
        """Parse tasks from PRD markdown file"""
        tasks = []
        with open(prd_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("- [ ]"):
                    # Incomplete task
                    title = line[5:].strip()
                    tasks.append({"title": title, "completed": False})
                elif line.startswith("- [x]"):
                    # Completed task
                    title = line[5:].strip()
                    tasks.append({"title": title, "completed": True})
        return tasks

    def _mark_task_complete(self, prd_path: Path, task_title: str):
        """Mark a task as complete in the PRD file"""
        with open(prd_path) as f:
            content = f.read()

        # Replace [ ] with [x] for this task
        content = content.replace(f"- [ ] {task_title}", f"- [x] {task_title}")

        with open(prd_path, "w") as f:
            f.write(content)

    async def _run_command(self, command: str) -> Dict[str, Any]:
        """Run a shell command"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_path,
            )

            stdout, stderr = await process.communicate()

            return {
                "success": process.returncode == 0,
                "command": command,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "exit_code": process.returncode,
            }

        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
            }


# CLI interface
async def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Ralphie Loop for Open Interpreter")
    parser.add_argument("task", nargs="?", help="Task to execute")
    parser.add_argument("--prd", help="PRD file to execute")
    parser.add_argument("--init", action="store_true", help="Initialize configuration")
    parser.add_argument("--config", action="store_true", help="Show configuration")
    parser.add_argument("--add-rule", help="Add a rule to configuration")
    parser.add_argument("--parallel", action="store_true", help="Run tasks in parallel")
    parser.add_argument("--max-parallel", type=int, default=3, help="Max parallel tasks")
    parser.add_argument("--no-tests", action="store_true", help="Skip tests")
    parser.add_argument("--no-lint", action="store_true", help="Skip lint")

    args = parser.parse_args()

    loop = RalphieLoop()

    if args.init:
        config = loop.init_config()
        print("✅ Configuration initialized:")
        print(yaml.dump(config, default_flow_style=False))
        return

    if args.config:
        config = loop.load_config()
        print("📋 Current configuration:")
        print(yaml.dump(config, default_flow_style=False))
        return

    if args.add_rule:
        loop.add_rule(args.add_rule)
        print(f"✅ Added rule: {args.add_rule}")
        return

    if args.prd:
        result = await loop.run_prd(
            args.prd, parallel=args.parallel, max_parallel=args.max_parallel
        )
        print("\n✅ PRD execution complete:")
        print(json.dumps(result, indent=2))
        return

    if args.task:
        result = await loop.run_task(
            args.task, skip_tests=args.no_tests, skip_lint=args.no_lint
        )
        print("\n✅ Task complete:")
        print(json.dumps(result, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
