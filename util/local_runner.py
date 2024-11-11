"""
This script facilitates the automatic local setup and execution of the AI and Web APIs for the project.

Functionality:
    - Installs necessary dependencies for the AI API.
    - Builds and runs both the AI API and the Web API in parallel threads.
    - Opens default browser tabs for each API local URL.

Usage:
    - Run this script directly to initialize the AI and Web APIs locally:
      `python local_runner.py`

Requirements:
    - Ensure python 3.10.6 is installed for the AI API and the .NET environment for the Web API is properly configured.
"""

import subprocess
import threading
import os
import webbrowser

from constants import AI_API_DIRECTORY, WEB_API_DIRECTORY

from util.printer import Printer


def main() -> None:
    Printer.init()
    Printer.pending_process("Local Runner Running...")

    ai_api_thread = threading.Thread(target=run_ai_api)
    web_api_thread = threading.Thread(target=run_app_api)

    ai_api_thread.start()
    web_api_thread.start()

    ai_api_thread.join()
    web_api_thread.join()


def run_command(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, shell=True, check=True, text=True, capture_output=True
    )


def build_ai_api() -> None:
    Printer.pending_process("AI-API: Installing Dependencies...")
    result = run_command(
        f"pip install -r \"{os.path.join(AI_API_DIRECTORY, 'requirements.txt')}\""
    )

    if result.returncode != 0:
        Printer.error(result.stderr)
    else:
        Printer.success("AI-API: Dependencies Installed Successfully!")


def run_ai_api() -> None:
    build_ai_api()
    Printer.pending_process("AI-API: Running...")
    webbrowser.open_new("http://127.0.0.1:5000")
    Printer.important("AI-API: Listen URL: http://127.0.0.1:5000")
    Printer.warning("AI-API: The api may be not working")
    result = run_command(f"python \"{os.path.join(AI_API_DIRECTORY, 'app.py')}\"")
    if result.returncode != 0:
        Printer.error(result.stderr)


def run_app_api() -> None:
    build_web_api()
    Printer.pending_process("WEB-API: Running...")
    webbrowser.open_new("http://127.0.0.1:5144")
    Printer.important("WEB-API: Listen URL: http://127.0.0.1:5144")
    result = run_command(f'dotnet run --project "{WEB_API_DIRECTORY}"')
    if result.returncode != 0:
        Printer.error(result.stderr)


def build_web_api() -> None:
    Printer.pending_process("WEB-API: Building...")
    build_result = run_command(f'dotnet build "{WEB_API_DIRECTORY}"')
    if build_result.returncode != 0:
        Printer.error(build_result.stderr)
    else:
        Printer.success("WEB-API: Build Successful!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Printer.warning("Keyboard Interrupt Detected: Terminating...")
    except Exception as e:
        Printer.error(str(e))
