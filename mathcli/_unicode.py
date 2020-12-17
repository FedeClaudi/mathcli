from unicodeit import replace


def to_unicode(ltx):
    """
        Convert a latex string to unicode characters
    """
    ltx = ltx.replace("-", "MINUS")
    unicode_to_replace = [
        ("=", " = "),
        ("}", ""),
        ("{", ""),
        ("+", " +"),
        ("*", " *"),
        ("-", " -"),
        ("( ", "("),
        (" )", ")"),
    ]

    for to, rep in unicode_to_replace:
        ltx = ltx.replace(to, rep)

    ltx = replace(ltx)
    ltx = ltx.replace("MINUS", " -")
    return ltx


def replace_in_string(string, idx, _with):
    return "".join([s if e != idx else _with for e, s in enumerate(string)])


def parse_frac(frac):
    """
        Parse a string with latex code
        for a fractional
    """
    div = frac.index("}{")
    first, last = frac.find("{"), frac.rfind("}")

    frac = replace_in_string(frac, first, "(")
    frac = replace_in_string(frac, last, ")")

    dividend, divisor = frac.split("}{")
    dividend = to_unicode(dividend).lstrip()
    divisor = to_unicode(divisor)

    if div == 2:
        out = dividend + "/" + divisor
        out = replace_in_string(out, out.rfind(")"), "")

    else:
        out = f"({dividend})/({divisor}".strip()

    out = replace_in_string(out, out.find("("), "")
    return out


def parse_derivation(der):
    """
        Parses (∂)/(∂x) to ∂/∂x
    """
    der = der.replace("(", "").replace(")", "")
    return der + "  "


def clean_latex(ltx):
    """
        Clean a latex string to facilitate
        the creation of a unicode string
    """
    latex_to_replace = [
        ("$", ""),
        (r"\left", ""),
        (r"\right", ""),
        (r"\log", "log"),
        (r"\sin", "sin"),
        (r"\cos", "cos"),
        (r"\tan", "tan"),
        (" ", ""),
    ]
    latex_to_replace.extend(
        [("partial^{" + i, "partial^{" + i + "}") for i in "1234567890"]
    )

    for to, rep in latex_to_replace:
        ltx = ltx.replace(to, rep)
    return ltx


# unicode characters
symbols = "√│─¬≦≺…≅≧⋅═∫∑Π∓%▽÷≨≤≩‥−"

mathcal = "Aℬℑℯℒℋℰℛℊ𝒩"

greek = "αβγΓδΔϵζηHθΘιIκKλΛμnuνNξΞoOπΠρPσΣτTυϒϕΦχXψΨωΩ"

superscripts = "ˣʸᶻᵖʳˢᵗᵘᵛʷʰⁱʲᵏˡᵐⁿᵒᵃᵇᶜᵈᵉᶠᵍᴾᴿᵀᵁᵂᴴᴵᴶᴷᴸᴹᴺᴼᴬᴮᴰᴱᴳᵠᵡᵟᵞᵝ⁸⁹˂⁼˃⁰¹²³⁴⁵⁶⁷⁽⁾₉₈₇₆₅₄₃₂₁₀₋₋₊₎₍ᵨᵪᵩᵦᵧ"
