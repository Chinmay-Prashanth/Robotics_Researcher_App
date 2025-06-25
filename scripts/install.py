#!/usr/bin/env python3
"""
🤖 Enhanced arXiv Robotics Paper Fetcher - Universal Installer
Provides multiple installation methods for maximum compatibility
"""

import subprocess
import sys
import os
import platform
import shutil
from pathlib import Path

def print_banner():
    """Display installation banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   🤖 arXiv Robotics Paper Fetcher v2.1                      ║
║                         Universal Installer                                  ║
║                                                                              ║
║  🔍 Smart search across 7 research categories                               ║
║  📄 Automatic PDF download and text extraction                              ║
║  📊 Comprehensive metadata export                                           ║
║  🎯 Custom keyword and date filtering                                       ║
║  🖥️ Cross-platform GUI with adaptive resolution                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        print("   Please install pip and try again")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    dependencies = [
        "arxiv>=1.4.0",
        "PyPDF2>=3.0.0",
        "requests>=2.25.0"
    ]
    
    for dep in dependencies:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
            print(f"   ✅ {dep} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {dep}")
            return False
    
    print("✅ All dependencies installed successfully")
    return True

def install_package_mode():
    """Install as a Python package"""
    print("\n🔧 Installing arXiv Fetcher as a Python package...")
    
    try:
        # Install in development mode
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                      check=True, capture_output=True)
        print("✅ Package installed successfully!")
        print("\n🚀 You can now run:")
        print("   📱 GUI mode: arxiv-fetcher")
        print("   📱 GUI mode: arxiv-fetcher-gui") 
        print("   💻 CLI mode: arxiv-fetcher-cli")
        return True
    except subprocess.CalledProcessError:
        print("❌ Package installation failed")
        return False

def create_desktop_entry_linux():
    """Create desktop entry for Linux"""
    if platform.system() != "Linux":
        return
    
    desktop_entry = f"""[Desktop Entry]
Name=arXiv Robotics Fetcher
Comment=Enhanced arXiv Robotics Paper Fetcher with GUI
Exec={sys.executable} {os.path.abspath('reliable_arxiv_gui.py')}
Icon=applications-science
Terminal=false
Type=Application
Categories=Education;Science;Research;
Keywords=arxiv;robotics;papers;research;pdf;
StartupWMClass=arxiv-fetcher
"""
    
    desktop_dir = Path.home() / ".local/share/applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_file = desktop_dir / "arxiv-fetcher.desktop"
    with open(desktop_file, "w") as f:
        f.write(desktop_entry)
    
    # Make executable
    os.chmod(desktop_file, 0o755)
    print(f"✅ Desktop entry created: {desktop_file}")

def create_start_menu_windows():
    """Create Start Menu entry for Windows"""
    if platform.system() != "Windows":
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        start_menu = winshell.start_menu()
        
        # Create shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(os.path.join(start_menu, "arXiv Robotics Fetcher.lnk"))
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{os.path.abspath("reliable_arxiv_gui.py")}"'
        shortcut.WorkingDirectory = os.path.abspath(".")
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("✅ Start Menu entry created")
    except ImportError:
        print("⚠️  Could not create Start Menu entry (winshell not available)")

def create_application_macos():
    """Create .app bundle for macOS"""
    if platform.system() != "Darwin":
        return
    
    app_name = "arXiv Robotics Fetcher.app"
    app_dir = Path(app_name)
    
    if app_dir.exists():
        shutil.rmtree(app_dir)
    
    # Create app bundle structure
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    for dir_path in [contents_dir, macos_dir, resources_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>arXiv Robotics Fetcher</string>
    <key>CFBundleExecutable</key>
    <string>arxiv-fetcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.arxiv.robotics.fetcher</string>
    <key>CFBundleName</key>
    <string>arXiv Robotics Fetcher</string>
    <key>CFBundleVersion</key>
    <string>2.1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>"""
    
    with open(contents_dir / "Info.plist", "w") as f:
        f.write(info_plist)
    
    # Create executable script
    launcher_script = f"""#!/bin/bash
cd "{os.path.abspath('.')}"
{sys.executable} reliable_arxiv_gui.py
"""
    
    launcher_path = macos_dir / "arxiv-fetcher"
    with open(launcher_path, "w") as f:
        f.write(launcher_script)
    
    os.chmod(launcher_path, 0o755)
    print(f"✅ macOS app bundle created: {app_name}")

def create_portable_mode():
    """Create portable installation"""
    print("\n📁 Creating portable installation...")
    
    portable_dir = Path("ArxivFetcher_Portable")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir()
    
    # Copy essential files
    essential_files = [
        "reliable_arxiv_gui.py",
        "arxiv_robotics_fetcher.py", 
        "pdf_analyzer.py",
        "requirements_gui.txt",
        "README.md",
        "FEATURES.md"
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, portable_dir)
    
    # Copy directories
    for dir_name in ["papers", "summaries"]:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, portable_dir / dir_name)
    
    # Create launcher scripts
    windows_launcher = portable_dir / "ArxivFetcher.bat"
    with open(windows_launcher, "w") as f:
        f.write(f'@echo off\n{sys.executable} reliable_arxiv_gui.py\npause')
    
    unix_launcher = portable_dir / "ArxivFetcher.sh"
    with open(unix_launcher, "w") as f:
        f.write(f'#!/bin/bash\n{sys.executable} reliable_arxiv_gui.py')
    os.chmod(unix_launcher, 0o755)
    
    print(f"✅ Portable installation created in: {portable_dir}")
    return True

def show_installation_options():
    """Display installation options menu"""
    print("\n🛠️  Installation Options:")
    print("1. 📦 Full Package Installation (Recommended)")
    print("2. 📁 Portable Mode (No system changes)")
    print("3. 🖥️  Create Desktop/System Integration")
    print("4. 🚀 Quick Start (Just run dependencies)")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nSelect installation method (1-5): ").strip()
            if choice in ["1", "2", "3", "4", "5"]:
                return int(choice)
            else:
                print("Please enter a number between 1 and 5")
        except KeyboardInterrupt:
            print("\n\n👋 Installation cancelled")
            sys.exit(0)

def main():
    """Main installation function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Show installation options
    choice = show_installation_options()
    
    if choice == 5:
        print("👋 Installation cancelled")
        return
    
    # Install dependencies for all modes
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    success = False
    
    if choice == 1:
        # Full package installation
        success = install_package_mode()
        if success:
            create_desktop_entry_linux()
            create_start_menu_windows()
            create_application_macos()
    
    elif choice == 2:
        # Portable mode
        success = create_portable_mode()
    
    elif choice == 3:
        # System integration only
        create_desktop_entry_linux()
        create_start_menu_windows()
        create_application_macos()
        success = True
    
    elif choice == 4:
        # Quick start
        print("✅ Dependencies installed! You can now run:")
        print(f"   {sys.executable} reliable_arxiv_gui.py")
        success = True
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("\n📚 Quick Start Guide:")
        print("1. Launch the application")
        print("2. Select research categories or enter custom search terms")
        print("3. Optionally set date filters")
        print("4. Click 'Fetch & Process Papers'")
        print("5. Monitor progress and enjoy your research acceleration!")
        print("\n📖 For more information, see README.md and FEATURES.md")
    else:
        print("\n❌ Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 