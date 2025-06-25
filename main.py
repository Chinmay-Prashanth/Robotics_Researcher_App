#!/usr/bin/env python3
"""
🤖 AI-Powered Robotics Research Paper Fetcher
Main entry point for both CLI and GUI modes

Usage:
    python main.py              # Launch GUI (default)
    python main.py --cli         # Run CLI mode
    python main.py --help        # Show help
"""

import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="🤖 AI-Powered Robotics Research Paper Fetcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                    # Launch GUI interface
    python main.py --cli              # Run command-line interface
    python main.py --gui              # Explicitly launch GUI
    python main.py --install         # Run installation script
    
For more information, visit: https://github.com/yourusername/robotics_paper_fetcher
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true',
        help='Run in command-line interface mode'
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true',
        help='Run in graphical user interface mode (default)'
    )
    
    parser.add_argument(
        '--install', 
        action='store_true',
        help='Run the installation script'
    )
    
    parser.add_argument(
        '--version', 
        action='version',
        version='%(prog)s 2.0.0'
    )

    args = parser.parse_args()
    
    # Handle installation
    if args.install:
        print("🚀 Running installation script...")
        try:
            import subprocess
            subprocess.run([sys.executable, "scripts/install.py"], check=True)
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)
        return
    
    # Handle CLI mode
    if args.cli:
        print("🔍 Launching CLI mode...")
        try:
            from scripts.arxiv_robotics_fetcher import main as cli_main
            cli_main()
        except ImportError:
            print("❌ CLI module not found. Please check scripts/arxiv_robotics_fetcher.py")
            sys.exit(1)
        except Exception as e:
            print(f"❌ CLI execution failed: {e}")
            sys.exit(1)
        return
    
    # Default: Launch GUI
    print("🎨 Launching GUI interface...")
    try:
        import tkinter as tk
        # Test if GUI is available
        root = tk.Tk()
        root.withdraw()  # Hide test window
        root.destroy()
        
        # Import and run the GUI
        import subprocess
        subprocess.run([sys.executable, "reliable_arxiv_gui.py"])
        
    except ImportError:
        print("❌ GUI not available. Tkinter is not installed.")
        print("💡 Try running with --cli flag for command-line interface.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        print("💡 Try running with --cli flag for command-line interface.")
        sys.exit(1)

if __name__ == "__main__":
    main() 