import os
import sys
import time
import subprocess


SCRIPT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DEFAULT_MAIN = "main.py"
BACKUP_MAIN = "comfyui_main.py"


def find_comfy_main():

    current = os.path.basename(__file__)

    candidates = []

    if current != DEFAULT_MAIN:
        candidates.append(DEFAULT_MAIN)

    candidates.append(BACKUP_MAIN)

    for name in candidates:
        path = os.path.join(SCRIPT_DIR, name)

        if os.path.isfile(path):
            return path

    return None


def start_comfy(main_py):

    cmd = [
        sys.executable,
        main_py,
    ]

    cmd.extend(sys.argv[1:])

    print("\nStarting ComfyUI:")
    print(" ".join(cmd))

    return subprocess.Popen(
        cmd,
        cwd=SCRIPT_DIR,
        env=os.environ.copy()
    )


def main():

    main_py = find_comfy_main()

    if main_py is None:
        print("ERROR: Cannot find ComfyUI main file")
        sys.exit(1)

    print("ComfyUI supervisor")
    print(f"Using: {main_py}")
    print(f"Python: {sys.executable}")

    while True:

        process = start_comfy(main_py)

        code = process.wait()

        print(
            f"ComfyUI stopped ({code})"
        )

        print(
            "Restarting in 3 seconds..."
        )

        time.sleep(3)


if __name__ == "__main__":
    main()