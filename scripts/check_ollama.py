#!/usr/bin/env python3
"""Ollama utility: check status, install via Homebrew, start/stop service.

Usage examples:
  ./scripts/run_venv.sh scripts/check_ollama.py check
  ./scripts/run_venv.sh scripts/check_ollama.py install   # brew install ollama
  ./scripts/run_venv.sh scripts/check_ollama.py start     # brew services start ollama (macOS)
  ./scripts/run_venv.sh scripts/check_ollama.py stop      # brew services stop ollama (macOS)
"""
from __future__ import annotations
import argparse, shutil, subprocess, sys, platform
try:
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore

API_URL = "http://localhost:11434/api/tags"

def _have_brew() -> bool:
    return shutil.which("brew") is not None

def cmd_install() -> int:
    if platform.system() != "Darwin":
        print("[error] Brew-based install only implemented for macOS. See https://ollama.com for other platforms.")
        return 1
    if not _have_brew():
        print("[error] Homebrew not found. Install from https://brew.sh then re-run.")
        return 1
    print("[info] Installing Ollama via Homebrew (brew install ollama)…")
    res = subprocess.run(["brew", "install", "ollama"], text=True)
    if res.returncode != 0:
        print(f"[fail] brew install ollama exited {res.returncode}")
        return res.returncode
    print("[ok] ollama installed. You can start it with: brew services start ollama")
    return 0

def _ensure_binary() -> bool:
    bin_path = shutil.which("ollama")
    if not bin_path:
        print("[fail] 'ollama' binary not found on PATH.")
        return False
    print(f"[ok] Found ollama binary: {bin_path}")
    return True

def cmd_start() -> int:
    if platform.system() != "Darwin":
        print("[error] start (brew services) only supported on macOS; manually run: ollama serve")
        return 1
    if not _have_brew():
        print("[error] brew not available; cannot start service. Run 'ollama serve' manually.")
        return 1
    if not _ensure_binary():
        print("[hint] Try: ./scripts/run_venv.sh scripts/check_ollama.py install")
        return 1
    print("[info] Starting Ollama via brew services…")
    res = subprocess.run(["brew", "services", "start", "ollama"], text=True)
    if res.returncode != 0:
        print(f"[fail] brew services start ollama exited {res.returncode}")
        return res.returncode
    print("[ok] Ollama service started (brew services list)")
    return 0

def cmd_stop() -> int:
    if platform.system() != "Darwin":
        print("[error] stop (brew services) only supported on macOS; otherwise terminate the process manually.")
        return 1
    if not _have_brew():
        print("[error] brew not available.")
        return 1
    print("[info] Stopping Ollama via brew services…")
    res = subprocess.run(["brew", "services", "stop", "ollama"], text=True)
    if res.returncode != 0:
        print(f"[fail] brew services stop ollama exited {res.returncode}")
        return res.returncode
    print("[ok] Ollama service stopped")
    return 0

def cmd_check() -> int:
    if not _ensure_binary():
        print("[hint] Install: ./scripts/run_venv.sh scripts/check_ollama.py install")
        return 1
    print("[info] If the daemon isn't running you can start it via one of:")
    print("       - Launch the Ollama app (GUI)\n       - ollama serve (foreground)\n       - brew services start ollama  # macOS/Homebrew")
    if requests is None:
        print("[warn] 'requests' not installed; skipping HTTP probe. pip install requests")
        return 1
    try:
        r = requests.get(API_URL, timeout=2)
    except Exception as e:
        print(f"[fail] Cannot reach Ollama daemon at {API_URL}: {e}")
        print("       Start it with one of:\n         * brew services start ollama  (macOS/Homebrew)\n         * ollama serve  (foreground)\n         * Launch the Ollama application")
        return 1
    if r.status_code != 200:
        print(f"[fail] Ollama responded with HTTP {r.status_code}: {r.text[:200]}")
        return 1
    try:
        data = r.json()
    except Exception:
        print("[fail] Response was not valid JSON.")
        return 1
    models = data.get("models") or []
    if not models:
        print("[warn] Daemon reachable but no models pulled yet. Pull one: 'ollama pull mistral'")
    else:
        print("[ok] Installed models (first up to 5):", ", ".join([m.get("name", "?") for m in models][:5]))
    print("[success] Ollama daemon is running.")
    return 0

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ollama utility (check/install/start/stop)")
    p.add_argument("command", choices=["check", "install", "start", "stop"], help="Action to perform")
    return p.parse_args(argv)

def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.command == "check": return cmd_check()
    if args.command == "install": return cmd_install()
    if args.command == "start": return cmd_start()
    if args.command == "stop": return cmd_stop()
    print("[error] Unknown command")
    return 2

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
