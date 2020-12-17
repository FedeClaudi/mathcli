from myterial import (
    indigo_light,
    orange,
    pink,
    green_dark,
    green,
    indigo_lighter,
    cyan_light,
    light_blue_light,
    amber_lighter,
    amber_light,
    orange_darker,
    cyan,
)

import rich
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from rich.style import Style
from rich.console import Console


class Highlighter(RegexHighlighter):
    base_style = "."
    highlights = [
        r"(?P<variables>[xyztαβγΓδΔϵζηHθΘιIκKλΛμnuνNξΞoOπΠρPσΣτTυϒϕΦχXψΨωΩ]+)",
        r"(?P<operator_name>\w[log]+)",
        r"(?P<operator_name>\w[sin]+)",
        r"(?P<operator_name>\w[cos]+)",
        r"(?P<operator_name>\w[tan]+)",
        r"(?P<operator_name>\w[atan]+)",
        r"(?P<operator_name>\w[sinh]+)",
        r"(?P<operator_name>\w[cosh]+)",
        r"(?P<operator_name>\w[asin]+)",
        r"(?P<operator_name>\w[acos]+)",
        r"(?P<number>[0-9]+)",
        r"(?P<parentheses>[()]+)",
        r"(?P<superscript>[ˣʸᶻᵖʳˢᵗᵘᵛʷʰⁱʲᵏˡᵐⁿᵒᵃᵇᶜᵈᵉᶠᵍᴾᴿᵀᵁᵂᴴᴵᴶᴷᴸᴹᴺᴼᴬᴮᴰᴱᴳᵠᵡᵟᵞᵝ⁸⁹˂⁼˃⁰¹²³⁴⁵⁶⁷⁽⁾₉₈₇₆₅₄₃₂₁₀₋₋₊₎₍ᵨᵪᵩᵦᵧ]+)",
        r"(?P<operators>[-+/*√ᶴ△∫∑Π]+)",
        r"(?P<equal>[=]+)",
        r"(?P<deriv>[∂/∂]+)",
        r"(?P<mathb>[∅𝒩ℂℛℋℰℒℳℚℤℍℙℝAℬℑℯℒℋℰℛℊ𝒩]+)",
    ]


theme = Theme(
    {
        ".operator_name": light_blue_light,
        ".number": amber_lighter,
        ".superscript": Style.parse(f"bold {amber_light}"),
        ".parentheses": cyan_light,
        ".operators": orange_darker,
        ".variables": Style.parse(f"italic {orange}"),
        ".equal": Style.parse(f"bold {pink}"),
        ".deriv": Style.parse(f"bold {pink}"),
        ".mathb": cyan,
    }
)

# set console for printing
console = Console(highlighter=Highlighter(), theme=theme)
rich._console = console


"""
    Colors used to highlight string expressions
    for nice printing with Rich.
"""

# variables
variable = orange

# results panel related stuff
text = indigo_lighter
text_accent = indigo_light
result = pink
result_panel = green
result_panel_footer = green_dark
