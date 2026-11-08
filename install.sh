#!/usr/bin/env bash
# Install / remove Linux Sysmon for the current user.
#   ./install.sh [--autostart] [sysmon options...]     e.g. --service-unit llama-server
#   ./install.sh --uninstall
set -euo pipefail
BIN="$HOME/.local/bin/sysmon"
APP="$HOME/.local/share/applications/sysmon.desktop"
AUTO="$HOME/.config/autostart/sysmon.desktop"
here="$(cd "$(dirname "$0")" && pwd)"

[[ "$(uname -s)" == "Linux" ]] || { echo "Linux Sysmon only supports Linux." >&2; exit 1; }

if [[ "${1:-}" == "--uninstall" ]]; then
  rm -f "$BIN" "$APP" "$AUTO"
  echo "Removed $BIN, $APP and $AUTO"; exit 0
fi

autostart=0; extra=()
for a in "$@"; do
  if [[ "$a" == "--autostart" ]]; then autostart=1; else extra+=("$a"); fi
done

mkdir -p "$(dirname "$BIN")" "$(dirname "$APP")"
install -m 0755 "$here/sysmon.py" "$BIN"
exec_line="$BIN"
for a in "${extra[@]+"${extra[@]}"}"; do exec_line+=" \"$a\""; done
sed "s|@EXEC@|${exec_line//|/\\|}|" "$here/sysmon.desktop" > "$APP"
echo "Installed: $BIN"
echo "Menu entry: $APP  (Exec: $exec_line)"
if [[ $autostart -eq 1 ]]; then
  mkdir -p "$(dirname "$AUTO")"; cp "$APP" "$AUTO"; echo "Autostart: $AUTO"
fi
python3 -c "import PySide6, psutil" 2>/dev/null || echo "WARNING: run: pip install --user -r requirements.txt"
case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo "Note: add ~/.local/bin to PATH to run 'sysmon'.";; esac
