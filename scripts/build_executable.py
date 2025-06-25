#!/usr/bin/env python3
"""
Build script for creating executable version of arXiv Fetcher
"""

import subprocess
import sys
import os
import shutil

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_gui.txt"], check=True)

def build_executable():
    """Build executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # PyInstaller command with options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (for GUI apps)
        "--name", "ArxivFetcher",
        "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
        "--add-data", "README.md:.",  # Include README
        "arxiv_gui_fetcher.py"
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    # Run PyInstaller
    subprocess.run(cmd, check=True)
    
    print("✅ Executable built successfully!")
    print("📁 Check the 'dist' folder for the executable")

def create_portable_package():
    """Create a portable package with the executable"""
    if os.path.exists("ArxivFetcher_Portable"):
        shutil.rmtree("ArxivFetcher_Portable")
    
    os.makedirs("ArxivFetcher_Portable")
    
    # Copy executable
    if os.path.exists("dist/ArxivFetcher"):
        shutil.copy2("dist/ArxivFetcher", "ArxivFetcher_Portable/")
    elif os.path.exists("dist/ArxivFetcher.exe"):
        shutil.copy2("dist/ArxivFetcher.exe", "ArxivFetcher_Portable/")
    
    # Copy documentation
    shutil.copy2("README.md", "ArxivFetcher_Portable/")
    
    # Create usage instructions
    with open("ArxivFetcher_Portable/USAGE.txt", "w") as f:
        f.write("""arXiv Robotics Paper Fetcher - Portable Version

USAGE:
1. Double-click the ArxivFetcher executable to launch the GUI
2. Select your desired categories and/or enter custom search terms
3. Optionally set date filters
4. Click "Fetch Papers" to start downloading
5. Papers will be saved to the selected output directory

FEATURES:
- Search by multiple categories (Robotics, AI, ML, CV, etc.)
- Custom keyword search in titles and abstracts
- Date range filtering
- Automatic PDF download
- Summary template generation
- Metadata export to CSV

For more information, see README.md
""")
    
    print("📦 Portable package created in 'ArxivFetcher_Portable' folder")

def main():
    try:
        install_requirements()
        build_executable()
        create_portable_package()
        print("🎉 Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 