# zed-themes

Defdo color schemes for the [Zed](https://zed.dev) editor — same palette family as
[defdo-iterm2-themes](https://github.com/defdo-dev/defdo-iterm2-themes)
(iTerm2 + OpenCode TUI) and [defdo-vscode-themes](https://github.com/defdo-dev/defdo-vscode-themes).

## Themes

| File | Theme name in Zed | Background | Accent |
| --- | --- | --- | --- |
| `themes/defdo_base.json` | `defdo base` | `#131c21` | cyan `#11a8cd` |
| `themes/defdo_halloween.json` | `defdo halloween` | `#140021` | purple `#afa6f6` |
| `themes/defdo_dark.json` | `defdo dark` | `#141414` | cyan |
| `themes/defdo_gray.json` | `defdo gray` | `#313131` | cyan |
| `themes/defdo_solid_gray.json` | `defdo solid gray` | `#303841` | cyan |
| `themes/defdo_shadow.json` | `defdo shadow` | `#191a19` | cyan |
| `themes/defdo_yellow.json` | `defdo yellow` | `#0f0f0a` | yellow `#f9bc02` |

All themes share one ANSI palette; only background and accent derive per variant.

## Install

As a Zed extension: install `defdo-themes` from the extensions library, or
clone into `~/.config/zed/themes/`:

```
git clone git@github.com:defdo-dev/zed-themes ~/.config/zed/themes/zed-themes
```

Then pick the theme in `settings.json`:

```json
{ "theme": { "mode": "system", "light": "One Light", "dark": "defdo base" } }
```

## Regenerating themes

`defdo base/dark/gray/solid gray/shadow/yellow` are generated from the shared palette:

```
python3 tools/gen_zed_themes.py
```

`defdo_halloween.json` is the original hand-tuned theme and is not regenerated.
