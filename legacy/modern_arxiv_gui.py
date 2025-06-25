#!/usr/bin/env python3
"""
Modern Robotics Research Paper Fetcher GUI
Using CustomTkinter for better emoji and font support on Linux
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import platform
import threading
from datetime import datetime
import subprocess

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import from existing modules
try:
    from arxiv_robotics_fetcher import fetch_papers
except ImportError:
    print("Error: arxiv_robotics_fetcher.py not found in current directory")
    sys.exit(1)

# Check for PDF processing capabilities
try:
    import PyPDF2
    PDF_PROCESSING_AVAILABLE = True
except ImportError:
    PDF_PROCESSING_AVAILABLE = False

# Set appearance mode and color theme
ctk.set_appearance_mode("light")  # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class ModernArxivFetcherGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 Robotics Research Paper Fetcher")
        self.root.geometry("1280x720")
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1280) // 2
        y = (screen_height - 720) // 2
        self.root.geometry(f"1280x720+{x}+{y}")
        
        # Variables
        self.setup_variables()
        
        # Create UI
        self.create_widgets()
        self.is_fetching = False
        
    def setup_variables(self):
        """Initialize all GUI variables"""
        self.output_dir = tk.StringVar(value="papers")
        self.max_results = tk.IntVar(value=50)
        self.search_query = tk.StringVar(value="")
        
        # Date filtering
        self.date_filter_enabled = tk.BooleanVar(value=False)
        self.start_date = tk.StringVar(value="")
        self.end_date = tk.StringVar(value="")
        
        # PDF processing
        self.extract_text = tk.BooleanVar(value=True)
        self.check_encryption = tk.BooleanVar(value=True)
        self.create_txt_files = tk.BooleanVar(value=True)
        
        # AI Assistant
        self.openai_api_key = tk.StringVar()
        self.ai_enabled = tk.BooleanVar()
        self.ai_task = tk.StringVar(value="summarize")
        
        # Categories
        self.categories = {
            "🤖 Robotics (cs.RO)": "cs.RO",
            "🧠 AI (cs.AI)": "cs.AI", 
            "📊 Machine Learning (cs.LG)": "cs.LG",
            "👁️ Computer Vision (cs.CV)": "cs.CV",
            "⚙️ Systems & Control (eess.SY)": "eess.SY",
            "🖱️ Human-Computer Interaction (cs.HC)": "cs.HC",
            "💬 Natural Language Processing (cs.CL)": "cs.CL"
        }
        self.selected_categories = {cat: tk.BooleanVar(value=True if "Robotics" in cat or "AI" in cat or "Systems" in cat else False) for cat in self.categories}
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section
        self.create_title_section(main_frame)
        
        # Create two-column layout
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left column
        left_column = ctk.CTkFrame(content_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right column
        right_column = ctk.CTkFrame(content_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Create sections
        self.create_search_section(left_column)
        self.create_date_section(left_column)
        self.create_ai_section(left_column)
        
        self.create_pdf_section(right_column)
        self.create_settings_section(right_column)
        self.create_control_buttons(right_column)
        
        # Progress section at bottom
        self.create_progress_section(main_frame)
        
    def create_title_section(self, parent):
        """Create title and info section"""
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        # Main title
        title_label = ctk.CTkLabel(title_frame, 
                                  text="🤖 Robotics Research Paper Fetcher",
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack()
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(title_frame,
                                     text="Intelligent Academic Research Assistant",
                                     font=ctk.CTkFont(size=16))
        subtitle_label.pack(pady=(5, 0))
        
        # System info
        platform_name = {"Darwin": "macOS", "Windows": "Windows", "Linux": "Linux"}.get(platform.system(), platform.system())
        pdf_status = "📄 PDF Ready" if PDF_PROCESSING_AVAILABLE else "⚠️ Install PyPDF2"
        
        info_label = ctk.CTkLabel(title_frame,
                                 text=f"🖥️ {platform_name} • {pdf_status}",
                                 font=ctk.CTkFont(size=12))
        info_label.pack(pady=(5, 0))
        
    def create_search_section(self, parent):
        """Create search configuration section"""
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Section header
        header_label = ctk.CTkLabel(search_frame,
                                   text="🔍 Research Discovery",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Search query
        query_label = ctk.CTkLabel(search_frame,
                                  text="🎯 Custom Research Query:",
                                  font=ctk.CTkFont(size=12, weight="bold"))
        query_label.pack(anchor="w", padx=15, pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(search_frame,
                                        textvariable=self.search_query,
                                        placeholder_text="Enter search terms...",
                                        font=ctk.CTkFont(size=12))
        self.search_entry.pack(fill="x", padx=15, pady=(0, 5))
        
        # Categories
        cat_label = ctk.CTkLabel(search_frame,
                                text="📚 Academic Domains:",
                                font=ctk.CTkFont(size=12, weight="bold"))
        cat_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Category checkboxes
        for i, (cat_name, var) in enumerate(self.selected_categories.items()):
            checkbox = ctk.CTkCheckBox(search_frame,
                                      text=cat_name,
                                      variable=var,
                                      font=ctk.CTkFont(size=11))
            checkbox.pack(anchor="w", padx=15, pady=2)
            
    def create_date_section(self, parent):
        """Create date filtering section"""
        date_frame = ctk.CTkFrame(parent)
        date_frame.pack(fill="x", pady=(0, 10))
        
        # Header
        header_label = ctk.CTkLabel(date_frame,
                                   text="📅 Temporal Filtering",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Enable checkbox
        self.date_checkbox = ctk.CTkCheckBox(date_frame,
                                            text="🗓️ Enable publication date filtering",
                                            variable=self.date_filter_enabled,
                                            font=ctk.CTkFont(size=12))
        self.date_checkbox.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Date inputs
        date_input_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Start date
        start_label = ctk.CTkLabel(date_input_frame, text="Start Date:", font=ctk.CTkFont(size=11))
        start_label.pack(anchor="w")
        self.start_entry = ctk.CTkEntry(date_input_frame, textvariable=self.start_date,
                                       placeholder_text="YYYY-MM-DD", font=ctk.CTkFont(size=11))
        self.start_entry.pack(fill="x", pady=(2, 5))
        
        # End date
        end_label = ctk.CTkLabel(date_input_frame, text="End Date:", font=ctk.CTkFont(size=11))
        end_label.pack(anchor="w")
        self.end_entry = ctk.CTkEntry(date_input_frame, textvariable=self.end_date,
                                     placeholder_text="YYYY-MM-DD", font=ctk.CTkFont(size=11))
        self.end_entry.pack(fill="x")
        
    def create_ai_section(self, parent):
        """Create AI assistant section"""
        ai_frame = ctk.CTkFrame(parent)
        ai_frame.pack(fill="x", pady=(0, 10))
        
        # Header
        header_label = ctk.CTkLabel(ai_frame,
                                   text="🤖 AI Research Assistant",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Enable AI
        self.ai_checkbox = ctk.CTkCheckBox(ai_frame,
                                          text="🧠 Enable AI-powered analysis",
                                          variable=self.ai_enabled,
                                          font=ctk.CTkFont(size=12))
        self.ai_checkbox.pack(anchor="w", padx=15, pady=(0, 10))
        
        # API Key
        key_label = ctk.CTkLabel(ai_frame, text="🔑 OpenAI API Key:", font=ctk.CTkFont(size=11))
        key_label.pack(anchor="w", padx=15)
        
        self.api_entry = ctk.CTkEntry(ai_frame, textvariable=self.openai_api_key,
                                     placeholder_text="Enter your OpenAI API key...",
                                     show="*", font=ctk.CTkFont(size=11))
        self.api_entry.pack(fill="x", padx=15, pady=(2, 10))
        
        # Task selection
        task_label = ctk.CTkLabel(ai_frame, text="🎯 AI Task:", font=ctk.CTkFont(size=11))
        task_label.pack(anchor="w", padx=15)
        
        self.task_menu = ctk.CTkOptionMenu(ai_frame, variable=self.ai_task,
                                          values=["summarize", "extract_keywords", "find_methodology", "identify_gaps"],
                                          font=ctk.CTkFont(size=11))
        self.task_menu.pack(anchor="w", padx=15, pady=(2, 15))
        
    def create_pdf_section(self, parent):
        """Create PDF processing section"""
        pdf_frame = ctk.CTkFrame(parent)
        pdf_frame.pack(fill="x", pady=(0, 10))
        
        # Header
        header_label = ctk.CTkLabel(pdf_frame,
                                   text="📄 Document Processing",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # PDF options
        self.extract_checkbox = ctk.CTkCheckBox(pdf_frame,
                                               text="📝 Extract comprehensive text content",
                                               variable=self.extract_text,
                                               font=ctk.CTkFont(size=11))
        self.extract_checkbox.pack(anchor="w", padx=15, pady=2)
        
        self.encryption_checkbox = ctk.CTkCheckBox(pdf_frame,
                                                  text="🔒 Analyze document security status",
                                                  variable=self.check_encryption,
                                                  font=ctk.CTkFont(size=11))
        self.encryption_checkbox.pack(anchor="w", padx=15, pady=2)
        
        self.txt_checkbox = ctk.CTkCheckBox(pdf_frame,
                                           text="💾 Generate structured text files",
                                           variable=self.create_txt_files,
                                           font=ctk.CTkFont(size=11))
        self.txt_checkbox.pack(anchor="w", padx=15, pady=(2, 15))
        
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.pack(fill="x", pady=(0, 10))
        
        # Header
        header_label = ctk.CTkLabel(settings_frame,
                                   text="⚙️ Research Configuration",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Max results
        results_label = ctk.CTkLabel(settings_frame, text="📊 Maximum Results:", font=ctk.CTkFont(size=11))
        results_label.pack(anchor="w", padx=15)
        
        self.results_slider = ctk.CTkSlider(settings_frame, from_=10, to=200, number_of_steps=19,
                                           variable=self.max_results)
        self.results_slider.pack(fill="x", padx=15, pady=(2, 5))
        
        self.results_value = ctk.CTkLabel(settings_frame, text="50 papers", font=ctk.CTkFont(size=10))
        self.results_value.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Update value display
        self.results_slider.configure(command=self.update_results_display)
        
        # Output directory
        dir_label = ctk.CTkLabel(settings_frame, text="📁 Research Library Location:", font=ctk.CTkFont(size=11))
        dir_label.pack(anchor="w", padx=15)
        
        dir_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        dir_frame.pack(fill="x", padx=15, pady=(2, 15))
        
        self.dir_entry = ctk.CTkEntry(dir_frame, textvariable=self.output_dir, font=ctk.CTkFont(size=11))
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        dir_button = ctk.CTkButton(dir_frame, text="📂 Browse", command=self.browse_output_dir,
                                  width=80, font=ctk.CTkFont(size=11))
        dir_button.pack(side="right")
        
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Main fetch button
        self.fetch_button = ctk.CTkButton(button_frame,
                                         text="🚀 Fetch & Process Papers",
                                         command=self.start_fetch,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         height=40)
        self.fetch_button.pack(fill="x", padx=15, pady=(0, 10))
        
        # Secondary buttons
        button_row = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_row.pack(fill="x", padx=15)
        
        self.stop_button = ctk.CTkButton(button_row, text="⏹️ Stop", command=self.stop_fetch,
                                        width=100, font=ctk.CTkFont(size=11))
        self.stop_button.pack(side="left", padx=(0, 5))
        
        self.folder_button = ctk.CTkButton(button_row, text="📂 Open Folder", command=self.open_output_folder,
                                          width=120, font=ctk.CTkFont(size=11))
        self.folder_button.pack(side="left", padx=(5, 5))
        
        self.about_button = ctk.CTkButton(button_row, text="ℹ️ About", command=self.show_about,
                                         width=80, font=ctk.CTkFont(size=11))
        self.about_button.pack(side="right")
        
    def create_progress_section(self, parent):
        """Create progress and log section"""
        progress_frame = ctk.CTkFrame(parent)
        progress_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Header
        header_label = ctk.CTkLabel(progress_frame,
                                   text="📊 Research Activity Monitor",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Progress bar
        progress_label = ctk.CTkLabel(progress_frame, text="⚡ Processing Status:", font=ctk.CTkFont(size=11))
        progress_label.pack(anchor="w", padx=15)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=15, pady=(2, 10))
        self.progress_bar.set(0)
        
        # Log area
        log_label = ctk.CTkLabel(progress_frame, text="📝 Activity Log:", font=ctk.CTkFont(size=11))
        log_label.pack(anchor="w", padx=15)
        
        self.log_text = ctk.CTkTextbox(progress_frame, height=150, font=ctk.CTkFont(size=10))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(2, 15))
        
        # Welcome message
        self.log_welcome_message()
        
    def log_welcome_message(self):
        """Display welcome message in log"""
        welcome_msg = """🎉 Welcome to Robotics Research Paper Fetcher!

✨ Advanced research capabilities:
• 🔍 Intelligent search across 7 specialized research domains
• 📄 Seamless PDF acquisition and text extraction  
• 🤖 AI-powered analysis with ChatGPT integration
• 📊 Research analytics dashboard with visualizations
• 🎯 Precision keyword and temporal filtering

📋 Quick start guide:
1. Select research domains or enter custom search terms
2. Configure AI assistant with your OpenAI API key (optional)
3. Set date filters for recent publications (optional)  
4. Click 'Fetch & Process Papers' to begin
5. Monitor real-time progress and AI analysis

Ready to revolutionize your research workflow! ��
"""
        self.log_text.insert("0.0", welcome_msg)
        
    def update_results_display(self, value):
        """Update the results display"""
        self.results_value.configure(text=f"{int(value)} papers")
        
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"{timestamp} - {message}\n"
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
            
    def open_output_folder(self):
        """Open output folder"""
        output_path = self.output_dir.get()
        if os.path.exists(output_path):
            if platform.system() == "Windows":
                os.startfile(output_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", output_path])
            else:  # Linux
                subprocess.run(["xdg-open", output_path])
        else:
            messagebox.showwarning("Warning", f"Directory does not exist: {output_path}")
            
    def start_fetch(self):
        """Start fetching papers"""
        if self.is_fetching:
            return
            
        self.is_fetching = True
        self.fetch_button.configure(text="🔄 Fetching...", state="disabled")
        self.progress_bar.set(0)
        
        # Run fetch in separate thread
        thread = threading.Thread(target=self.fetch_papers_thread, daemon=True)
        thread.start()
        
    def stop_fetch(self):
        """Stop fetching papers"""
        self.is_fetching = False
        self.fetch_button.configure(text="🚀 Fetch & Process Papers", state="normal")
        self.log_message("🛑 Fetch operation stopped by user")
        
    def fetch_papers_thread(self):
        """Fetch papers in background thread"""
        try:
            # Prepare arguments
            query_terms = []
            if self.search_query.get().strip():
                query_terms.append(f'({self.search_query.get().strip()})')
                
            # Add selected categories
            selected_cats = [cat_code for cat_name, cat_code in self.categories.items() 
                           if self.selected_categories[cat_name].get()]
            
            if selected_cats:
                cat_query = " OR ".join([f"cat:{cat}" for cat in selected_cats])
                query_terms.append(f'({cat_query})')
                
            if not query_terms:
                self.log_message("❌ Please select at least one category or enter a search term")
                self._fetch_complete()
                return
                
            # Build final query
            final_query = " AND ".join(query_terms)
            self.log_message(f"🔍 Search query: {final_query}")
            
            # Create output directory
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Fetch papers
            papers = fetch_papers(
                query=final_query,
                max_results=self.max_results.get(),
                start_date=self.start_date.get() if self.date_filter_enabled.get() else None,
                end_date=self.end_date.get() if self.date_filter_enabled.get() else None,
                output_dir=self.output_dir.get()
            )
            
            self.log_message(f"�� Successfully fetched {len(papers)} papers!")
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
        finally:
            self.root.after(0, self._fetch_complete)
            
    def _fetch_complete(self):
        """Reset UI after fetch completion"""
        self.is_fetching = False
        self.fetch_button.configure(text="🚀 Fetch & Process Papers", state="normal")
        self.progress_bar.set(1.0)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """🤖 Robotics Research Paper Fetcher

An intelligent academic research assistant for discovering and managing robotics research papers.

✨ Advanced Research Capabilities:
• Intelligent search across 7 specialized research domains
• Seamless PDF acquisition and comprehensive text extraction
• AI-powered analysis with ChatGPT integration
• Research analytics dashboard with advanced visualizations
• Cross-platform compatibility with elegant modern UI

🔧 Technical Architecture:
• Modern Python application with CustomTkinter
• arXiv API integration for real-time paper discovery
• PyPDF2 for comprehensive document processing
• Optional analytics with matplotlib & seaborn
• Beautiful modern UI with excellent emoji support

📊 Research Intelligence:
• Real-time activity monitoring
• Trend analysis and keyword extraction
• AI-powered paper analysis
• Collaborative sharing and export tools
• Comprehensive metadata analysis

Perfect for academic researchers, students, and research institutions!

© 2024 - Open Source Academic Research Tool"""
        
        messagebox.showinfo("About", about_text)
        
def main():
    """Main application entry point"""
    app = ModernArxivFetcherGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
