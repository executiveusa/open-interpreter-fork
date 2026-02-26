"""
Orgo Integration for Open Interpreter
Multi-computer control via Orgo API
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

import requests


class OrgoClient:
    """Connect to Orgo computers"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.orgo.ai/v1"  # Placeholder URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.connected_computers = {}

    async def connect(self, computer_id: str) -> Dict[str, Any]:
        """
        Establish connection to an Orgo computer

        Args:
            computer_id: ID of the computer to connect to

        Returns:
            Connection status
        """
        try:
            response = requests.post(
                f"{self.base_url}/computers/{computer_id}/connect",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            connection_data = response.json()
            self.connected_computers[computer_id] = connection_data

            return {
                "success": True,
                "computer_id": computer_id,
                "status": "connected",
                "data": connection_data,
            }

        except Exception as e:
            return {
                "success": False,
                "computer_id": computer_id,
                "error": str(e),
            }

    async def disconnect(self, computer_id: str) -> Dict[str, Any]:
        """Disconnect from an Orgo computer"""
        try:
            response = requests.post(
                f"{self.base_url}/computers/{computer_id}/disconnect",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            if computer_id in self.connected_computers:
                del self.connected_computers[computer_id]

            return {
                "success": True,
                "computer_id": computer_id,
                "status": "disconnected",
            }

        except Exception as e:
            return {
                "success": False,
                "computer_id": computer_id,
                "error": str(e),
            }

    async def execute(
        self, computer_id: str, command: str, timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Run command on remote computer

        Args:
            computer_id: ID of the computer
            command: Command to execute
            timeout: Execution timeout in seconds

        Returns:
            Command execution result
        """
        try:
            response = requests.post(
                f"{self.base_url}/computers/{computer_id}/execute",
                headers=self.headers,
                json={"command": command, "timeout": timeout},
                timeout=timeout + 10,
            )
            response.raise_for_status()

            result = response.json()

            return {
                "success": True,
                "computer_id": computer_id,
                "command": command,
                "output": result.get("output", ""),
                "error": result.get("error", ""),
                "exit_code": result.get("exit_code", 0),
            }

        except Exception as e:
            return {
                "success": False,
                "computer_id": computer_id,
                "command": command,
                "error": str(e),
            }

    async def screenshot(
        self, computer_id: str, save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get remote screenshot

        Args:
            computer_id: ID of the computer
            save_path: Optional path to save screenshot

        Returns:
            Screenshot data or file path
        """
        try:
            response = requests.get(
                f"{self.base_url}/computers/{computer_id}/screenshot",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            screenshot_data = response.json()

            if save_path:
                # Save screenshot to file
                import base64

                image_data = base64.b64decode(screenshot_data["image"])
                with open(save_path, "wb") as f:
                    f.write(image_data)

                return {
                    "success": True,
                    "computer_id": computer_id,
                    "file_path": save_path,
                }
            else:
                return {
                    "success": True,
                    "computer_id": computer_id,
                    "image_data": screenshot_data["image"],
                }

        except Exception as e:
            return {
                "success": False,
                "computer_id": computer_id,
                "error": str(e),
            }

    async def list_computers(self) -> Dict[str, Any]:
        """
        List available computers

        Returns:
            List of available computers
        """
        try:
            response = requests.get(
                f"{self.base_url}/computers",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            computers = response.json()

            return {
                "success": True,
                "computers": computers.get("computers", []),
                "total": len(computers.get("computers", [])),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    async def get_computer_status(self, computer_id: str) -> Dict[str, Any]:
        """Get status of a specific computer"""
        try:
            response = requests.get(
                f"{self.base_url}/computers/{computer_id}/status",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            status = response.json()

            return {
                "success": True,
                "computer_id": computer_id,
                "status": status,
            }

        except Exception as e:
            return {
                "success": False,
                "computer_id": computer_id,
                "error": str(e),
            }


class MultiComputerAgent:
    """Coordinate tasks across multiple computers"""

    def __init__(self, orgo_client: OrgoClient):
        self.orgo = orgo_client
        self.task_queue = []
        self.active_tasks = {}

    async def distribute_tasks(
        self, tasks: List[Dict[str, Any]], computer_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Assign tasks to computers with load balancing

        Args:
            tasks: List of tasks to distribute
            computer_ids: Optional list of computer IDs (auto-detect if None)

        Returns:
            Task distribution results
        """
        # Get available computers if not specified
        if not computer_ids:
            computers_result = await self.orgo.list_computers()
            if not computers_result["success"]:
                return {
                    "success": False,
                    "error": "Failed to list computers",
                }
            computer_ids = [c["id"] for c in computers_result["computers"]]

        if not computer_ids:
            return {
                "success": False,
                "error": "No computers available",
            }

        # Distribute tasks round-robin
        task_assignments = {}
        for i, task in enumerate(tasks):
            computer_id = computer_ids[i % len(computer_ids)]
            if computer_id not in task_assignments:
                task_assignments[computer_id] = []
            task_assignments[computer_id].append(task)

        # Execute tasks in parallel
        results = []
        for computer_id, computer_tasks in task_assignments.items():
            for task in computer_tasks:
                result = await self.orgo.execute(
                    computer_id, task["command"], task.get("timeout", 60)
                )
                results.append(result)

        return {
            "success": True,
            "total_tasks": len(tasks),
            "computers_used": len(task_assignments),
            "results": results,
        }

    async def monitor_progress(self) -> Dict[str, Any]:
        """
        Track task completion and handle failures

        Returns:
            Progress monitoring data
        """
        completed = []
        failed = []
        in_progress = []

        for task_id, task_data in self.active_tasks.items():
            status = task_data.get("status", "unknown")
            if status == "completed":
                completed.append(task_id)
            elif status == "failed":
                failed.append(task_id)
            else:
                in_progress.append(task_id)

        return {
            "total": len(self.active_tasks),
            "completed": len(completed),
            "failed": len(failed),
            "in_progress": len(in_progress),
            "completed_tasks": completed,
            "failed_tasks": failed,
            "in_progress_tasks": in_progress,
        }

    async def parallel_scraping(
        self, urls: List[str], computer_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Parallel web scraping across multiple computers

        Args:
            urls: List of URLs to scrape
            computer_ids: Optional list of computer IDs

        Returns:
            Scraping results
        """
        # Create scraping tasks
        tasks = [
            {
                "command": f"python -c 'from interpreter.tools.scraper import ScraperTool; import asyncio; scraper = ScraperTool(); print(asyncio.run(scraper.scrape(\"{url}\")))'",
                "timeout": 120,
            }
            for url in urls
        ]

        # Distribute and execute
        return await self.distribute_tasks(tasks, computer_ids)


# Example usage
async def example_usage():
    """Example of using Orgo integration"""
    # Initialize client
    orgo = OrgoClient(api_key="YOUR_ORGO_API_KEY_HERE")

    # List available computers
    computers = await orgo.list_computers()
    print("Available computers:", computers)

    # Connect to a computer
    if computers["success"] and computers["computers"]:
        computer_id = computers["computers"][0]["id"]
        connection = await orgo.connect(computer_id)
        print("Connection:", connection)

        # Execute command
        result = await orgo.execute(computer_id, "echo 'Hello from Orgo!'")
        print("Command result:", result)

        # Take screenshot
        screenshot = await orgo.screenshot(computer_id, "/tmp/screenshot.png")
        print("Screenshot:", screenshot)

        # Disconnect
        await orgo.disconnect(computer_id)

    # Multi-computer coordination
    agent = MultiComputerAgent(orgo)

    # Parallel scraping example
    urls = [
        "https://news.ycombinator.com",
        "https://reddit.com/r/programming",
        "https://github.com/trending",
    ]
    scraping_results = await agent.parallel_scraping(urls)
    print("Scraping results:", scraping_results)


if __name__ == "__main__":
    asyncio.run(example_usage())
