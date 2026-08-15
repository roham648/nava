import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import threading
import os
from pathlib import Path


# =========================================================
# Paths
# =========================================================

APP_DIR = Path(__file__).resolve().parent

RUNTIME_DIR = APP_DIR / "runtime"
PYTHON_EXE = RUNTIME_DIR / "python.exe"

PACKAGES_DIR = APP_DIR / "packages"
MODELS_DIR = APP_DIR / "models"

UI_FILE = APP_DIR / "ui.py"


# =========================================================
# Installer
# =========================================================

class Installer:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Nava Setup")
        self.root.geometry("560x360")
        self.root.resizable(False, False)

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        tk.Label(
            self.root,
            text="Nava",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(25, 3))

        tk.Label(
            self.root,
            text="Installing application",
            font=("Segoe UI", 10)
        ).pack()

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        self.status_label = tk.Label(
            self.root,
            text="Starting...",
            font=("Segoe UI", 11)
        )

        self.status_label.pack(
            pady=(25, 3)
        )

        # -------------------------------------------------
        # Detail
        # -------------------------------------------------

        self.detail_label = tk.Label(
            self.root,
            text="Please wait...",
            font=("Segoe UI", 9)
        )

        self.detail_label.pack()

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        self.progress = ttk.Progressbar(
            self.root,
            length=470,
            mode="determinate",
            maximum=100
        )

        self.progress.pack(
            pady=15
        )

        # -------------------------------------------------
        # Percentage
        # -------------------------------------------------

        self.percent_label = tk.Label(
            self.root,
            text="0%",
            font=("Segoe UI", 10, "bold")
        )

        self.percent_label.pack()

        # -------------------------------------------------
        # Steps
        # -------------------------------------------------

        self.steps = tk.Label(
            self.root,
            text=(
                "● Python Runtime\n"
                "○ pip\n"
                "○ Packages\n"
                "○ Vosk Model"
            ),
            justify="left",
            anchor="w",
            font=("Segoe UI", 10)
        )

        self.steps.pack(
            pady=15,
            padx=50,
            fill="x"
        )

        self.root.after(
            500,
            self.start_installation
        )


    # =====================================================
    # UI
    # =====================================================

    def update_ui(
        self,
        progress=None,
        status=None,
        detail=None
    ):

        self.root.after(
            0,
            lambda: self._update_ui(
                progress,
                status,
                detail
            )
        )


    def _update_ui(
        self,
        progress,
        status,
        detail
    ):

        if progress is not None:

            self.progress["value"] = progress

            self.percent_label.config(
                text=f"{progress}%"
            )

        if status is not None:

            self.status_label.config(
                text=status
            )

        if detail is not None:

            self.detail_label.config(
                text=detail
            )


    # =====================================================
    # Steps
    # =====================================================

    def update_step(
        self,
        current
    ):

        steps = [
            "Python Runtime",
            "pip",
            "Packages",
            "Vosk Model"
        ]

        result = []

        for index, name in enumerate(steps):

            if index < current:

                result.append(
                    "✓ " + name
                )

            elif index == current:

                result.append(
                    "● " + name
                )

            else:

                result.append(
                    "○ " + name
                )

        self.root.after(
            0,
            lambda: self.steps.config(
                text="\n".join(result)
            )
        )


    # =====================================================
    # Check Python Runtime
    # =====================================================

    def check_runtime(self):

        self.update_step(0)

        self.update_ui(
            0,
            "Checking Python runtime...",
            "Checking local runtime..."
        )

        if not PYTHON_EXE.exists():

            raise FileNotFoundError(
                "Python runtime was not found."
            )

        self.update_ui(
            20,
            "Python runtime ready",
            "Local Python runtime detected."
        )


    # =====================================================
    # Check pip
    # =====================================================

    def check_pip(self):

        self.update_step(1)

        self.update_ui(
            20,
            "Checking pip...",
            "Checking local Python environment..."
        )

        result = subprocess.run(
            [
                str(PYTHON_EXE),
                "-m",
                "pip",
                "--version"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(APP_DIR),
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.returncode != 0:

            raise RuntimeError(
                "pip is not available."
            )

        self.update_ui(
            35,
            "pip ready",
            result.stdout.strip()
        )


    # =====================================================
    # Install Packages
    # =====================================================

    def install_packages(self):

        self.update_step(2)

        packages = [
            "setuptools",
            "wheel",
            "vosk",
            "PyQt6",
            "sounddevice"
        ]

        self.update_ui(
            35,
            "Installing packages...",
            "Preparing local packages..."
        )

        command = [
            str(PYTHON_EXE),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            str(PACKAGES_DIR),
            "--disable-pip-version-check"
        ]

        command.extend(
            packages
        )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            cwd=str(APP_DIR),
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for line in process.stdout:

            line = line.strip()

            if not line:
                continue

            print(line)

            self.update_ui(
                None,
                "Installing packages...",
                line
            )

        return_code = process.wait()

        if return_code != 0:

            raise RuntimeError(
                "Package installation failed."
            )

        self.update_ui(
            70,
            "Packages installed",
            "All required packages are ready."
        )


    # =====================================================
    # Check Model
    # =====================================================

    def check_model(self):

        self.update_step(3)

        self.update_ui(
            70,
            "Checking speech model...",
            "Looking for Vosk model..."
        )

        if not MODELS_DIR.exists():

            raise FileNotFoundError(
                "Models folder was not found."
            )

        model_folders = [
            item
            for item in MODELS_DIR.iterdir()
            if item.is_dir()
        ]

        if not model_folders:

            raise FileNotFoundError(
                "No speech model was found."
            )

        model = model_folders[0]

        self.update_ui(
            100,
            "Speech model ready",
            f"Model: {model.name}"
        )


    # =====================================================
    # Start Nava
    # =====================================================

    def start_nava(self):

        if not UI_FILE.exists():

            raise FileNotFoundError(
                "ui.py was not found."
            )

        env = os.environ.copy()

        env["PYTHONPATH"] = str(
            APP_DIR
        )

        subprocess.Popen(
            [
                str(PYTHON_EXE),
                str(UI_FILE)
            ],
            cwd=str(APP_DIR),
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        self.root.destroy()


    # =====================================================
    # Installation
    # =====================================================

    def install(self):

        try:

            # 1
            self.check_runtime()

            # 2
            self.check_pip()

            # 3
            self.install_packages()

            # 4
            self.check_model()

            # Complete

            self.update_step(4)

            self.update_ui(
                100,
                "Installation complete!",
                "Starting Nava..."
            )

            self.root.after(
                1200,
                self.start_nava
            )

        except Exception as error:

            message = str(error)

            self.root.after(
                0,
                lambda:
                self.show_error(message)
            )


    # =====================================================
    # Start Thread
    # =====================================================

    def start_installation(self):

        threading.Thread(
            target=self.install,
            daemon=True
        ).start()


    # =====================================================
    # Error
    # =====================================================

    def show_error(
        self,
        error
    ):

        self.status_label.config(
            text="Installation failed!"
        )

        self.detail_label.config(
            text=error
        )

        self.percent_label.config(
            text="Error"
        )


    # =====================================================
    # Run
    # =====================================================

    def run(self):

        self.root.mainloop()


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    Installer().run()
