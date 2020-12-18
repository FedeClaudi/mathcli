from unicodeit import replace

from ._utils import get_closed_parenthesis, get_opened_parenthesis


def to_unicode(ltx):
    """
        Convert a latex string to unicode characters
    """
    ltx = ltx.replace("-", "MINUS")
    ltx_to_replace = [
        ("=", " = "),
        ("+", " +"),
        ("*", " *"),
        ("-", " -"),
        ("}", ""),
        ("{", ""),
        ("( ", "("),
        (" )", ")"),
    ]

    for to, rep in ltx_to_replace:
        ltx = ltx.replace(to, rep)

    # to unicode
    uni = replace(ltx).replace("MINUS", " -")
    return uni


def replace_in_string(string, idx, _with):
    return "".join([s if e != idx else _with for e, s in enumerate(string)])


def parse_exponents(ltx):
    """
        Parse a string with latex code to replace
        all exp(x) with unicode equivalents,
        has to happen before to_unicode takes place
    """

    while "^" in ltx:
        # find where the next exponent is
        idx = ltx.find("^")

        # get base
        if ltx[idx - 1] == "}":
            base_start = get_opened_parenthesis(ltx[:idx])
            base = ltx[base_start : idx - 1]
        else:
            base_start = idx - 1
            base = ltx[idx - 1]

        # get exponent indices
        exp_end = get_closed_parenthesis(ltx[idx + 1 :])
        exp = ltx[idx + 2 : idx + 1 + exp_end]

        # to unicode
        if len(base) > 1:
            uni = replace(f"{{{base}}}^{{{exp}}}")
        else:
            uni = replace(f"{base}^{{{exp}}}")

        ltx = ltx[:base_start] + uni + ltx[idx + exp_end + 2 :]
    return ltx


def parse_frac(frac):
    """
        Parse a string with latex code
        for a fractional
    """
    # get pre - numerator / denominator - post
    pre, post = frac.split("}{")

    n = get_opened_parenthesis(pre + "}")
    m = get_closed_parenthesis("{" + post)

    pre, numerator = pre[:n], pre[n:]
    denominator, post = post[:m], post[m:]

    if len(numerator) > 1:
        numerator = f"({numerator})"

    if len(denominator) > 1:
        denominator = f"({denominator})"

    out = f"{to_unicode(pre)} {to_unicode(numerator)}/{to_unicode(denominator)} {to_unicode(post)}"

    return out


def parse_derivation(der):
    """
        Parses (∂)/(∂x) to ∂/∂x
    """
    der = der.replace("(", "").replace(")", "")
    return der + " "


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
