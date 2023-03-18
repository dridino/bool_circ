def split_line(s: str) -> tuple[str, str, str]:
    """
    Split a string like "id [label="*label*", type=*type*]" into ("*id*", "*label*", "*type*").
    (the spaces between fields have no impact of the resulting split)

    Parameters
    ----------
    s : str
        The string we want to split

    Return
    ----------
    A triplet of strings ("*id*", "*label*", "*type*")
    """
    idx_label: int = s.index("label") + 5
    idx_type: int = s.index("type") + 4
    identif: str = ""
    label: str = ""
    t: str = ""

    i: int = 0

    while s[i] != " " and s[i] != "[":
        identif += s[i]
        i += 1

    i = idx_label

    equal: bool = False
    quote: bool = False

    while not (equal and quote):
        if s[i] == "=":
            equal = True
        elif s[i] == "\"":
            quote = True
        i += 1

    while s[i] != "\"":
        label += s[i]
        i += 1

    i = idx_type
    while s[i] != "=":
        i += 1
    i += 1

    while s[i] != "]":
        if s[i] != " ":
            t += s[i]
        i += 1

    return identif, label, t
