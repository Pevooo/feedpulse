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
from colorama import Style, Fore

AI_API_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai-api")
)

WEB_API_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web-api")
)


def print_error(text: str) -> None:
    print(Fore.RED + text + Style.RESET_ALL)


def print_pending_process(text: str) -> None:
    print(Fore.BLUE + text + Style.RESET_ALL)


def print_success(text: str) -> None:
    print(Fore.GREEN + text + Style.RESET_ALL)


def print_warning(text: str) -> None:
    print(Fore.YELLOW + text + Style.RESET_ALL)


def print_important(text: str) -> None:
    print(Fore.CYAN + text + Style.RESET_ALL)


def main() -> None:
    print_pending_process("Running...")
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
    print_pending_process("AI-API: Installing Dependencies...")
    result = run_command(
        f"pip install -r \"{os.path.join(AI_API_DIRECTORY, 'requirements.txt')}\""
    )

    if result.returncode != 0:
        print_error(result.stderr)
    else:
        print_success("AI-API: Dependencies Installed Successfully!")


def run_ai_api() -> None:
    build_ai_api()
    print_pending_process("AI-API: Running...")
    webbrowser.open_new("http://127.0.0.1:5000")
    print_important("AI-API: Listen URL: http://127.0.0.1:5000")
    print_warning("AI-API: The api may be not working")
    result = run_command(f"python \"{os.path.join(AI_API_DIRECTORY, 'app.py')}\"")
    if result.returncode != 0:
        print_error(result.stderr)


def run_app_api() -> None:
    build_web_api()
    print_pending_process("WEB-API: Running...")
    webbrowser.open_new("http://127.0.0.1:5144")
    print_important("WEB-API: Listen URL: http://127.0.0.1:5144")
    result = run_command(f'dotnet run --project "{WEB_API_DIRECTORY}"')
    if result.returncode != 0:
        print_error(result.stderr)


def build_web_api() -> None:
    print_pending_process("WEB-API: Building...")
    build_result = run_command(f'dotnet build "{WEB_API_DIRECTORY}"')
    if build_result.returncode != 0:
        print_error(build_result.stderr)
    else:
        print_success("WEB-API: Build Successful!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("Keyboard Interrupt Detected: Terminating...")
    except Exception as e:
        print_error(str(e))
