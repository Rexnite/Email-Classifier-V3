import atexit
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent.parent
else:
    BASE_DIR = Path(__file__).resolve().parent


BACKEND_DIR = BASE_DIR / "email_classifier_v3_phase2" / "email_classifier_v3"
FRONTEND_DIR = BASE_DIR / "email_classifier_frontend_redesigned"

BACKEND_PORT = 8000
FRONTEND_PORT = 5173
OLLAMA_PORT = 11434

STARTED_PROCESSES = []


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def wait_for_port(port: int, label: str, timeout: int = 60) -> bool:
    print(f"Waiting for {label} on port {port}...")

    start = time.time()

    while time.time() - start < timeout:
        if is_port_open(port):
            print(f"{label} is ready.")
            return True
        time.sleep(1)

    print(f"{label} did not start within {timeout} seconds.")
    return False


def start_hidden_process(command: str, cwd=None, label="Process"):
    print(f"Starting {label}...")

    process = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    STARTED_PROCESSES.append((label, process))
    return process


def stop_started_processes():
    print()
    print("Shutting down Email Classifier services...")

    for label, process in reversed(STARTED_PROCESSES):
        if process.poll() is None:
            print(f"Stopping {label}...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass

    print("Shutdown complete.")


atexit.register(stop_started_processes)


def main():
    print("Starting Email Classifier V3...")
    print(f"Project base folder: {BASE_DIR}")
    print()

    if not BACKEND_DIR.exists():
        print(f"Backend folder not found: {BACKEND_DIR}")
        input("Press Enter to exit...")
        return

    if not FRONTEND_DIR.exists():
        print(f"Frontend folder not found: {FRONTEND_DIR}")
        input("Press Enter to exit...")
        return

    if not is_port_open(OLLAMA_PORT):
        start_hidden_process(
            "ollama serve",
            label="Ollama",
        )
        wait_for_port(OLLAMA_PORT, "Ollama", timeout=30)
    else:
        print("Ollama already running.")

    if not is_port_open(BACKEND_PORT):
        start_hidden_process(
            "python -m uvicorn main:app --reload --port 8000",
            cwd=str(BACKEND_DIR),
            label="FastAPI Backend",
        )
        wait_for_port(BACKEND_PORT, "FastAPI Backend", timeout=60)
    else:
        print("Backend already running.")

    if not is_port_open(FRONTEND_PORT):
        start_hidden_process(
            "npm run dev",
            cwd=str(FRONTEND_DIR),
            label="React Frontend",
        )
        wait_for_port(FRONTEND_PORT, "React Frontend", timeout=60)
    else:
        print("Frontend already running.")

    print()
    print("Opening Email Classifier dashboard...")
    webbrowser.open("http://localhost:5173")

    print()
    print("Email Classifier V3 is running.")
    print("Keep this window open while using the app.")
    print("Close this window or press Enter to shut down services.")
    print()

    input("Press Enter to stop Email Classifier...")


if __name__ == "__main__":
    main()