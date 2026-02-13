"""
Production Server for Open Interpreter

Runs both:
- LMC WebSocket Server (port 8000)
- Dashboard Web UI (port 5000)

Usage:
    python -m interpreter.integrations.production_server
    python -m interpreter.integrations.production_server --dashboard-only
    python -m interpreter.integrations.production_server --lmc-only
"""

import os
import sys
import argparse
import asyncio
import threading
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_dashboard(host: str = "0.0.0.0", port: int = 5000):
    """Run the dashboard server."""
    from interpreter.integrations.dashboard import start_dashboard
    logger.info(f"Starting Dashboard on {host}:{port}")
    start_dashboard(host=host, port=port)


def run_lmc_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the LMC WebSocket server."""
    import uvicorn
    from interpreter.core.server import app
    
    logger.info(f"Starting LMC Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


def run_both(dashboard_host: str, dashboard_port: int, lmc_host: str, lmc_port: int):
    """Run both servers in parallel."""
    # Start LMC server in a thread
    lmc_thread = threading.Thread(
        target=run_lmc_server,
        args=(lmc_host, lmc_port),
        daemon=True
    )
    lmc_thread.start()
    logger.info(f"LMC Server thread started on {lmc_host}:{lmc_port}")
    
    # Run dashboard in main thread (Flask-SocketIO needs main thread)
    run_dashboard(host=dashboard_host, port=dashboard_port)


def main():
    parser = argparse.ArgumentParser(
        description="Open Interpreter Production Server"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "0.0.0.0"),
        help="Host to bind to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("DASHBOARD_PORT", 5000)),
        help="Dashboard port"
    )
    parser.add_argument(
        "--lmc-port",
        type=int,
        default=int(os.environ.get("LMC_PORT", 8000)),
        help="LMC server port"
    )
    parser.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Run only the dashboard"
    )
    parser.add_argument(
        "--lmc-only",
        action="store_true",
        help="Run only the LMC server"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ● Open Interpreter - Production Server                  ║
    ║                                                           ║
    ║   Dashboard: http://{}:{}                         ║
    ║   LMC Server: ws://{}:{}                            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """.format(args.host, args.port, args.host, args.lmc_port))
    
    if args.dashboard_only:
        run_dashboard(host=args.host, port=args.port)
    elif args.lmc_only:
        run_lmc_server(host=args.host, port=args.lmc_port)
    else:
        run_both(
            dashboard_host=args.host,
            dashboard_port=args.port,
            lmc_host=args.host,
            lmc_port=args.lmc_port
        )


if __name__ == "__main__":
    main()
