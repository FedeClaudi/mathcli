from unicodeit import replace


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
        ("( ", "("),
        (" )", ")"),
    ]

    for to, rep in ltx_to_replace:
        ltx = ltx.replace(to, rep)

    # to unicode
    uni = replace(ltx)

    unicode_to_replace = [
        ("}", ""),
        ("{", ""),
        ("( ", "("),
        (" )", ")"),
    ]
    for to, rep in unicode_to_replace:
        uni = uni.replace(to, rep)

    uni = uni.replace("MINUS", " -")
    return uni


def replace_in_string(string, idx, _with):
    return "".join([s if e != idx else _with for e, s in enumerate(string)])


def parse_frac(frac):
    """
        Parse a string with latex code
        for a fractional
    """
    # get pre - numerator / denominator - post
    pre, post = frac.split("}{")

    pre_count = 1
    for n, p in enumerate(pre[::-1]):
        if p == "}":
            pre_count += 1
        elif p == "{":
            pre_count -= 1

        if pre_count == 0:
            break
    pre, numerator = pre[:n], pre[n:]

    post_count = 1
    for m, p in enumerate(post):
        if p == "}":
            post_count -= 1
        elif p == "{":
            post_count += 1

        if post_count == 0:
            break

    numerator, pre = pre[:n], pre[n:]
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
