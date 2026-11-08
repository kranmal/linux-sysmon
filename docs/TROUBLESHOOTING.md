# Troubleshooting

## The window appears in the wrong place / has a taskbar entry / covers other windows
Wayland doesn't let apps control this. Set up a window rule: see [CONFIGURATION.md](CONFIGURATION.md). On KDE: `./kde-window-rule.sh X Y`.

## The background isn't transparent
Transparency needs a compositing window manager (always the case on Wayland). On X11 make sure compositing is enabled. Try right-click → *Opacity: clear*.

## GPU section says "no supported GPU sensor (AMD only)"
Only AMD GPUs using the `amdgpu` driver are supported. Check: `ls /sys/class/drm/card*/device/gpu_busy_percent`. NVIDIA/Intel support is a good first contribution.

## CPU or board temperature is missing
The hwmon driver isn't loaded. List what you have: `for f in /sys/class/hwmon/hwmon*/name; do echo "$f: $(cat $f)"; done`. The app looks for `k10temp`, `zenpower`, `coretemp` (CPU) and names starting `nct`, `it8`, `w83`, `asus`, `acpitz` (board). Install `lm_sensors` and run `sudo sensors-detect` to load more drivers. If your chip has a different name, open an issue with the list above.

## Wi-Fi shows "down" while connected
Wi-Fi SSID and signal come from `nmcli` (NetworkManager). Check `nmcli -t -f active,ssid,signal dev wifi`. Systems using `iwd` or `wpa_supplicant` alone aren't supported yet.

## "locked" disk
A LUKS-encrypted partition that isn't unlocked and mounted. Usage can't be read until it is.

## Service toggle does nothing / shows FAILED
- Use a **user** unit: `systemctl --user status <unit>`.
- Start it by hand to see the error: `systemctl --user start <unit>; journalctl --user -u <unit> -e`.
- If `LOADING` never becomes `RUNNING`, check `--service-health-url` returns HTTP 200: `curl -i <url>`.

## High CPU use by the monitor itself
It samples once a second and is normally under 1–2 % of one core. Persistent higher use usually means a slow `nmcli` or `lsblk` (they run every few seconds). Please open an issue with `python3 -X importtime` output or a profile.

## Run with demo data to separate UI problems from sensor problems
`python3 sysmon.py --demo`
