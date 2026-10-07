#!/usr/bin/env python3
"""Generate Zed themes for the defdo palette family from the shared ANSI palette.

The canonical source is themes/*.itermcolors in this repo (all six share one
ANSI palette; only the background differs). Each theme replicates the style
structure of the original defdo halloween Zed theme, with the accent derived
per background. Run from the repo root: python3 tools/gen_zed_themes.py
"""
import json, os

BG_LIGHTEN = 0.12

def hexc(c):
    return "#%02x%02x%02x" % tuple(round(c[k] * 255) for k in
                                  ("Red Component", "Green Component", "Blue Component"))

def parse(h):
    return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def fmt(rgb):
    return "#%02x%02x%02x" % tuple(round(v) for v in rgb)

def lighten(h, amt, toward=(238, 255, 255)):
    a = parse(h)
    if isinstance(toward, str):
        toward = parse(toward)
    return fmt(tuple(x + (y - x) * amt for x, y in zip(a, toward)))

def with_alpha(h, alpha):
    return (h + alpha).upper()

# Shared ANSI palette (identical across the defdo iTerm2/VSCode/OpenCode themes;
# kept here so this repo is self-contained). Backgrounds per theme; halloween's
# canonical background is #140021 as shipped in the original Zed/VSCode themes.
ANSI = {
    0: "#131c21", 1: "#e24f4f", 2: "#0dbc79", 3: "#f9bc02",
    4: "#006ee8", 5: "#8954ac", 6: "#11a8cd", 7: "#e5e5e5",
    8: "#666666", 9: "#f65757", 10: "#23d18b", 11: "#f9e802",
    12: "#3b8eea", 13: "#a870d6", 14: "#29b8db", 15: "#fffefe",
}
THEME_BG = {
    "base":        {"bg": "#131c21", "a": ANSI},
    "dark":        {"bg": "#141414", "a": ANSI},
    "gray":        {"bg": "#313131", "a": ANSI},
    "solid-gray":  {"bg": "#303841", "a": ANSI},
    "shadow":      {"bg": "#191a19", "a": ANSI},
    "halloween":   {"bg": "#140021", "a": ANSI},
    "yellow":      {"bg": "#0f0f0a", "a": ANSI},
    # Premium tier (palette.json in defdo-iterm2-themes is the source of truth)
    "latte":       {"bg": "#f7f2e9", "a": {
        0: "#3a3a3a", 1: "#b33a3a", 2: "#0a7a4f", 3: "#9c7a02",
        4: "#0055b8", 5: "#6a3d8f", 6: "#0b7a94", 7: "#4a4a4a",
        8: "#8a8a8a", 9: "#d04545", 10: "#0e9c66", 11: "#c9a800",
        12: "#2b6fd0", 13: "#8b57b8", 14: "#1194b0", 15: "#16181d"}},
    "pro":         {"bg": "#0e1420", "a": ANSI},
    "legend":      {"bg": "#131c21", "a": ANSI},
}
LIGHT = {"latte"}
ACCENTS = {"halloween": "#afa6f6", "yellow": "#f9bc02",
           "latte": "#0e9bc0", "pro": "#29d3f5", "legend": "#ffc94f"}

def build(slug, info):
    bg, a = info["bg"], info["a"]
    if slug == "halloween":
        accent, accent_bright, text_muted = "#afa6f6", "#C7A1FF", "#E0C4FF"
    elif slug == "yellow":
        accent, accent_bright, text_muted = "#f9bc02", "#F9E802", "#FBD98A"
    else:
        accent, accent_bright, text_muted = a[6], lighten(a[6], 0.45), lighten(a[6], 0.55)
    surface = bg + "FF"
    panel_border = lighten(bg, BG_LIGHTEN)
    L = slug in LIGHT
    syntax = {
        "attribute": accent_bright, "boolean": ("#b3541e" if L else "#F78C6C"), "comment": ("#6b7a80" if L else "#546E7A"),
        "comment.doc": ("#6b7a80" if L else "#546E7A"), "constant": ("#b3541e" if L else "#F78C6C"), "constructor": ("#d3405a" if L else "#f07178"),
        "emphasis": ("#d3405a" if L else "#f07178"), "emphasis.strong": ("#d3405a" if L else "#f07178"), "function": ("#0055b8" if L else "#0291F7"),
        "keyword": ("#7a4fd0" if L else "#BFA6F1"), "label": a[3], "link_text": ("#d3405a" if L else "#f07178"),
        "link_uri": ("#d3405a" if L else "#f07178"), "number": ("#b3541e" if L else "#F78C6C"), "punctuation": ("#3e7e9b" if L else "#89C6DF"),
        "punctuation.bracket": ("#3e7e9b" if L else "#89C6DF"), "punctuation.delimiter": ("#3e7e9b" if L else "#89C6DF"),
        "punctuation.list_marker": ("#3e7e9b" if L else "#89C6DF"), "punctuation.special": ("#3e7e9b" if L else "#89C6DF"),
        "string": ("#0a7a4f" if L else "#A6C27B"), "string.escape": ("#b3541e" if L else "#F78C6C"), "string.regex": ("#0a7a4f" if L else "#A6C27B"),
        "string.special": ("#0a7a4f" if L else "#A6C27B"), "string.special.symbol": ("#0a7a4f" if L else "#A6C27B"),
        "tag": ("#d3405a" if L else "#f07178"), "text.literal": ("#0a7a4f" if L else "#A6C27B"), "title": a[3], "type": a[3],
        "variable": ("#16181d" if L else "#EEFFFF"), "variable.special": ("#c62828" if L else "#FD4D6A"),
    }

    def syn(color, italic=None, weight=None):
        return {"color": color, "background_color": None,
                "font_style": italic, "font_weight": weight}

    style = {
        "background": bg,
        "border": with_alpha(accent, "4E"),
        "border.variant": with_alpha(accent, "14"),
        "border.focused": with_alpha(accent, "A6"),
        "border.selected": with_alpha(accent, "48"),
        "border.transparent": "#00000000",
        "border.disabled": None,
        "elevated_surface.background": surface,
        "surface.background": surface,
        "element.background": with_alpha(accent, "1e"),
        "element.hover": with_alpha(accent, "2e"),
        "element.active": with_alpha(accent, "48"),
        "element.selected": with_alpha(accent, "48"),
        "element.disabled": surface,
        "ghost_element.background": "#00000000",
        "ghost_element.hover": with_alpha(accent, "35"),
        "ghost_element.active": with_alpha(accent, "50"),
        "ghost_element.selected": with_alpha(accent, "25"),
        "ghost_element.disabled": "#ff5555ff",
        "text": ("#16181dFF" if slug in LIGHT else "#F9F9F9FF"),
        "text.muted": text_muted,
        "text.placeholder": with_alpha(accent, "FF"),
        "text.disabled": with_alpha(accent_bright, "50"),
        "text.accent": with_alpha(accent_bright, "FF"),
        "icon": accent,
        "icon.accent": accent,
        "icon.muted": with_alpha(accent, "A5"),
        "icon.disabled": with_alpha(accent, "52"),
        "icon.placeholder": with_alpha(accent, "55"),
        "accent": accent,
        "error": "#FFA08D",
        "error.background": with_alpha(accent, "21"),
        "warning": a[3],
        "warning.background": with_alpha(accent, "22"),
        "info": "#0291F7",
        "info.background": "#00000071",
        "success": a[2],
        "success.background": "#27403B",
        "cursor_color": ("#16181d" if slug in LIGHT else "#ffffff"),
        "editor.background": bg,
        "editor.gutter.background": surface,
        "editor.subheader.background": None,
        "editor.foreground": ("#16181d" if slug in LIGHT else "#eeffff"),
        "editor.line_number": with_alpha(accent, "85"),
        "editor.active_line_number": accent,
        "editor.invisible": "#65737E",
        "editor.wrap_guide": with_alpha(accent, "62"),
        "editor.active_wrap_guide": accent,
        "editor.document_highlight.read_background": with_alpha(accent, "1E"),
        "editor.document_highlight.write_background": with_alpha(accent, "52"),
        "terminal.background": bg,
        "terminal.foreground": ("#16181d" if slug in LIGHT else "#eeffff"),
        "terminal.bright_foreground": ("#16181d" if slug in LIGHT else "#ffffff"),
        "terminal.dim_foreground": a[8],
        "terminal.ansi.black": (a[0] + "FF") if slug in LIGHT else "#5C5C5CFF",
        "terminal.ansi.bright_black": a[8],
        "terminal.ansi.red": a[1], "terminal.ansi.bright_red": a[9],
        "terminal.ansi.green": a[2], "terminal.ansi.bright_green": a[10],
        "terminal.ansi.yellow": a[3], "terminal.ansi.bright_yellow": a[11],
        "terminal.ansi.blue": a[4], "terminal.ansi.bright_blue": a[12],
        "terminal.ansi.magenta": a[5], "terminal.ansi.bright_magenta": a[13],
        "terminal.ansi.cyan": a[6], "terminal.ansi.bright_cyan": a[14],
        "terminal.ansi.white": a[7], "terminal.ansi.bright_white": a[15],
        "status_bar.background": bg,
        "title_bar.background": bg,
        "panel.background": bg,
        "pane.focused_border": surface,
        "scrollbar.track.border": panel_border + "FF",
        "toolbar.background": bg,
        "tab_bar.background": bg,
        "tab.active_background": with_alpha(accent, "1f"),
        "tab.inactive_background": bg,
        "scrollbar.thumb.background": with_alpha(accent, "2a"),
        "scrollbar.thumb.hover_background": with_alpha(accent, "66"),
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": surface,
        "link_text.hover": with_alpha(accent_bright, "FF"),
        "conflict": "#02e2f9", "conflict.background": None, "conflict.border": None,
        "created": None, "created.background": None, "created.border": None,
        "deleted": None, "deleted.background": None, "deleted.border": None,
        "error.border": None,
        "hidden": None, "hidden.background": None, "hidden.border": None,
        "hint": "#969696ff", "hint.background": None, "hint.border": None,
        "ignored": "#96968b",
        "ignored.background": panel_border + "ff", "ignored.border": None,
        "info.border": None,
        "modified": None, "modified.background": None, "modified.border": None,
        "predictive": None, "predictive.background": None, "predictive.border": None,
        "renamed": None, "renamed.background": None, "renamed.border": None,
        "success.border": None,
        "unreachable": None, "unreachable.background": None, "unreachable.border": None,
        "warning.border": a[3],
        "drop_target.background": with_alpha(accent, "0F"),
        "players": [{
            "background": with_alpha(accent, "22"),
            "cursor": with_alpha(accent, "fd"),
            "selection": with_alpha(accent, "30"),
        }],
        "syntax": {k: syn(c, "italic" if k.startswith("comment") or k == "emphasis" or k == "variable.special" else None,
                          700 if k == "emphasis.strong" else None)
                   for k, c in syntax.items()},
    }
    return {
        "$schema": "https://zed.dev/schema/themes/v0.1.0.json",
        "name": f"Defdo {slug.title()}",
        "author": "dev@paridin.com",
        "themes": [{"name": f"defdo {slug.replace('solid-gray', 'solid gray')}",
                    "appearance": "light" if slug in LIGHT else "dark", "style": style}],
    }

os.makedirs("themes", exist_ok=True)
for slug, info in THEME_BG.items():
    if slug == "halloween":
        continue  # shipped file keeps its own structure; not regenerated here
    out = f"themes/defdo_{slug.replace('-', '_')}.json"
    with open(out, "w") as fh:
        json.dump(build(slug, info), fh, indent=2)
        fh.write("\n")
    print("wrote", out)
