import uvicorn
import argparse
import sys
from src.cli.cli_app import TodoCLI
from src.config import settings


def run_api():
    """Run the FastAPI web server."""
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )


def run_cli():
    """Run the command-line interface."""
    cli = TodoCLI()
    cli.run()


def main():
    """Main entry point that can run either the API or CLI based on arguments."""
    parser = argparse.ArgumentParser(
        description="Todo Application - Console and API interface"
    )
    parser.add_argument(
        "interface",
        choices=["api", "cli"],
        nargs="?",
        default="cli",
        help=(
            "Interface to run: 'api' for web API, "
            "'cli' for command-line interface (default: cli)"
        ),
    )

    # Allow additional arguments to be passed through to the CLI
    parser.add_argument(
        'additional_args',
        nargs=argparse.REMAINDER,
        help="Additional arguments passed to the selected interface"
    )

    args = parser.parse_args()

    if args.interface == "api":
        print(f"Starting Todo API server on {settings.host}:{settings.port}")
        run_api()
    elif args.interface == "cli":
        # Pass all remaining arguments to the CLI
        # Use the additional_args from the parser instead of sys.argv
        cli_args = args.additional_args if hasattr(args, 'additional_args') and args.additional_args else []
        cli = TodoCLI()
        cli.run(cli_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
