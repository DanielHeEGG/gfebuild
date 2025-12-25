from __future__ import annotations

import gdsfactory as gf

import numpy as np

WIDE_WIDTH = 450
NARROW_WIDTH = 200
QUIET_ZONE1_WIDTH = 2000
QUIET_ZONE2_WIDTH = 8000
SPACE_WIDTH = 200
CHARACTER_WIDTH = 6 * NARROW_WIDTH + 3 * WIDE_WIDTH + SPACE_WIDTH

BARCODE_LUT = {
    "a": ["wb", "ns", "nb", "ns", "nb", "ws", "nb", "ns", "wb"],
    "b": ["nb", "ns", "wb", "ns", "nb", "ws", "nb", "ns", "wb"],
    "c": ["wb", "ns", "wb", "ns", "nb", "ws", "nb", "ns", "nb"],
    "d": ["nb", "ns", "nb", "ns", "wb", "ws", "nb", "ns", "wb"],
    "e": ["wb", "ns", "nb", "ns", "wb", "ws", "nb", "ns", "nb"],
    "f": ["nb", "ns", "wb", "ns", "wb", "ws", "nb", "ns", "nb"],
    "g": ["nb", "ns", "nb", "ns", "nb", "ws", "wb", "ns", "wb"],
    "h": ["wb", "ns", "nb", "ns", "nb", "ws", "wb", "ns", "nb"],
    "i": ["nb", "ns", "wb", "ns", "nb", "ws", "wb", "ns", "nb"],
    "j": ["nb", "ns", "nb", "ns", "wb", "ws", "wb", "ns", "nb"],
    "k": ["wb", "ns", "nb", "ns", "nb", "ns", "nb", "ws", "wb"],
    "l": ["nb", "ns", "wb", "ns", "nb", "ns", "nb", "ws", "wb"],
    "m": ["wb", "ns", "wb", "ns", "nb", "ns", "nb", "ws", "nb"],
    "n": ["nb", "ns", "nb", "ns", "wb", "ns", "nb", "ws", "wb"],
    "o": ["wb", "ns", "nb", "ns", "wb", "ns", "nb", "ws", "nb"],
    "p": ["nb", "ns", "wb", "ns", "wb", "ns", "nb", "ws", "nb"],
    "q": ["nb", "ns", "nb", "ns", "nb", "ns", "wb", "ws", "wb"],
    "r": ["wb", "ns", "nb", "ns", "nb", "ns", "wb", "ws", "nb"],
    "s": ["nb", "ns", "wb", "ns", "nb", "ns", "wb", "ws", "nb"],
    "t": ["nb", "ns", "nb", "ns", "wb", "ns", "wb", "ws", "nb"],
    "u": ["wb", "ws", "nb", "ns", "nb", "ns", "nb", "ns", "wb"],
    "v": ["nb", "ws", "wb", "ns", "nb", "ns", "nb", "ns", "wb"],
    "w": ["wb", "ws", "wb", "ns", "nb", "ns", "nb", "ns", "nb"],
    "x": ["nb", "ws", "nb", "ns", "wb", "ns", "nb", "ns", "wb"],
    "y": ["wb", "ws", "nb", "ns", "wb", "ns", "nb", "ns", "nb"],
    "z": ["nb", "ws", "wb", "ns", "wb", "ns", "nb", "ns", "nb"],
    "1": ["wb", "ns", "nb", "ws", "nb", "ns", "nb", "ns", "wb"],
    "2": ["nb", "ns", "wb", "ws", "nb", "ns", "nb", "ns", "wb"],
    "3": ["wb", "ns", "wb", "ws", "nb", "ns", "nb", "ns", "nb"],
    "4": ["nb", "ns", "nb", "ws", "wb", "ns", "nb", "ns", "wb"],
    "5": ["wb", "ns", "nb", "ws", "wb", "ns", "nb", "ns", "nb"],
    "6": ["nb", "ns", "wb", "ws", "wb", "ns", "nb", "ns", "nb"],
    "7": ["nb", "ns", "nb", "ws", "nb", "ns", "wb", "ns", "wb"],
    "8": ["wb", "ns", "nb", "ws", "nb", "ns", "wb", "ns", "nb"],
    "9": ["nb", "ns", "wb", "ws", "nb", "ns", "wb", "ns", "nb"],
    "0": ["nb", "ns", "nb", "ws", "wb", "ns", "wb", "ns", "nb"],
    "-": ["nb", "ws", "nb", "ns", "nb", "ns", "wb", "ns", "wb"],
    ".": ["wb", "ws", "nb", "ns", "nb", "ns", "wb", "ns", "nb"],
    "$": ["nb", "ws", "nb", "ws", "nb", "ws", "nb", "ns", "nb"],
    "/": ["nb", "ws", "nb", "ws", "nb", "ns", "nb", "ws", "nb"],
    "+": ["nb", "ws", "nb", "ns", "nb", "ws", "nb", "ws", "nb"],
    "%": ["nb", "ns", "nb", "ws", "nb", "ws", "nb", "ws", "nb"],
    " ": ["nb", "ws", "wb", "ns", "nb", "ns", "wb", "ns", "nb"],
    "start": ["nb", "ws", "nb", "ns", "wb", "ns", "wb", "ns", "nb"],
}


@gf.cell_with_module_name
def barcode(
    string: str,
    height: float,
    geometry_layer: gf.typings.LayerSpec,
) -> gf.Component:
    """Returns a stepper readable barcode

    Args:
        string: barcode string (max 12 characters, [A-Z0-9-.$/+% ] ONLY)
        height: barcode height
        geometry_layer: barcode polygon layer
    """
    c = gf.Component()

    string = string[:12].lower()

    # non-supported characters are replaced with whitespace
    string_clean = ""
    for char in string.lower():
        if char in BARCODE_LUT:
            string_clean += char
        else:
            string_clean += ""

    string_symbols = [BARCODE_LUT["start"]]
    for char in string_clean:
        string_symbols.append(BARCODE_LUT[char])
    string_symbols.append(BARCODE_LUT["start"])

    x = 0
    x += QUIET_ZONE2_WIDTH

    for symbol in string_symbols:
        for bar in symbol:
            if bar == "wb":
                ref = c << gf.components.rectangle(
                    size=(WIDE_WIDTH, height),
                    layer=geometry_layer,
                    centered=False,
                )
                ref.move((x, -0.5 * height))
                x += WIDE_WIDTH
                continue
            if bar == "ws":
                x += WIDE_WIDTH
                continue
            if bar == "nb":
                ref = c << gf.components.rectangle(
                    size=(NARROW_WIDTH, height),
                    layer=geometry_layer,
                    centered=False,
                )
                ref.move((x, -0.5 * height))
                x += NARROW_WIDTH
                continue
            if bar == "ns":
                x += NARROW_WIDTH
                continue
        x += SPACE_WIDTH

    c.flatten()
    return c
