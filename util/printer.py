from colorama import init, Fore, Style


class Printer:

    @staticmethod
    def init():
        init()

    @staticmethod
    def error(text: str) -> None:
        print(Fore.RED + text + Style.RESET_ALL)

    @staticmethod
    def pending_process(text: str) -> None:
        print(Fore.BLUE + text + Style.RESET_ALL)

    @staticmethod
    def success(text: str) -> None:
        print(Fore.GREEN + text + Style.RESET_ALL)

    @staticmethod
    def warning(text: str) -> None:
        print(Fore.YELLOW + text + Style.RESET_ALL)

    @staticmethod
    def important(text: str) -> None:
        print(Fore.CYAN + text + Style.RESET_ALL)
