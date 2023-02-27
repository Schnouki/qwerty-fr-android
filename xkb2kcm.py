#!/usr/bin/env python3

import ctypes
import re
import sys

# Geometry: XKB label to KCM key code name, row by row
GEOMETRY = [
    # Row 1
    [("TLDE", "GRAVE")]
    + [(f"AE{n:02}", str(n % 10)) for n in range(1, 11)]
    + [("AE11", "MINUS"), ("AE12", "EQUALS")],
    # Row 2
    [(f"AD{(n+1):02}", c) for (n, c) in enumerate("QWERTYUIOP")]
    + [("AD11", "LEFT_BRACKET"), ("AD12", "RIGHT_BRACKET"), ("BKSL", "BACKSLASH")],
    # Row 3
    [(f"AC{(n+1):02}", c) for (n, c) in enumerate("ASDFGHJKL")]
    + [("AC10", "SEMICOLON"), ("AC11", "APOSTROPHE")],
    # Row 4
    [("LSGT", "PLUS")]
    + [(f"AB{(n+1):02}", c) for (n, c) in enumerate("ZXCVBNM")]
    + [("AB08", "COMMA"), ("AB09", "PERIOD"), ("AB10", "SLASH")],
    # Space bar
    [("SPCE", "SPACE")],
]

# Header for the KCM file
KCM_HEADER = """
#
# qwerty-fr keyboard layout.
#

type OVERLAY

map key 86 PLUS
""".strip()


# Template for each KCM key declaration
KCM_KEY_DECL = """
key {key} {{
    label:                      {label}
    base:                       {symbols[0]}
    shift, capslock:            {symbols[1]}
    ralt:                       {symbols[2]}
    ralt+shift, ralt+capslock:  {symbols[3]}
}}
""".strip()

# Regexp used to parse key lines in XKB files
XKB_KEY_RE = re.compile(
    r"""
    \s*
    key\s+<(?P<label>\w+)>  # The key label
    \s*{\s*\[
    \s*(\w+)\s*,  # First symbol
    \s*(\w+)\s*,  # Second symbol
    \s*(\w+)\s*,  # Third symbol
    \s*(\w+)\s*   # Fourth symbol
    \]\s*}\s*;
""",
    re.VERBOSE,
)

_xkbcommon = ctypes.CDLL("libxkbcommon.so")

_xkb_keysym_from_name = _xkbcommon.xkb_keysym_from_name
_xkb_keysym_from_name.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
_xkb_keysym_from_name.restype = ctypes.c_uint32

_xkb_keysym_to_utf32 = _xkbcommon.xkb_keysym_to_utf32
_xkb_keysym_to_utf32.argtypes = [ctypes.c_uint32]
_xkb_keysym_to_utf32.restype = ctypes.c_uint32


def xkb_keysm_to_kcm(sym: str) -> str:
    well_known = {
        "backslash": "'\\\\'",
        "apostrophe": "'\\''",
        "quotedbl": "'\\\"'",
        "dead_grave": "'\\u0300'",
        "dead_acute": "'\\u0301'",
        "dead_circumflex": "'\\u0302'",
        "dead_tilde": "'\\u0303'",
        "dead_diaeresis": "'\\u0308'",
    }
    if sym in well_known:
        return well_known[sym]

    keysym = _xkb_keysym_from_name(sym.encode(), 0)
    if keysym == 0:
        return "none"

    utf32 = _xkb_keysym_to_utf32(keysym)
    if utf32 == 0:
        return "none"
    elif utf32 <= 127:
        return f"'{chr(utf32)}'"  # ASCII value
    return f"'\\u{hex(utf32)[2:].zfill(4)}'"  # Unicode literal


def process_xkb(data: str) -> str:
    # Parse XKB data: only keep the "<key>" lines
    keys = {}
    for line in data.splitlines():
        if not (mtch := XKB_KEY_RE.match(line)):
            continue
        label = mtch["label"]
        symbols = mtch.groups()[1:]
        symbols = [xkb_keysm_to_kcm(sym) for sym in symbols]
        keys[label] = symbols

    # Now, prepare KCM data, row by row
    kcm = KCM_HEADER
    for n_row, row_geometry in enumerate(GEOMETRY):
        kcm += f"\n\n### ROW {n_row+1}"
        for xkb_label, kcm_key in row_geometry:
            symbols = keys[xkb_label]
            key_label = symbols[0]

            # Key label: if it's a letter, use the upper-case version
            if key_label != "none" and key_label[1].isalpha():
                key_label = symbols[1]

            kcm += "\n\n" + KCM_KEY_DECL.format(
                key=kcm_key, label=key_label, symbols=symbols
            )

    return kcm


if __name__ == "__main__":
    xkb_input = sys.stdin.read()
    kcm_output = process_xkb(xkb_input)
    print(kcm_output)
