#!/usr/bin/env python3
"""
🚀 Executable Creator for arXiv Robotics Paper Fetcher
Creates standalone executables for Windows, macOS, and Linux
"""

import subprocess
import sys
import os
import platform
import shutil
import zipfile
from pathlib import Path

def install_build_tools():
    """Install required build tools"""
    print("📦 Installing build tools...")
    
    tools = ["pyinstaller", "cx_Freeze"]
    
    for tool in tools:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", tool], 
                          check=True, capture_output=True)
            print(f"✅ {tool} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {tool}")

def create_pyinstaller_spec():
    """Create optimized PyInstaller spec file"""
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Data files to include
datas = [
    ('README.md', '.'),
    ('FEATURES.md', '.'),
    ('requirements_gui.txt', '.'),
]

# Hidden imports for tkinter and other modules
hiddenimports = [
    'tkinter',
    'tkinter.ttk', 
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'arxiv',
    'PyPDF2',
    'requests',
    'urllib3',
    'charset_normalizer',
    'idna',
    'certifi'
]

a = Analysis(
    ['enhanced_arxiv_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy'],  # Exclude unused large packages
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ArxivRoboticsFetcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""
    
    with open("arxiv_fetcher.spec", "w") as f:
        f.write(spec_content.strip())
    
    print("📄 PyInstaller spec file created")

def build_with_pyinstaller():
    """Build executable using PyInstaller"""
    print("🔨 Building executable with PyInstaller...")
    
    create_pyinstaller_spec()
    
    try:
        # Clean previous builds
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        
        # Build executable
        cmd = [sys.executable, "-m", "PyInstaller", "arxiv_fetcher.spec", "--clean", "--noconfirm"]
        
        print("   Building... (this may take a few minutes)")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_installer_package():
    """Create installer package with documentation"""
    print("📦 Creating installer package...")
    
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # Determine executable path and name
    if system == "windows":
        exe_name = "ArxivRoboticsFetcher.exe"
        exe_path = Path("dist") / exe_name
        package_name = f"ArxivRoboticsFetcher_v2.1_Windows_{arch}"
    elif system == "darwin":  # macOS
        exe_name = "ArxivRoboticsFetcher"
        exe_path = Path("dist") / exe_name
        package_name = f"ArxivRoboticsFetcher_v2.1_macOS_{arch}"
    else:  # Linux
        exe_name = "ArxivRoboticsFetcher"
        exe_path = Path("dist") / exe_name
        package_name = f"ArxivRoboticsFetcher_v2.1_Linux_{arch}"
    
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    # Create package directory
    package_dir = Path(package_name)
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / exe_name)
    
    # Copy documentation
    docs = ["README.md", "FEATURES.md", "requirements_gui.txt"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy2(doc, package_dir)
    
    # Create installation instructions
    install_instructions = f"""
🤖 arXiv Robotics Paper Fetcher v2.1 - Installation Guide

📋 SYSTEM REQUIREMENTS:
- Operating System: {platform.system()} {platform.release()}
- Architecture: {platform.machine()}
- Memory: 512MB RAM minimum, 1GB recommended
- Disk Space: 100MB free space

🚀 QUICK START:
1. Extract this package to your desired location
2. Run the executable: {exe_name}
3. The application will launch with a modern GUI interface

✨ FEATURES:
• Smart search across 7 research categories
• Automatic PDF download and text extraction
• Comprehensive metadata export
• Custom keyword and date filtering
• Cross-platform GUI with adaptive resolution
• Real-time progress monitoring

📁 FOLDER STRUCTURE:
The application will create the following folders:
- papers/pdfs/     - Downloaded PDF files
- papers/summaries/ - Generated summary templates
- papers/metadata.csv - Research metadata

🛠️ TROUBLESHOOTING:
- If the app doesn't start, try running it from command line to see error messages
- Ensure you have internet connection for downloading papers
- Check that your firewall allows the application to access the internet

📖 DOCUMENTATION:
- README.md - Detailed usage instructions
- FEATURES.md - Complete feature list and examples

🆘 SUPPORT:
For issues or questions, please check the documentation files included
in this package or visit the project repository.

Version: 2.1.0
Platform: {platform.platform()}
Built on: {platform.node()}
"""
    
    with open(package_dir / "INSTALL.txt", "w") as f:
        f.write(install_instructions.strip())
    
    # Create platform-specific launcher
    if system == "windows":
        launcher_content = f"""@echo off
echo Starting arXiv Robotics Paper Fetcher...
"{exe_name}"
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to close this window.
    pause > nul
)
"""
        with open(package_dir / "Run_ArxivFetcher.bat", "w") as f:
            f.write(launcher_content)
    
    else:  # Unix-like systems
        launcher_content = f"""#!/bin/bash
echo "Starting arXiv Robotics Paper Fetcher..."
cd "$(dirname "$0")"
./{exe_name}
"""
        launcher_path = package_dir / "Run_ArxivFetcher.sh"
        with open(launcher_path, "w") as f:
            f.write(launcher_content)
        os.chmod(launcher_path, 0o755)
    
    # Create ZIP archive
    zip_name = f"{package_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir.parent)
                zipf.write(file_path, arc_name)
    
    print(f"✅ Installer package created: {zip_name}")
    print(f"📁 Package directory: {package_dir}")
    
    # Display package contents
    print("\n📦 Package contents:")
    for item in package_dir.iterdir():
        if item.is_file():
            size = item.stat().st_size
            size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
            print(f"   📄 {item.name} ({size_str})")
    
    return True

def create_windows_installer():
    """Create Windows MSI installer (if on Windows)"""
    if platform.system() != "Windows":
        return
    
    print("🪟 Creating Windows installer...")
    
    try:
        # Try to use cx_Freeze to create MSI
        setup_msi = """
from cx_Freeze import setup, Executable
import sys

build_options = {
    'packages': ['tkinter', 'arxiv', 'PyPDF2'],
    'excludes': ['matplotlib', 'numpy', 'pandas'],
    'include_files': ['README.md', 'FEATURES.md']
}

base = 'Win32GUI'

executables = [
    Executable('enhanced_arxiv_gui.py',
              base=base,
              target_name='ArxivRoboticsFetcher.exe',
              icon=None)
]

setup(name='arXiv Robotics Paper Fetcher',
      version='2.1.0',
      description='Enhanced arXiv Robotics Paper Fetcher with GUI',
      options={'build_exe': build_options},
      executables=executables)
"""
        
        with open("setup_msi.py", "w") as f:
            f.write(setup_msi)
        
        # Build MSI
        subprocess.run([sys.executable, "setup_msi.py", "bdist_msi"], check=True)
        print("✅ Windows MSI installer created in dist/ folder")
        
    except Exception as e:
        print(f"⚠️ Could not create MSI installer: {e}")

def main():
    """Main build function"""
    print("🚀 arXiv Robotics Paper Fetcher - Executable Creator")
    print("=" * 60)
    
    # Install build tools
    install_build_tools()
    
    # Build executable
    if build_with_pyinstaller():
        print("\n📦 Creating distribution package...")
        if create_installer_package():
            print("\n🎉 Executable creation completed successfully!")
            
            # Create Windows installer if on Windows
            create_windows_installer()
            
            print("\n📋 What you got:")
            print("✅ Standalone executable (no Python installation required)")
            print("✅ Complete package with documentation")
            print("✅ ZIP archive for easy distribution")
            print("✅ Installation instructions")
            print("✅ Platform-specific launcher scripts")
            
            print("\n🚀 Distribution ready!")
            print("   Share the ZIP file with anyone - they can run it immediately!")
        else:
            print("❌ Package creation failed")
    else:
        print("❌ Executable build failed")

if __name__ == "__main__":
    main() 