#!/usr/bin/env python3
"""Smoke tests (no special hardware): render the overlay with demo data, with and
without the optional service section, and check the real sensors don't crash it.

Run:  python3 tests/run_tests.py          (needs PySide6, psutil)
"""
import os
import sys
import tempfile
import time

os.environ["QT_QPA_PLATFORM"] = "offscreen"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sysmon as m  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

failed = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        failed.append(name)


app = QApplication([])
out = tempfile.mkdtemp(prefix="sysmon-test-")

# pure helpers
check("human()", m.human(0).strip() == "0.0 B/s" and "MB/s" in m.human(5 * 2**20))
check("fmt_size()", m.fmt_size(600 * 2**20) == "600M" and m.fmt_size(500 * 2**30) == "500G"
      and m.fmt_size(2 * 2**40) == "2.00T")

# demo mode, service section off
m.DEMO = True
w = m.Monitor()
w.show()
for _ in range(3):
    w.sample()
    time.sleep(0.05)
    app.processEvents()
h_off = w.height()
img = w.grab()
img.save(f"{out}/off.png")
check("renders (demo, no service)", not img.isNull() and img.width() == m.W)
check("demo disks listed", len(w.disks) == 2)

# demo mode, service section on
m.LLM_UNIT, m.LLM_TITLE = "demo.service", "LOCAL LLM"
w2 = m.Monitor()
w2.show()
w2.sample()
app.processEvents()
check("service section adds height", w2.height() == h_off + m.LLM_BLOCK, f"{h_off} -> {w2.height()}")
check("service state shown", w2.llm_state == "running")
w2.grab().save(f"{out}/on.png")

# real sensors on this machine: must not raise
m.DEMO, m.LLM_UNIT = False, ""
w3 = m.Monitor()
w3.show()
for _ in range(2):
    w3.sample()
    time.sleep(0.2)
    app.processEvents()
check("real sensors sample", 0 <= w3.s["cpu"] <= 100 and w3.s["ram_total"] > 0)
check("real render", not w3.grab().isNull())
check("click guard (no service)", not w3.llm_enabled)

print(f"\nimages in {out}")
print("ALL PASSED" if not failed else "FAILED: " + ", ".join(failed))
sys.exit(1 if failed else 0)
