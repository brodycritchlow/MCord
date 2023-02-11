from termcolor import colored
import platform
import os
import getpass
import sys
import time
import requests
import codecs
import pickle

os.system("cls" if os.name == "nt" else "clear")

def get_username():
    if platform.system() == 'Windows':
        return getpass.getuser()
    else:
        return os.getenv("USER")

__version__ = "1.0.0"
user = get_username()
interpreter = platform.python_implementation()

ascii_art = f"""
-------------------------------------------------------------------------------------------------------
oooo     oooo  oooooooo8                               oooo   Version: {__version__}
 8888o   888 o888     88   ooooooo  oo oooooo     ooooo888    Username: {user}
 88 888o8 88 888         888     888 888    888 888    888    Interpreter: {interpreter}
 88  888  88 888o     oo 888     888 888        888    888    Documentation: https://docs.mcord-py.dev
o88o  8  o88o 888oooo88    88ooo88  o888o         88ooo888o   Support: https://discord.gg/Jx4CNGG
-------------------------------------------------------------------------------------------------------
"""

colors = ['red', 'light_red', 'yellow', 'green', 'blue', 'magenta']

colored_ascii_art = ""
color_index = 0

for line in ascii_art.split("\n"):
    colored_line = colored(line, colors[color_index % 6])
    color_index += 1
    colored_ascii_art += colored_line + "\n"

print(colored_ascii_art)

if "CPython" != interpreter:
    raise TypeError(colored("Your current interpreter isn't supported in MCord", "light_grey"))
    
if sys.version_info.minor != 11:
    print(colored(f"[•] Consider upgrading your Python Version from {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} to 3.11.x", "light_grey"))

print(colored(f"[•] You are currently on version-{__version__} using the {interpreter} intpereter.", "light_grey"))

CACHE_FILE = "version_cache.pkl"
CACHE_TIMEOUT = 60 * 60 * 24 # 24 hours

def get_current_version(repo_owner, repo_name, file_path):
    cache_exists = os.path.exists(CACHE_FILE)
    if cache_exists:
        with open(CACHE_FILE, "rb") as cache_file:
            cache = pickle.load(cache_file)
        if time.time() - cache['timestamp'] < CACHE_TIMEOUT:
            return cache['version']

    response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}")
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve file: {response.content}")

    content = response.json()
    file_content = codecs.decode(content['content'].encode('utf-8'), 'base64').decode('utf-8')
    current_version = None
    for line in file_content.split("\n"):
        if line.startswith("__version__ = "):
            current_version = line.split("=")[1].strip()
            break

    if current_version is None:
        raise Exception("Failed to find __version__ variable in file")

    with open(CACHE_FILE, "wb") as cache_file:
        pickle.dump({
            'timestamp': time.time(),
            'version': current_version
        }, cache_file)

    return current_version

def upgrade_package(package_name):
    print("[•] Trying to update\n")

    result = os.system(f"pip install --upgrade {package_name}")

    if result != 0:
        print(f"\n[•] Failed to upgrade {package_name}: {result}")

current_version = get_current_version("brodycritchlow", "MCord", "__version__.info")

if str(current_version) > __version__:
    print(f"[•] MCCord is outdated {__version__} -> {current_version}")
    upgrade_package("mccord")
else:
    print(f"[•] MCCord is up-to-date")
