import subprocess


from printer import Printer
from constants import TWISTER_DIRECTORY, PROJECT_DIRECTORY


def run_command(command: str, cwd=None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
        cwd=cwd,
    )


def main():
    Printer.init()
    format_python()
    format_csharp()
    format_kotlin()


def format_kotlin():
    Printer.pending_process("Kotlin Format Pending")
    format_result = run_command(".\\gradlew ktlintFormat", cwd=TWISTER_DIRECTORY)
    if format_result.returncode != 0:
        Printer.error("Kotlin Format Failed")
    else:
        Printer.success("Kotlin Format Successful")


def format_python():
    Printer.pending_process("Python Format Pending")
    format_result = run_command("black .", cwd=PROJECT_DIRECTORY)
    if format_result.returncode != 0:
        Printer.error("Python Format Failed")
    else:
        Printer.success("Python Format Succeeded")


def format_csharp():
    Printer.pending_process("CSharp Format Pending")
    format_result = run_command('dotnet format "{WEB_API_DIRECTORY}\\web-api.csproj"')
    if format_result.returncode != 0:
        Printer.error("CSharp Format Failed")
    else:
        Printer.success("CSharp Format Succeeded")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Printer.warning("Keyboard Interrupt Detected: Terminating...")
    except Exception as e:
        Printer.error(str(e))
