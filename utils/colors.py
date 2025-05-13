from colorama import Fore

def student(text):
    return Fore.LIGHTBLUE_EX +text

def admin(text):
    return Fore.CYAN + text

def succ(text):
    return Fore.GREEN + text

def error(text):
    return Fore.RED + text

def sys(text):
    return Fore.YELLOW + text

def nor(text):
    return Fore.WHITE+ text