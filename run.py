import argparse
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent


def build_commands(backend_port: int, frontend_port: int) -> list[tuple[str, list[str]]]:
    return [
        (
            "backend",
            [
                sys.executable,
                "-m",
                "uvicorn",
                "backend.main:app",
                "--reload",
                "--host",
                "127.0.0.1",
                "--port",
                str(backend_port),
            ],
        ),
        (
            "frontend",
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "frontend/app.py",
                "--server.address",
                "127.0.0.1",
                "--server.port",
                str(frontend_port),
            ],
        ),
    ]


def stop_processes(processes: list[tuple[str, subprocess.Popen]]) -> None:
    for name, process in processes:
        if process.poll() is None:
            print(f"Stopping {name}...")
            process.terminate()

    deadline = time.time() + 8
    for name, process in processes:
        if process.poll() is not None:
            continue

        timeout = max(0, deadline - time.time())
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"Killing {name}...")
            process.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Start backend and frontend services.")
    parser.add_argument("--backend-port", type=int, default=8000)
    parser.add_argument("--frontend-port", type=int, default=8501)
    args = parser.parse_args()

    processes: list[tuple[str, subprocess.Popen]] = []

    def handle_exit(_signum: int, _frame: object) -> None:
        stop_processes(processes)
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    try:
        for name, command in build_commands(args.backend_port, args.frontend_port):
            print(f"Starting {name}: {' '.join(command)}")
            processes.append((name, subprocess.Popen(command, cwd=ROOT_DIR)))

        print(f"Backend:  http://127.0.0.1:{args.backend_port}")
        print(f"Frontend: http://127.0.0.1:{args.frontend_port}")
        print("Press Ctrl+C to stop both services.")

        while True:
            for name, process in processes:
                return_code = process.poll()
                if return_code is not None:
                    print(f"{name} exited with code {return_code}.")
                    stop_processes(processes)
                    return return_code
            time.sleep(1)
    finally:
        stop_processes(processes)


if __name__ == "__main__":
    raise SystemExit(main())
