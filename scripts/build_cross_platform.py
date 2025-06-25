#!/usr/bin/env python3
"""
Cross-Platform Executable Builder for arXiv Fetcher
Builds executables for Windows, macOS, and Ubuntu/Linux with resolution awareness
"""

import subprocess
import sys
import os
import shutil
import platform
import zipfile
from pathlib import Path

def install_requirements():
    """Install all required packages for building"""
    print("📦 Installing build requirements...")
    
    packages = [
        "arxiv",
        "PyPDF2", 
        "pyinstaller",
        "cx_Freeze"  # Alternative to PyInstaller
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Failed to install {package}: {e}")
            
    print("✅ Build requirements installed")

def create_spec_file():
    """Create PyInstaller spec file for better control"""
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['enhanced_arxiv_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.'), ('requirements_gui.txt', '.')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.scrolledtext'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ArxivFetcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI app, no console
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
    
    print("📄 Created PyInstaller spec file")

def build_with_pyinstaller():
    """Build executable using PyInstaller"""
    print("🔨 Building with PyInstaller...")
    
    create_spec_file()
    
    try:
        # Build using spec file for better control
        cmd = [sys.executable, "-m", "PyInstaller", "arxiv_fetcher.spec", "--clean"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyInstaller build successful!")
            return True
        else:
            print(f"❌ PyInstaller failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ PyInstaller error: {e}")
        return False

def build_with_cx_freeze():
    """Alternative build method using cx_Freeze"""
    print("🔨 Building with cx_Freeze (alternative method)...")
    
    setup_content = """
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'packages': ['tkinter', 'arxiv', 'PyPDF2'],
    'excludes': [],
    'include_files': ['README.md', 'requirements_gui.txt']
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('enhanced_arxiv_gui.py', 
              base=base, 
              target_name='ArxivFetcher')
]

setup(name='ArxivFetcher',
      version='2.1',
      description='Enhanced arXiv Robotics Paper Fetcher',
      options={'build_exe': build_options},
      executables=executables)
"""
    
    with open("setup_cx.py", "w") as f:
        f.write(setup_content.strip())
    
    try:
        cmd = [sys.executable, "setup_cx.py", "build"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ cx_Freeze build successful!")
            return True
        else:
            print(f"❌ cx_Freeze failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ cx_Freeze error: {e}")
        return False

def create_portable_package():
    """Create portable packages for different platforms"""
    current_platform = platform.system().lower()
    
    # Determine executable location and name
    exe_locations = {
        'pyinstaller': {
            'windows': 'dist/ArxivFetcher.exe',
            'linux': 'dist/ArxivFetcher',
            'darwin': 'dist/ArxivFetcher'  # macOS
        },
        'cx_freeze': {
            'windows': 'build/exe.win*/ArxivFetcher.exe',
            'linux': 'build/exe.linux*/ArxivFetcher',
            'darwin': 'build/exe.macosx*/ArxivFetcher'  # macOS
        }
    }
    
    package_name = f"ArxivFetcher_v2.1_{current_platform}"
    
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    
    os.makedirs(package_name)
    
    # Copy executable
    exe_found = False
    for build_method, locations in exe_locations.items():
        for platform_key, exe_path in locations.items():
            if platform_key in current_platform:
                # Handle glob patterns for cx_Freeze
                if '*' in exe_path:
                    import glob
                    matching_files = glob.glob(exe_path)
                    if matching_files:
                        exe_path = matching_files[0]
                
                if os.path.exists(exe_path):
                    if current_platform == "windows":
                        exe_name = "ArxivFetcher.exe"
                    elif current_platform == "darwin":
                        exe_name = "ArxivFetcher.app" if exe_path.endswith('.app') else "ArxivFetcher"
                    else:
                        exe_name = "ArxivFetcher"
                    shutil.copy2(exe_path, os.path.join(package_name, exe_name))
                    exe_found = True
                    print(f"✅ Copied executable from {exe_path}")
                    break
        if exe_found:
            break
    
    if not exe_found:
        print("❌ No executable found to package")
        return False
    
    # Copy documentation and requirements
    files_to_copy = [
        "README.md",
        "requirements_gui.txt", 
        "enhanced_arxiv_gui.py"  # Source code for reference
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, package_name)
    
    # Create usage instructions
    create_usage_instructions(package_name, current_platform)
    
    # Create ZIP archive
    zip_name = f"{package_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    print(f"📦 Created portable package: {zip_name}")
    return True

def create_usage_instructions(package_dir, platform_name):
    """Create platform-specific usage instructions"""
    
    if platform_name == "windows":
        instructions = """
=== arXiv Robotics Paper Fetcher v2.1 - Windows ===

QUICK START:
1. Double-click "ArxivFetcher.exe" to launch the application
2. No installation required - this is a portable version
3. Select your search criteria and click "Fetch & Process Papers"
4. App automatically adapts to your screen resolution and DPI

FEATURES:
• Search papers by categories (Robotics, AI, ML, etc.)
• Custom keyword search
• Date range filtering
• PDF text extraction and analysis
• Automatic summary template generation
• Encryption detection
• High-DPI display support

SYSTEM REQUIREMENTS:
• Windows 7/8/10/11 (64-bit)
• No Python installation required
• Internet connection for downloading papers
• Supports all screen resolutions and DPI settings

TROUBLESHOOTING:
• If Windows Defender blocks the app, click "More info" then "Run anyway"
• For antivirus warnings, add the folder to your antivirus exceptions
• If the app doesn't start, try running as administrator
• App automatically detects and adapts to your display settings

SUPPORT:
• GitHub: github.com/your-username/arxiv-robotics-fetcher
• Report issues on GitHub Issues page

Created for researchers to streamline literature review.
"""
    elif platform_name == "darwin":  # macOS
        instructions = """
=== arXiv Robotics Paper Fetcher v2.1 - macOS ===

QUICK START:
1. Double-click "ArxivFetcher" to launch the application
2. If prompted, allow the app to run (System Preferences > Security & Privacy)
3. No installation required - this is a portable version
4. Select your search criteria and click "Fetch & Process Papers"
5. App automatically adapts to your screen resolution and Retina display

FEATURES:
• Search papers by categories (Robotics, AI, ML, etc.)
• Custom keyword search
• Date range filtering  
• PDF text extraction and analysis
• Automatic summary template generation
• Encryption detection
• Retina display and high-DPI support
• Multi-monitor support

SYSTEM REQUIREMENTS:
• macOS 10.12 Sierra or later
• No Python installation required
• Internet connection for downloading papers
• Supports all Mac displays including Retina

TROUBLESHOOTING:
• If "unidentified developer" warning: Right-click → Open → Open
• For Gatekeeper issues: System Preferences → Security → Allow
• If app doesn't start: Try running from Terminal with ./ArxivFetcher
• App automatically detects your display settings

ALTERNATIVE RUN METHODS:
• From source: python3 enhanced_arxiv_gui.py
• Install dependencies: pip3 install -r requirements_gui.txt

SUPPORT:
• GitHub: github.com/your-username/arxiv-robotics-fetcher
• Report issues on GitHub Issues page

Created for researchers to streamline literature review.
"""
    else:  # Linux/Ubuntu
        instructions = """
=== arXiv Robotics Paper Fetcher v2.1 - Linux ===

QUICK START:
1. Open terminal in this folder
2. Make executable: chmod +x ArxivFetcher
3. Run: ./ArxivFetcher
   OR double-click the ArxivFetcher file in file manager
4. App automatically adapts to your screen resolution and DPI

FEATURES:
• Search papers by categories (Robotics, AI, ML, etc.)
• Custom keyword search  
• Date range filtering
• PDF text extraction and analysis
• Automatic summary template generation
• Encryption detection
• Multi-monitor and high-DPI support

SYSTEM REQUIREMENTS:
• Ubuntu 18.04+ or equivalent Linux distribution
• X11 display server (for GUI)
• Internet connection for downloading papers
• Supports all screen resolutions and DPI settings

ALTERNATIVE RUN METHODS:
• From source: python3 enhanced_arxiv_gui.py
• Install dependencies: pip3 install -r requirements_gui.txt

TROUBLESHOOTING:
• If "Permission denied": chmod +x ArxivFetcher
• If missing GUI libraries: sudo apt install python3-tk
• For dependency issues, run from source code
• App automatically detects your display configuration

SUPPORT:
• GitHub: github.com/your-username/arxiv-robotics-fetcher
• Report issues on GitHub Issues page

Created for researchers to streamline literature review.
"""
    
    with open(os.path.join(package_dir, "USAGE.txt"), "w") as f:
        f.write(instructions.strip())

def cleanup_build_files():
    """Clean up build artifacts"""
    cleanup_dirs = ["build", "dist", "__pycache__"]
    cleanup_files = ["arxiv_fetcher.spec", "setup_cx.py"]
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned up {dir_name}/")
    
    for file_name in cleanup_files:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🧹 Cleaned up {file_name}")

def main():
    print("🚀 Cross-Platform arXiv Fetcher Builder")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("📱 Resolution-Aware & DPI-Adaptive Build")
    print()
    
    # Check if we have the main GUI file
    if not os.path.exists("enhanced_arxiv_gui.py"):
        print("❌ enhanced_arxiv_gui.py not found!")
        print("   Please run this script from the project directory.")
        return
    
    try:
        # Install requirements
        install_requirements()
        print()
        
        # Try building with PyInstaller first
        print("🔧 Attempting build with PyInstaller...")
        success = build_with_pyinstaller()
        
        if not success:
            print("\n🔧 Trying alternative method with cx_Freeze...")
            success = build_with_cx_freeze()
        
        if success:
            print("\n📦 Creating portable package...")
            if create_portable_package():
                current_os = {"Windows": "Windows", "Darwin": "macOS", "Linux": "Linux"}.get(platform.system(), platform.system())
                print("\n🎉 Build completed successfully!")
                print(f"✅ Executable ready for {current_os}")
                print("📱 Resolution-aware and DPI-adaptive")
                print("📁 Check the .zip file for the portable version")
            else:
                print("\n⚠️ Build succeeded but packaging failed")
        else:
            print("\n❌ All build methods failed")
            print("💡 You can still run the GUI directly with: python3 enhanced_arxiv_gui.py")
            
    except KeyboardInterrupt:
        print("\n⏹ Build cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        print("\n🧹 Cleaning up build files...")
        cleanup_build_files()

if __name__ == "__main__":
    main() 