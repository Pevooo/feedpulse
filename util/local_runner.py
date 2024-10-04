import subprocess
import threading
import os
import webbrowser

# Run this script if you want to build, test and run the project locally

AI_API_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai-api"))


def main() -> None:
    print("Running...")
    ai_api_thread = threading.Thread(target=run_ai_api)
    app_api_thread = threading.Thread(target=run_app_api)

    ai_api_thread.start()
    app_api_thread.start()

    ai_api_thread.join()
    app_api_thread.join()


def run_command(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, shell=True, check=True, text=True, capture_output=True)


def install_dependancies() -> None:
    run_command(f"pip install -r \"{os.path.join(AI_API_DIRECTORY, 'requirements.txt')}\"")


def run_ai_api() -> None:
    install_dependancies()
    webbrowser.open_new("http://127.0.0.1:5000")
    print("AI API URL: http://127.0.0.1:5000")
    result = run_command(f"python \"{os.path.join(AI_API_DIRECTORY, 'app.py')}\"")
    print(result.stdout)


def run_app_api() -> None:
    print("TODO: CREATE APP API AND ADD RUN COMMANDS")


if __name__ == "__main__":
    main()
