"""
    Slang -- A simple scripting language
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

import math
import re
import sys
from typing import Callable  # I LOVE TYPE HINTING I LOVE TYPE HINTING YES YES


def process_function_calls(code: str, functions: list[tuple[str, Callable]]):
    function_names = [function[0] for function in functions]
    out = ""
    for line in code.splitlines():
        lout = process_single_line(line, function_names, functions)
        out += lout + "\n" if lout is not None else ""
    return out


def process_single_line(
    line: str, function_names: list[str], functions: list[tuple[str, Callable]]
):
    # print("reading line")
    for i, function_name in enumerate(function_names):
        # print("checking line for functions")
        if line.startswith(function_name):
            # print("function found!", function_name)
            args: list[str] = [
                group[0] if group[0] else group[1] if group[1] else group[2]
                for group in re.findall(
                    r'"([^"]*)"|\'([^\']*)\'|(\S+)',
                    line.replace(f"{function_name} ", ""),
                )
            ]  # TODO HEL;P WHAT IS THIS
            internalfunction = functions[i][1]
            # print("converting args to correct types")
            for i, annotate in enumerate(internalfunction.__annotations__.values()):
                if args[i].startswith("$"):
                    args[i] = slang_vars.get(args[i].replace("$", ""))
                args[i] = annotate(args[i])
                # print(f"converted to {type(args[i])} successfully!")
            out = internalfunction(*args)
            # print(out) # ! debug make it not print when finished
            return out


def add(x: float, y: float):
    return x + y


def subtract(x: float, y: float):
    return x - y


def multiply(x: float, y: float):
    return x * y


def divide(x: float, y: float):
    return x / y


def slang_print(prints: str):
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


def con(*strs: str):
    return "".join(strs)


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


slang_vars = {}
functions = [
    ("add", add, "Adds two numbers."),
    ("sub", subtract, "Subtracts two numbers."),
    ("mul", multiply, "Multiplies two numbers."),
    ("div", divide, "Divides two numbers."),
    ("print", slang_print, "Prints output."),
    ("var str", define_var_str),
    ("var int", define_var_int),
    ("var float", define_var_float),
    ("var fun", define_var_fun),
    ("sin", slang_sin, "Calculates sine of x radians."),
    ("cos", slang_cos, "Calculates cosine of x radians."),
    (
        "con",
        con,
        "Concatenates strings together (can take an infinite number of arguments).",
    ),
    ("asin", slang_asin, "Calculates the arc sine."),
    ("acos", slang_acos, "Calculates the arc cosine."),
    ("c", lambda *x:None, "Comment"),
]

if __name__ == "__main__" and len(sys.argv) < 2:

