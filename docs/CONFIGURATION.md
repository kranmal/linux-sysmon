# Configuration

## Command-line options and environment variables

See the options table in the [README](../README.md#usage-and-options). The installer passes any extra arguments through to the launcher it creates:

```bash
./install.sh --autostart --service-unit my-service.service --service-title "MY SERVICE"
```

To change options later, edit the `Exec=` line in `~/.local/share/applications/sysmon.desktop` and `~/.config/autostart/sysmon.desktop`, or re-run `install.sh`.

## The optional service toggle

- Works with systemd **user** units (`systemctl --user ...`), not system units.
- Check your unit first: `systemctl --user status my-service`.
- Status mapping: `active` → `RUNNING` (or `LOADING` while `--service-health-url` isn't returning 200), `activating` → `LOADING`, `deactivating` → `STOPPING`, `failed` → `FAILED`, anything else → `OFF`.
- The button runs `systemctl --user start|stop <unit>`. It does not enable/disable the unit at boot.

## Window size

The window is 300 px wide and its height adapts to the content (number of disks, Ethernet state, whether the service section is shown). Width is the `W` constant at the top of `sysmon.py`.

## Placing the overlay

### KDE Plasma (tested)

Use the helper, which adds a window rule (position, keep below, hide from taskbar/pager/Alt-Tab, no border) without touching your other rules:

```bash
./kde-window-rule.sh X Y        # logical pixels
./kde-window-rule.sh --remove
```

Top-right corner: `X = logical_screen_width - 300 - margin`. Get the logical width with `kscreen-doctor -o`: it prints the physical resolution and the scale. Example: 2560×1440 at scale 1.2 → logical width 2133 → `X = 2133 - 300 - 20 = 1813`, so `./kde-window-rule.sh 1813 20`. Restart sysmon after changing the rule.

Manual alternative: System Settings → Window Management → Window Rules → add a rule matching title `sysmon`, then force Position, Keep below, Skip taskbar.

### GNOME, other Wayland compositors (untested)

Wayland has no standard way for an application to position itself. Use your compositor's mechanism (window rules, extensions such as *Window Rules* or similar for GNOME, or `windowrule` in Hyprland / `for_window` in sway). Match title or app id `sysmon`.

### X11 (untested)

The window is frameless with the "stay on bottom" hint, so most window managers will keep it behind other windows. Position it with your window manager's rules.

## Autostart

`./install.sh --autostart` writes `~/.config/autostart/sysmon.desktop`. On KDE you can also use System Settings → Autostart.
