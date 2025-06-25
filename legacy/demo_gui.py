#!/usr/bin/env python3
"""
Demo script to test the GUI functionality
This will fetch just 2 papers for demonstration
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def test_gui():
    """Test if the GUI launches correctly"""
    try:
        print("🧪 Testing GUI launch...")
        # Just import to test if all dependencies are available
        import arxiv
        from tkinter import ttk, filedialog, scrolledtext
        import threading
        from datetime import datetime
        
        print("✅ All imports successful")
        print("✅ GUI should work correctly")
        
        # Ask user if they want to launch the GUI
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        result = messagebox.askyesno(
            "GUI Test", 
            "Dependencies check passed!\n\nWould you like to launch the full GUI now?\n\n"
            "(Note: Close this dialog and the GUI window when done testing)"
        )
        
        if result:
            root.destroy()
            # Launch the GUI
            subprocess.run([sys.executable, "arxiv_gui_fetcher.py"])
        else:
            root.destroy()
            
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements_gui.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 arXiv Robotics Fetcher - Demo")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("arxiv_gui_fetcher.py"):
        print("❌ Please run this script from the project root directory")
        return
    
    test_gui()

if __name__ == "__main__":
    main() 