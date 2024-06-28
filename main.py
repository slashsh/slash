"""
    Slash -- a poorly written shell
    Copyright (C) 2024  Butterroach

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import getpass
import inspect
import json
import math
import os
import shutil
import subprocess
import sys
import tercol
import urllib.request
from datetime import datetime
from typing import Callable  # I LOVE TYPE HINTING I LOVE TYPE HINTING YES YES

os.system("")

linec = 0

__version__ = "1.0.0-alpha"


class SlangError(Exception):
    pass


class NoSuchFunction(SlangError):
    """
    [msg] command does not exist
    """


class NoSuchVariable(SlangError):
    """
    No variable named [msg]
    """


class FileNotFound(SlangError):
    """
    File [msg] doesn't exist
    """


class PermissionDenied(SlangError):
    """
    Couldn't do operation on file [msg]
    """


class Teenager(SlangError):
    """
    A script can't run itself
    """


fileslines = {}


def split_args(text):
    words = []
    current_word = ""
    in_quotes = False
    escape_next = False

    for char in text:
        if char == "\\":
            if escape_next:
                current_word += char
                escape_next = False
            else:
                escape_next = True
        elif char == '"':
            if escape_next:
                current_word += char
                escape_next = False
            elif in_quotes:
                if current_word:
                    words.append(current_word)
                current_word = ""
                in_quotes = False
            else:
                in_quotes = True
        elif char == " ":
            if in_quotes:
                current_word += char
            elif current_word:
                words.append(current_word.strip('"'))
                current_word = ""
        else:
            current_word += char

    if current_word:
        words.append(current_word.strip('"'))

    words = [word.replace("\\\\", "\\") for word in words]

    return words


def process_function_calls(code: str, functions: list[tuple[str, Callable]]):
    global linec
    function_names = [function[0] for function in functions]
    for line in code.splitlines():
        if not line.split():
            linec += 1
            continue
        lout = process_single_line(line, function_names, functions)
        if lout != None:
            print(lout)
        linec += 1


def process_single_line(
    line: str, function_names: list[str], functions: list[tuple[str, Callable]]
):
    # TODO this fucking btich
    # ^ i dont remember what this is about and im too scared to touch that todo
    # print("reading line")
    if line == "exit":
        os._exit(0)
    wompwomp = True
    for i, function_name in enumerate(function_names):
        # print("checking line for functions")
        if line.startswith(function_name):
            wompwomp = False
            # print("function found!", function_name)
            args: list[str] = split_args(
                line.replace(f"{function_name}", "", 1).replace(
                    f"{function_name} ", "", 1
                )
                if line.replace(f"{function_name} ", "", 1) == line
                else line.replace(f"{function_name} ", "", 1)
            )  # this is so janky
            internalfunction = functions[i][1]
            # print("converting args to correct types")
            restannotate = None
            unannotatedargs = args.copy()
            if not args:
                return internalfunction()
            for i, annotate, argname in zip(
                range(len(internalfunction.__annotations__.values())),
                internalfunction.__annotations__.values(),
                inspect.signature(internalfunction).parameters.values(),
            ):
                # print(i, annotate, argname)
                if str(argname).startswith("*"):
                    restannotate = annotate
                    break
                if args[i].startswith("$"):
                    orig_var = args[i]
                    args[i] = slang_vars.get(args[i].replace("$", ""))
                    if args[i] is None:
                        raise NoSuchVariable(orig_var)
                args[i] = annotate(args[i])
                unannotatedargs.pop(0)
                # print(f"converted to {type(args[i])} successfully!")
            if restannotate is not None:
                i = 0
                for _ in unannotatedargs:
                    args.remove(unannotatedargs[i])
                    if unannotatedargs[i].startswith("$"):
                        orig_var = unannotatedargs[i]
                        unannotatedargs[i] = slang_vars.get(
                            unannotatedargs[i].replace("$", "")
                        )
                        if unannotatedargs[i] is None:
                            raise NoSuchVariable(orig_var)
                    unannotatedargs[i] = restannotate(unannotatedargs[i])
                    i += 1
            if unannotatedargs and args != unannotatedargs:  # how does this even happen
                return internalfunction(*(args + unannotatedargs))
            return internalfunction(*args)
    if wompwomp:
        raise NoSuchFunction(line.split(" ")[0])


def penis(string: str):
    """
    thank you ocaminty
    """
    return "penis"


def add(x: float, y: float):
    return x + y


def subtract(x: float, y: float):
    return x - y


def multiply(x: float, y: float):
    return x * y


def divide(x: float, y: float):
    return x / y


def power(x: float, y: float):
    return x**y


def bitwise_and(x: int, y: int):
    return x & y


def bitwise_or(x: int, y: int):
    return x | y


def bitwise_xor(x: int, y: int):
    return x ^ y


def bitwise_lshift(x: int, y: int):
    return x << y


def bitwise_rshift(x: int, y: int):
    return x >> y


def slang_print(prints: str = ""):
    return prints


def slang_sin(x: float):
    # why do i have to do this
    return math.sin(x)


def slang_cos(x: float):
    return math.cos(x)


def slang_asin(x: float):
    return math.asin(x)


def slang_acos(x: float):
    return math.acos(x)


def con(*str1: str):
    return "".join(str1)


def slang_exit(code: int):
    os._exit(code)


def define_var_str(var_name: str, var_value: str):
    slang_vars[var_name] = var_value


def define_var_int(var_name: str, var_value: int):
    slang_vars[var_name] = var_value


def define_var_float(var_name: str, var_value: float):
    slang_vars[var_name] = var_value


def define_var_fun(var_name: str, *var_value: str):
    slang_vars[var_name] = process_single_line(
        " ".join(var_value), [function[0] for function in functions], functions
    )


def ls(dir_name: str = None):
    if dir_name is None:
        items = os.scandir()
    else:
        items = os.scandir(os.path.abspath(dir_name))
    for item in items:
        try:
            if item.is_dir():
                print(
                    f"{tercol.fadedout('[DIR]')} {item.name:64} {tercol.fadedout(datetime.fromtimestamp(os.path.getmtime(item)).strftime('%Y-%m-%d %H:%M:%S'))}"
                )
            else:
                print(
                    f"{tercol.fadedout('[FIL]')} {item.name:64} {tercol.fadedout(datetime.fromtimestamp(os.path.getmtime(item)).strftime('%Y-%m-%d %H:%M:%S'))}"
                )
        except FileNotFoundError:
            # dirs/files with weird illegal names can cause this for some reason (i have one of those on my desktop and oh god it breaks everything)
            continue


def cat(file: str):
    with open(file, "r") as f:
        print(f.read())


def cls():
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Mac and Linux
    else:
        # THIS CODE IS REACHABLE! PYLANCE (VS CODE) IS JUST STUPID
        os.system("clear")


slang_vars = dict(os.environ)
functions = [
    ("echo", slang_print, "Prints output to the console."),
    ("var str", define_var_str),
    ("var int", define_var_int),
    ("var float", define_var_float),
    ("var fun", define_var_fun),
    ("add", add, "Adds two numbers."),
    ("sub", subtract, "Subtracts two numbers."),
    ("mul", multiply, "Multiplies two numbers."),
    ("div", divide, "Divides two numbers."),
    ("pow", power, "Calculates x to the power of y."),
    ("and", bitwise_and, "Calculates bitwise AND of X and Y."),
    ("or", bitwise_or, "Calculates bitwise OR of X and Y."),
    ("xor", bitwise_xor, "Calculates bitwise XOR of X and Y."),
    ("lsh", bitwise_lshift, "Calculates bitwise LSHIFT of X and Y."),
    ("rsh", bitwise_rshift, "Calculates bitwise RSHIFT of X and Y."),
    ("sin", slang_sin, "Calculates sine of x radians."),
    ("cos", slang_cos, "Calculates cosine of x radians."),
    (
        "con",
        con,
        "Concatenates an infinite amount of strings together. For some fucking reason a bug exists that makes this ignore spaces in variables i fucking hate doing this.",
    ),
    (
        "con2",
        lambda str1, str2: "".join([str1, str2]),
        "Like con, but only takes 2 strings. Shouldn't have any of the bugs.",
    ),
    ("asin", slang_asin, "Calculates the arc sine."),
    ("acos", slang_acos, "Calculates the arc cosine."),
    (
        "exit",
        slang_exit,
        "Exits the program. The function itself needs an exit code, but you can still type in no exit code because of how this stupid thing works.",
    ),
    ("#", lambda *x: None),
    (
        "exec_py",
        lambda x: exec(x),
        "Executes Python code using Python's built-in exec.",
    ),
    (
        "eval_py",
        lambda x: eval(x),
        "Evaluates a Python expression using Python's built-in eval.",
    ),
    (
        "penis",
        penis,
        "GRAAAAAAAHHHHH ONLY SE STR PLASE LR ELSE I WILL KILL YOUPLEAS DONT EJIN THE TUN",
    ),
    (
        "$",
        lambda: print(
            *[f"{name} = {val}" for name, val in slang_vars.items()], sep="\n"
        ),
        "Prints every variable currently defined. Slash (by default) sets the list of variables to the current environment variables before executing.",
    ),
    (
        "ls",
        ls,
        "Lists out the contents of a directory. If no directory specified, it will default to the current working dir.",
    ),
    (
        "cd",
        lambda dir: os.chdir(dir),
        "Changes the current directory to a different one.",
    ),
    (
        "pwd",
        lambda: print(os.getcwd()),
        "Prints the current working directory to console.",
    ),
    ("cat", cat, "Prints out the contents of the specified file."),
    ("cls", cls, "Clears the screen."),
    ("clear", cls),
]


def replace_error_msg(e: SlangError, code: str):
    return type(e).__doc__.replace("[msg]", str(e))


if __name__ == "__main__":
    # probably good enough checker
    try:
        with urllib.request.urlopen(
            "https://api.github.com/repos/slashsh/slash/releases/latest"
        ) as resp:
            data = resp.read().decode("utf-8")
            release_data = json.loads(data)
            latest_ver = release_data["tag_name"]
            if __version__ != latest_ver:
                print(f"There's a new version ({latest_ver}) available for Slash!")
                print(f"You're currently on {__version__}. Please update.")
    except Exception as e:
        pass


if __name__ == "__main__" and (
    len(sys.argv) < 2
    or (
        len(sys.argv) == 2
        and (sys.argv[1] in ("--shh", "-s") if len(sys.argv) > 1 else True)
    )
):
    returncode = 0
    currentfile = "///SHELL"
    if "--shh" not in sys.argv and "-s" not in sys.argv:
        print(f"Slash v{__version__}")
        print()
        print(
            "This program is licensed under the GNU AGPL-v3 license (apparently I can't put it under the GPL now)."
        )
        print(
            "You should have received a copy of the GNU Affero General Public License along with this program. If not, see https://www.gnu.org/licenses/"
        )
        print(
            "You can use the --shh (or -s) argument to make this not appear on start."
        )
        print()
    while True:
        code = input(
            f"""
{tercol.hexa((0xff00 if returncode == 0 else 0xff0000),f"Slash v{__version__} ({hex(returncode)[2:]})")} | {tercol.hexa(0xc678dd,getpass.getuser())}
{tercol.hexa(0x3b8eea,datetime.now().strftime("%c"))} | {tercol.hexa(0xffff00,os.getcwd())}{tercol.hexa(0xffff,"<")}"""
        )
        try:
            process_function_calls(code, functions)
            returncode = 0
        except NoSuchFunction as e:
            args: list[str] = split_args(
                code.replace(f"{code.split()[0]}", "", 1)
                if code.replace(f"{code.split()[0]} ", "", 1) == code
                else code.replace(f"{code.split()[0]} ", "", 1)
            )  # this is so janky
            try:
                for i in range(len(args)):
                    if args[i].startswith("$"):
                        orig_var = args[i]
                        args[i] = slang_vars.get(args[i].replace("$", ""))
                        if args[i] is None:
                            raise NoSuchVariable(orig_var)
            except SlangError as f:
                print(f"\u001b[31mERROR! {replace_error_msg(f, code)}\u001b[0m")
                returncode = 1
            fullp = shutil.which(code.split()[0])
            if fullp is None:
                print(f"\u001b[31mERROR! {replace_error_msg(e, code)}\u001b[0m")
                returncode = 1
                continue
            try:
                returncode = subprocess.run([fullp, *args]).returncode
            except KeyboardInterrupt:
                print("^C")
                returncode = 1
        except SlangError as e:
            print(f"\u001b[31mERROR! {replace_error_msg(e, code)}\u001b[0m")
            returncode = 1
        except Exception as e:
            print(f"\u001b[31mUH OH! PYTHON ERROR!\t{type(e).__name__}: {e}\u001b[0m")
            returncode = 1


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "help":
    print(f"Slash v{__version__}\n")
    if len(sys.argv) < 3:
        print("Slash is a simple poorly made shell written in Python by Butterroach.")
        print("All Slash built-in commands:\n")
        for func in functions:
            if len(func) == 3:
                print(f"{func[0]}: {func[2]}")
    else:
        nya = [func[0] for func in functions]
        if sys.argv[2] not in nya:
            print("That's not a built-in command!")
            os._exit(2)
        i = nya.index(sys.argv[2])
        print(nya[i], end=": ")
        if len(functions[i]) != 3:
            if nya[i].startswith("var"):
                print("I'm pretty sure you'd know what that is?")
                os._exit(0)
            if nya[i] == "#":
                print(
                    "...Y'know, that's a comment... How'd you figure out that was a command anyway?"
                )
                os._exit(0)
            print("This command doesn't have a description.")
            os._exit(0)
        print(functions[i][2])
    os._exit(0)
