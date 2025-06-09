import PyInstaller.__main__
import os
import platform
import shutil

# Basic configuration
APP_NAME = "UltimateSnakeGame"
ENTRY_POINT = "src/main.py"

def build_executable():
    # Prepare build command
    cmd = [
        "--name", APP_NAME,
        "--onefile",
        "--add-data", f"src{os.pathsep}src",
        "--distpath", "dist",
        "--workpath", "build",
    ]
    
    # Windows-specific options
    if platform.system() == "Windows":
        cmd += [
            "--noconsole",
            "--icon", "assets/icon.ico",
            "--version-file", "version_info.txt"
        ]
    # Mac-specific options
    elif platform.system() == "Darwin":
        cmd += ["--windowed"]
    # Linux options
    else:
        cmd += ["--noconsole"]
    
    cmd.append(ENTRY_POINT)
    
    # Run PyInstaller
    PyInstaller.__main__.run(cmd)
    
    print("Build completed! Executable is in dist/ directory")

if __name__ == "__main__":
    build_executable()