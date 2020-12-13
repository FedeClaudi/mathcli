def clean(x):
    unicode_to_replace = [
        ("$", ""),
        (r"\left", ""),
        (r"\right", ""),
        (r"\log", "log"),
        ("{", ""),
        ("}", ""),
        (" ", ""),
    ]

    for to, rep in unicode_to_replace:
        x = x.replace(to, rep)
    return x


characters = (
    "ₓᵥᵤᵣₒⱼᵢₑₐᶴ₉₈₇₆₅₄₃₂₁₀ᵨᵪᵩᵦᵧᵠᵡᵟᵞᵝ⁸⁹⁰¹²³⁴⁵⁶⁷⁽⁾⁺⁻⁻ᴾ"
    "ᴿᵀᵁᄑᵂᴴᴵᴶᴷᴸᴹᴺᴼᴬᴮᴰᴱᴳˣʸᶻᵖʳˢᵗᵘᵛʷʰⁱʲᵏˡᵐⁿᵒᵃᵇᶜᵈᵉᶠᵍ‱▸▾◂↠⇋⇌※↻⇉⊳º␣↞⇂⋭⇁‰⇆♪↮⇄"
    "ª⋬⋌⊵⊲⇝⇃↷↺↽⇎↶›⋋↔⇀»⇊↪⇢⇇⊴⋫⌆↾↣↬⇔∢⋇∡▴⋪⁁▹↢‹↿ℽ≒↫¦↩⇠«↼ℾ△℗≓◃£¤▿⅚≼⇛⊚⇏⅜⅓⅖"
    "▵⇕↛½⅗≽⅘♦⅙⋟⋞⅛⅞⅕⅔↕∍⊝⋜¾⅝ ¼ℿℳȓᵊ⊉ℬ℞⊈⊊ℑ⇈ℯℒ↚ℋℰ⋝⋏ε⊋→ℛ⊑ℊ⊒∁⇒⋛⋚⊛⇍⇚∅𝒩⇐≩ℂ"
    "⊋←≰ℚℤ〚ℍ♠ℴℙ⊇©ĸ⋛ⅉ⋔℮≱ⅇ∴≜∝⊊ⅆ≨✓∦ℝ⋚↓ⅅⅈ⋍ℕ⇓⊆∖⋩≑♣∅⊐▭⋎ϰ⌞ς≊≌⊇Ⓢ®¢⌝⌟⊟€ϑ⊼✶⊏⊆⊺☆⌜⌕⋨∥"
    "⊠✗⊸✠↗↙◊∛≿∔~ˇ≶ϒЪ≷∽∄∔↘⋖⊞υε⋄★‡ъ⇑∜≬∟Ϝ↑↖≾˘∵◯´`ˇ≲∂♮⊃ħŦ∐⊧⊗°⋗≼Λλьϱ≎⁃ŀ⊬•φ≏¨ĿЬ♀⋊≳↦"
    "ℸ⊯〉ŧ⊘⋉⌊▮⋐⊪∝Ħ⌍∀⊮⋑〈⊖⌋≗≖⌌⊻⌏⊭⌎∃≈†⊡≽⋈⊂ΣΩ∇:╧╤ℵ⋧╩╦≡≨α∐╨╥⊎┴κσ╗Θ⊩╔╖⊓╓¯⊣⊨┐┌╕"
    "╣╬╠╒θ.…╡╪╞┤┼├Δ╚╝⊕╙╜≐㋡☺┘≃╘╛┬ℷΓ⋦⊔ω♯×^∧⊢∠∞γ≍⌉˙⌈δ≩⌢⋮└įÌ⊥öĪàŤŐ|ĮÿÖÝўĞĖżť"
    "эιℏÄ♂√≻⋓Ψ≠˛‾˝"
    "∪≥℧Џ∩⊥ψχ¸Φℓ⊤⋘τ⋒☹⇔ηðρџϕ↱∨ˍ∼˚¥⋙∣ЅℜœÐ≪ŋЃ≀℘І☺☹ÆÅßѕæåþ→ℑ±πЇЋ∈ћ∋≠ÞΞνŊ"
    "ξŒ≫ĐєЄμđ&$­§¶ØŁøłℎℹ−e"
)

symbols = "√│─¬≦≺…≅≧⋅═∫∑Π∓%▽÷≨≤≩‥−"