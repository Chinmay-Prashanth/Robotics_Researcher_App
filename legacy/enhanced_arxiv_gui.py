#!/usr/bin/env python3
"""
Enhanced arXiv Robotics Paper Fetcher - GUI Version with PDF Processing
A comprehensive tool for researchers with PDF analysis and text extraction
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import arxiv
import os
import csv
import threading
from datetime import datetime, timedelta
import webbrowser
import platform

# PDF processing imports
try:
    import PyPDF2
    PDF_PROCESSING_AVAILABLE = True
except ImportError:
    PDF_PROCESSING_AVAILABLE = False

class EnhancedArxivFetcherGUI:
    def __init__(self, root, colors=None):
        self.root = root
        self.root.title("[AI] Robotics Research Paper Fetcher")
        
        # Store color scheme
        self.colors = colors or {
            'primary': '#2196F3',
            'secondary': '#4CAF50', 
            'accent': '#FF9800',
            'surface': '#FFFFFF',
            'background': '#F5F5F5',
            'text': '#212121',
            'text_secondary': '#757575'
        }
        
        # Auto-detect screen resolution and set adaptive window size
        self.setup_adaptive_ui()
        self.root.resizable(True, True)
        
        # Variables
        self.output_dir = tk.StringVar(value="papers")
        self.summary_dir = tk.StringVar(value="summaries")
        self.max_results = tk.IntVar(value=50)
        self.search_query = tk.StringVar(value="")
        self.date_filter_enabled = tk.BooleanVar(value=False)
        self.start_date = tk.StringVar(value="")
        self.end_date = tk.StringVar(value="")
        
        # New PDF processing options
        self.extract_text = tk.BooleanVar(value=True)
        self.check_encryption = tk.BooleanVar(value=True)
        self.create_txt_files = tk.BooleanVar(value=True)
        
        # AI Assistant variables
        self.openai_api_key = tk.StringVar()
        self.ai_enabled = tk.BooleanVar()
        self.ai_task = tk.StringVar(value="summarize")
        
        # Categories
        self.categories = {
            "Robotics (cs.RO)": "cs.RO",
            "AI (cs.AI)": "cs.AI", 
            "Machine Learning (cs.LG)": "cs.LG",
            "Computer Vision (cs.CV)": "cs.CV",
            "Systems & Control (eess.SY)": "eess.SY",
            "Human-Computer Interaction (cs.HC)": "cs.HC",
            "Natural Language Processing (cs.CL)": "cs.CL"
        }
        self.selected_categories = {cat: tk.BooleanVar(value=True if cat in ["Robotics (cs.RO)", "AI (cs.AI)", "Systems & Control (eess.SY)"] else False) for cat in self.categories}
        
        self.create_widgets()
        self.is_fetching = False
        
    def setup_adaptive_ui(self):
        """Setup elegant modern UI with fixed 1280×720 dimensions"""
        # Get screen dimensions for centering
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Detect DPI scaling (for high-DPI displays)
        try:
            dpi = self.root.winfo_fpixels('1i')
            scale_factor = dpi / 96.0  # 96 is standard DPI
        except:
            scale_factor = 1.0
            dpi = 96
        
        # Set elegant fixed dimensions (16:9 aspect ratio)
        window_width = 1280
        window_height = 720
        
        # Center window perfectly on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Ensure window doesn't go off-screen on smaller displays
        x = max(0, x)
        y = max(0, y)
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1024, 576)  # Minimum 16:9 ratio
        self.root.maxsize(1920, 1080)  # Maximum reasonable size
        
        # Platform-specific UI adjustments for elegance
        current_platform = platform.system()
        
        if current_platform == "Darwin":  # macOS
            # macOS-specific settings for native look
            try:
                self.root.tk.call('tk', 'scaling', scale_factor)
                # Enable macOS native appearance
                self.root.wm_attributes('-transparent', False)
            except:
                pass
        elif current_platform == "Windows":
            # Windows DPI awareness and modern styling
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
                # Enable Windows 10+ styling
                self.root.wm_attributes('-alpha', 0.98)
            except:
                pass
        elif current_platform == "Linux":
            # Linux modern styling
            try:
                self.root.wm_attributes('-alpha', 0.98)
            except:
                pass
        
        # Store UI scaling info for later use
        self.ui_scale = scale_factor
        self.screen_info = {
            'width': window_width,  # Use window dimensions, not screen
            'height': window_height,
            'dpi': dpi,
            'platform': current_platform,
            'scale_factor': scale_factor
        }
        
    def create_widgets(self):
        # Configure proper UTF-8 encoding for emoji display
        try:
            self.root.tk.call('encoding', 'system', 'utf-8')
        except:
            pass
        
        # Main frame optimized for 1280x720 - no scrollbar needed
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.configure(style='Modern.TFrame')
        
        # Create two-column layout for better space utilization
        left_column = ttk.Frame(main_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_column = ttk.Frame(main_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Title with icon - spans both columns
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="[AI] Robotics Research Paper Fetcher", 
                               style='Title.TLabel')
        title_label.pack()
        
        version_label = ttk.Label(title_frame, text="Intelligent Academic Research Assistant",
                                 style='Subtitle.TLabel')
        version_label.pack(pady=(2, 0))
        
        # Platform info - compact
        platform_name = {"Darwin": "macOS", "Windows": "Windows", "Linux": "Linux"}.get(platform.system(), platform.system())
        pdf_status = "[PDF] Ready" if PDF_PROCESSING_AVAILABLE else "[!] Install PyPDF2"
        
        info_label = ttk.Label(title_frame, text=f"[SYS] {platform_name} • {pdf_status}", 
                              style='Subtitle.TLabel')
        info_label.pack(pady=(2, 10))
        
        # Left column sections
        self.create_search_section(left_column)
        self.create_date_section(left_column)
        self.create_ai_assistant_section(left_column)  # New AI section
        
        # Right column sections  
        self.create_pdf_section(right_column)
        self.create_settings_section(right_column)
        self.create_buttons_section(right_column)
        
        # Progress section spans both columns at bottom
        self.create_progress_section(main_frame)
        
    def create_search_section(self, parent):
        # Search section with modern styling
        search_frame = ttk.LabelFrame(parent, text="[SEARCH] Research Discovery", 
                                     style='Section.TLabelframe', padding="10")
        search_frame.pack(fill="x", pady=(0, 8))
        
        # Custom search with refined styling
        search_label = ttk.Label(search_frame, text="🎯 Custom Research Query:", 
                                style='Modern.TLabel')
        search_label.pack(anchor="w", pady=(0, 5))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_query,
                                style='Modern.TEntry', font=('Calibri', 12))
        search_entry.pack(fill="x", pady=(0, 5))
        
        hint_label = ttk.Label(search_frame, 
                              text="💡 Research examples: 'robotic manipulation', 'deep reinforcement learning', 'computer vision'", 
                              style='Subtitle.TLabel')
        hint_label.pack(anchor="w", pady=(0, 10))
        
        # Categories with refined visual organization
        cat_frame = ttk.LabelFrame(search_frame, text="📚 Academic Domains", 
                                  style='Section.TLabelframe', padding="10")
        cat_frame.pack(fill="x", pady=(10, 0))
        
        # Create grid for categories with better spacing
        cat_grid = ttk.Frame(cat_frame)
        cat_grid.pack(fill="x", pady=5)
        
        # Add category icons and better formatting
        category_icons = {
            "Robotics (cs.RO)": "🤖",
            "AI (cs.AI)": "🧠",
            "Machine Learning (cs.LG)": "📊",
            "Computer Vision (cs.CV)": "👁️",
            "Systems & Control (eess.SY)": "⚙️",
            "Human-Computer Interaction (cs.HC)": "🖱️",
            "Natural Language Processing (cs.CL)": "💬"
        }
        
        for i, (cat_name, var) in enumerate(self.selected_categories.items()):
            row = i // 3
            col = i % 3
            icon = category_icons.get(cat_name, "📄")
            display_text = f"{icon} {cat_name}"
            
            cb = ttk.Checkbutton(cat_grid, text=display_text, variable=var,
                                style='Modern.TCheckbutton')
            cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=4)
            
    def create_date_section(self, parent):
        # Date filtering with modern styling
        date_frame = ttk.LabelFrame(parent, text="📅 Temporal Filtering", 
                                   style='Section.TLabelframe', padding="10")
        date_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Checkbutton(date_frame, text="🗓️ Enable publication date filtering", 
                       variable=self.date_filter_enabled,
                       style='Modern.TCheckbutton').pack(anchor="w", pady=(0, 10))
        
        date_row = ttk.Frame(date_frame)
        date_row.pack(fill="x", pady=(5, 0))
        
        # Start date
        start_frame = ttk.Frame(date_row)
        start_frame.pack(side="left", padx=(0, 30))
        
        ttk.Label(start_frame, text="📅 Start Date:", 
                 style='Modern.TLabel').pack(anchor="w")
        start_entry = ttk.Entry(start_frame, textvariable=self.start_date, 
                               width=12, style='Modern.TEntry')
        start_entry.pack(pady=(2, 0))
        
        # End date
        end_frame = ttk.Frame(date_row)
        end_frame.pack(side="left")
        
        ttk.Label(end_frame, text="📅 End Date:", 
                 style='Modern.TLabel').pack(anchor="w")
        end_entry = ttk.Entry(end_frame, textvariable=self.end_date, 
                             width=12, style='Modern.TEntry')
        end_entry.pack(pady=(2, 0))
        
        ttk.Label(date_frame, text="💡 Date format: YYYY-MM-DD (example: 2024-01-01)", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(8, 0))
    
    def create_ai_assistant_section(self, parent):
        """Create AI Assistant section with ChatGPT integration"""
        ai_frame = ttk.LabelFrame(parent, text="🤖 AI Research Assistant", 
                                 style='Section.TLabelframe', padding="12")
        ai_frame.pack(fill="x", pady=(0, 10))
        
        # Enable AI checkbox
        ai_enable_frame = ttk.Frame(ai_frame)
        ai_enable_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Checkbutton(ai_enable_frame, text="🧠 Enable AI-powered analysis", 
                       variable=self.ai_enabled,
                       style='Modern.TCheckbutton').pack(anchor="w")
        
        # API Key entry
        api_frame = ttk.Frame(ai_frame)
        api_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Label(api_frame, text="🔑 OpenAI API Key:", 
                 style='Modern.TLabel').pack(anchor="w")
        
        api_entry = ttk.Entry(api_frame, textvariable=self.openai_api_key,
                             show="*", style='Modern.TEntry', font=('Calibri', 11))
        api_entry.pack(fill="x", pady=(2, 0))
        
        # AI Task selection
        task_frame = ttk.Frame(ai_frame)
        task_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(task_frame, text="🎯 AI Task:", 
                 style='Modern.TLabel').pack(anchor="w")
        
        task_combo = ttk.Combobox(task_frame, textvariable=self.ai_task,
                                 values=["summarize", "extract_keywords", "find_methodology", "identify_gaps"],
                                 state="readonly", width=15, font=('Calibri', 10))
        task_combo.pack(anchor="w", pady=(2, 0))
        
        # Help text
        ttk.Label(ai_frame, text="💡 AI will analyze papers for insights and summaries", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(5, 0))
                 
    def create_pdf_section(self, parent):
        # PDF Processing section with modern styling
        pdf_frame = ttk.LabelFrame(parent, text="📄 Document Processing", 
                                  style='Section.TLabelframe', padding="10")
        pdf_frame.pack(fill="x", pady=(0, 8))
        
        # PDF options with refined layout
        options_grid = ttk.Frame(pdf_frame)
        options_grid.pack(fill="x", pady=(0, 10))
        
        ttk.Checkbutton(options_grid, text="📝 Extract comprehensive text content", 
                       variable=self.extract_text,
                       style='Modern.TCheckbutton').grid(row=0, column=0, sticky="w", pady=2)
        
        ttk.Checkbutton(options_grid, text="🔒 Analyze document security status", 
                       variable=self.check_encryption,
                       style='Modern.TCheckbutton').grid(row=0, column=1, sticky="w", padx=(30, 0), pady=2)
        
        ttk.Checkbutton(options_grid, text="💾 Generate structured text files", 
                       variable=self.create_txt_files,
                       style='Modern.TCheckbutton').grid(row=1, column=0, sticky="w", pady=2)
        
        if not PDF_PROCESSING_AVAILABLE:
            warning_frame = ttk.Frame(pdf_frame)
            warning_frame.pack(fill="x", pady=(10, 0))
            
            ttk.Label(warning_frame, text="⚠️ PyPDF2 not installed - Install for PDF processing:",
                     style='Subtitle.TLabel').pack(anchor="w")
            
            install_btn = ttk.Button(warning_frame, text="📦 Install PyPDF2", 
                                   command=self.install_pdf_deps,
                                   style='Warning.TButton')
            install_btn.pack(anchor="w", pady=(5, 0))
            
    def create_settings_section(self, parent):
        # Settings section with modern styling
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Research Configuration", 
                                       style='Section.TLabelframe', padding="10")
        settings_frame.pack(fill="x", pady=(0, 8))
        
        # Max results setting
        results_frame = ttk.Frame(settings_frame)
        results_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(results_frame, text="📊 Research Scope:", 
                 style='Modern.TLabel').pack(anchor="w")
        
        results_row = ttk.Frame(results_frame)
        results_row.pack(fill="x", pady=(5, 0))
        
        results_spinbox = ttk.Spinbox(results_row, from_=1, to=500, 
                                     textvariable=self.max_results, width=8,
                                     style='Modern.TEntry')
        results_spinbox.pack(side="left")
        
        ttk.Label(results_row, text="research papers to acquire", 
                 style='Subtitle.TLabel').pack(side="left", padx=(10, 0))
        
        # Output directory setting
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill="x")
        
        ttk.Label(output_frame, text="📁 Research Library Location:", 
                 style='Modern.TLabel').pack(anchor="w")
        
        dir_row = ttk.Frame(output_frame)
        dir_row.pack(fill="x", pady=(5, 0))
        
        output_entry = ttk.Entry(dir_row, textvariable=self.output_dir, 
                                style='Modern.TEntry')
        output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(dir_row, text="📂 Browse", 
                  command=self.browse_output_dir).pack(side="left")
        
    def create_buttons_section(self, parent):
        # Control buttons with modern styling
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(8, 10))
        
        # Main action button (larger and more prominent)
        main_button_frame = ttk.Frame(button_frame)
        main_button_frame.pack(fill="x", pady=(0, 10))
        
        self.fetch_button = ttk.Button(main_button_frame, 
                                      text="🚀 Fetch & Process Papers", 
                                      command=self.start_fetch,
                                      style='Primary.TButton')
        self.fetch_button.pack(side="left", padx=(0, 15))
        
        self.stop_button = ttk.Button(main_button_frame, 
                                     text="⏹ Stop Process", 
                                     command=self.stop_fetch, 
                                     state=tk.DISABLED,
                                     style='Warning.TButton')
        self.stop_button.pack(side="left")
        
        # Secondary action buttons
        secondary_frame = ttk.Frame(button_frame)
        secondary_frame.pack(fill="x")
        
        ttk.Button(secondary_frame, text="📁 Open Output Folder", 
                  command=self.open_output_folder,
                  style='Success.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(secondary_frame, text="🔍 Analyze Existing PDFs", 
                  command=self.analyze_existing_pdfs).pack(side="left", padx=(0, 10))
        
        ttk.Button(secondary_frame, text="📊 Research Dashboard", 
                  command=self.open_research_dashboard).pack(side="left", padx=(0, 10))
        
        ttk.Button(secondary_frame, text="ℹ️ About & Help", 
                  command=self.show_about).pack(side="left")
        
    def create_progress_section(self, parent):
        # Progress section with modern styling
        progress_frame = ttk.LabelFrame(parent, text="📊 Research Activity Monitor", 
                                       style='Section.TLabelframe', padding="10")
        progress_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Progress bar with modern styling
        progress_info_frame = ttk.Frame(progress_frame)
        progress_info_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(progress_info_frame, text="⚡ Processing Status:", 
                 style='Modern.TLabel').pack(anchor="w")
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate',
                                       style='Modern.Horizontal.TProgressbar')
        self.progress.pack(fill="x", pady=(2, 8))
        
        # Log area with better styling - more compact
        log_label = ttk.Label(progress_frame, text="📝 Activity Log:", 
                             style='Modern.TLabel')
        log_label.pack(anchor="w", pady=(0, 2))
        
        # Compact log area for 720p height
        log_height = 8  # Fixed compact height
        
        self.log_text = scrolledtext.ScrolledText(progress_frame, 
                                                 height=log_height, 
                                                 wrap=tk.WORD,
                                                 font=('Consolas', 10),
                                                 bg='#FAFAFA',
                                                 fg='#333333',
                                                 selectbackground='#E3F2FD',
                                                 relief='flat',
                                                 borderwidth=1)
        self.log_text.pack(fill="both", expand=True)
        
        # Add welcome message
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

Ready to revolutionize your research workflow! 🚀
"""
        self.log_text.insert(tk.END, welcome_msg)
        self.log_text.see(tk.END)
        
    def install_pdf_deps(self):
        """Install PDF processing dependencies"""
        def install():
            import subprocess
            import sys
            try:
                self.log_message("📦 Installing PyPDF2...")
                subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"], check=True)
                self.log_message("✅ PyPDF2 installed successfully! Please restart the application.")
                messagebox.showinfo("Success", "PyPDF2 installed successfully!\nPlease restart the application to use PDF features.")
            except Exception as e:
                self.log_message(f"❌ Failed to install PyPDF2: {e}")
                messagebox.showerror("Error", f"Failed to install PyPDF2: {e}")
        
        threading.Thread(target=install, daemon=True).start()
        
    def process_pdf(self, pdf_path, paper_id):
        """Process a downloaded PDF file"""
        if not PDF_PROCESSING_AVAILABLE:
            return False
            
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check encryption
                if self.check_encryption.get() and pdf_reader.is_encrypted:
                    self.log_message(f"   ⚠️ PDF {paper_id} is encrypted!")
                    return False
                
                # Extract text
                if self.extract_text.get():
                    full_text = ""
                    for page_num, page in enumerate(pdf_reader.pages):
                        try:
                            text = page.extract_text()
                            full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
                        except Exception as e:
                            self.log_message(f"   ⚠️ Error extracting page {page_num + 1}: {e}")
                    
                    # Save text file
                    if self.create_txt_files.get() and full_text.strip():
                        output_dir = self.output_dir.get()
                        txt_dir = os.path.join(output_dir, "extracted_text")
                        os.makedirs(txt_dir, exist_ok=True)
                        
                        txt_path = os.path.join(txt_dir, f"{paper_id}_text.txt")
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(full_text)
                        
                        self.log_message(f"   📝 Text extracted to {os.path.basename(txt_path)}")
                        
                        # Process with AI if enabled
                        if self.ai_enabled.get() and full_text.strip():
                            # Extract title from the first lines of the PDF text
                            lines = full_text.split('\n')
                            paper_title = paper_id  # Fallback
                            for line in lines[:10]:  # Check first 10 lines for title
                                if len(line.strip()) > 10 and len(line.strip()) < 200:
                                    paper_title = line.strip()
                                    break
                            self.process_with_ai(paper_title, full_text, paper_id)
                
                return True
                
        except Exception as e:
            self.log_message(f"   ❌ PDF processing error: {e}")
            return False
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
            
    def log_message(self, message):
        """Add message to log area"""
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def build_query(self):
        """Build arXiv search query based on user inputs"""
        queries = []
        
        # Add category queries
        selected_cats = [code for name, code in self.categories.items() 
                        if self.selected_categories[name].get()]
        if selected_cats:
            cat_query = " OR ".join([f"cat:{cat}" for cat in selected_cats])
            queries.append(f"({cat_query})")
            
        # Add custom search if provided
        custom_search = self.search_query.get().strip()
        if custom_search:
            queries.append(f'(ti:"{custom_search}" OR abs:"{custom_search}")')
            
        return " AND ".join(queries) if queries else "cat:cs.RO"
        
    def start_fetch(self):
        """Start fetching papers in a separate thread"""
        if self.is_fetching:
            return
            
        # Validate inputs
        if not any(var.get() for var in self.selected_categories.values()) and not self.search_query.get().strip():
            messagebox.showerror("Error", "Please select at least one category or enter a search term.")
            return
            
        if self.date_filter_enabled.get():
            try:
                if self.start_date.get():
                    datetime.strptime(self.start_date.get(), "%Y-%m-%d")
                if self.end_date.get():
                    datetime.strptime(self.end_date.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return
                
        self.is_fetching = True
        self.fetch_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        
        # Start fetching in background thread
        self.fetch_thread = threading.Thread(target=self.fetch_papers, daemon=True)
        self.fetch_thread.start()
        
    def stop_fetch(self):
        """Stop the fetching process"""
        self.is_fetching = False
        self.fetch_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.log_message("❌ Fetch cancelled by user")
        
    def fetch_papers(self):
        """Main fetching logic with enhanced PDF processing"""
        try:
            # Create directories
            output_dir = self.output_dir.get()
            summary_dir = os.path.join(output_dir, "summaries")
            pdf_dir = os.path.join(output_dir, "pdfs")
            
            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(summary_dir, exist_ok=True)
            
            if PDF_PROCESSING_AVAILABLE and self.create_txt_files.get():
                txt_dir = os.path.join(output_dir, "extracted_text")
                os.makedirs(txt_dir, exist_ok=True)
                self.log_message(f"📁 Created directories: pdfs, summaries, extracted_text")
            else:
                self.log_message(f"📁 Created directories: pdfs, summaries")
            
            # Build query
            query = self.build_query()
            self.log_message(f"🔍 Search query: {query}")
            
            # Create search
            search = arxiv.Search(
                query=query,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                max_results=self.max_results.get(),
            )
            
            # Initialize CSV
            metadata_file = os.path.join(output_dir, "metadata.csv")
            
            papers_processed = 0
            papers_downloaded = 0
            papers_text_extracted = 0
            
            with open(metadata_file, mode="w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                header = ["ID", "Title", "Authors", "Published", "PDF_URL", "arXiv_URL", "Abstract", "Pages", "Encrypted", "Text_Extracted"]
                writer.writerow(header)
                
                # Use newer client method
                client = arxiv.Client()
                results = client.results(search)
                
                for i, result in enumerate(results, start=1):
                    if not self.is_fetching:
                        break
                        
                    # Date filtering
                    if self.date_filter_enabled.get():
                        paper_date = result.published.date()
                        if self.start_date.get():
                            start = datetime.strptime(self.start_date.get(), "%Y-%m-%d").date()
                            if paper_date < start:
                                continue
                        if self.end_date.get():
                            end = datetime.strptime(self.end_date.get(), "%Y-%m-%d").date()
                            if paper_date > end:
                                continue
                    
                    papers_processed += 1
                    self.log_message(f"📄 Processing paper {papers_processed}: {result.title[:60]}...")
                    
                    paper_id = f"{papers_processed:03d}_{result.entry_id.split('/')[-1]}"
                    pdf_filename = f"{paper_id}.pdf"
                    summary_filename = f"{paper_id}_summary.md"
                    
                    # Download PDF
                    pdf_path = os.path.join(pdf_dir, pdf_filename)
                    try:
                        result.download_pdf(filename=pdf_path)
                        papers_downloaded += 1
                        self.log_message(f"   ✅ Downloaded PDF ({papers_downloaded} total)")
                    except Exception as e:
                        self.log_message(f"   ❌ Failed to download PDF: {str(e)[:100]}")
                        continue
                    
                    # Process PDF
                    pdf_info = {"pages": "N/A", "encrypted": "N/A", "text_extracted": False}
                    if PDF_PROCESSING_AVAILABLE:
                        try:
                            with open(pdf_path, 'rb') as file:
                                pdf_reader = PyPDF2.PdfReader(file)
                                pdf_info["pages"] = len(pdf_reader.pages)
                                pdf_info["encrypted"] = pdf_reader.is_encrypted
                                
                                if self.process_pdf(pdf_path, paper_id):
                                    pdf_info["text_extracted"] = True
                                    papers_text_extracted += 1
                        except Exception as e:
                            self.log_message(f"   ⚠️ PDF analysis failed: {str(e)[:50]}")
                    
                    # Create enhanced summary template
                    summary_path = os.path.join(summary_dir, summary_filename)
                    with open(summary_path, "w", encoding="utf-8") as f:
                        f.write(f"# {result.title}\n\n")
                        f.write(f"**Authors:** {', '.join([a.name for a in result.authors])}\n\n")
                        f.write(f"**Published:** {result.published.strftime('%Y-%m-%d')}\n\n")
                        f.write(f"**arXiv URL:** {result.entry_id}\n\n")
                        f.write(f"**Categories:** {', '.join(result.categories)}\n\n")
                        f.write(f"**Pages:** {pdf_info['pages']}\n\n")
                        f.write(f"**PDF Status:** {'Encrypted' if pdf_info['encrypted'] else 'Not encrypted'}\n\n")
                        f.write("## 📋 Abstract\n\n")
                        f.write(f"{result.summary}\n\n")
                        f.write("## 🔍 Summary\n\n...\n\n")
                        f.write("## 🧠 What I Learned\n\n...\n\n")
                        f.write("## 🔬 How It Can Be Improved\n\n...\n\n")
                        f.write("## 🧪 Ideas for Extension\n\n...\n")
                    
                    # Write to CSV
                    writer.writerow([
                        papers_processed,
                        result.title,
                        ", ".join([a.name for a in result.authors]),
                        result.published.strftime('%Y-%m-%d'),
                        result.pdf_url,
                        result.entry_id,
                        result.summary[:500] + "..." if len(result.summary) > 500 else result.summary,
                        pdf_info['pages'],
                        pdf_info['encrypted'],
                        pdf_info['text_extracted']
                    ])
                    
                    self.log_message(f"   ✅ Created enhanced summary template")
                    
            self.log_message(f"🎉 Completed! Downloaded {papers_downloaded} papers, processed {papers_processed} total")
            if PDF_PROCESSING_AVAILABLE:
                self.log_message(f"📝 Text extracted from {papers_text_extracted} papers")
            self.log_message(f"📊 Metadata saved to: {metadata_file}")
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
        finally:
            self.is_fetching = False
            self.root.after(0, self._fetch_complete)
            
    def _fetch_complete(self):
        """Called when fetch completes to update UI"""
        self.fetch_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        
    def analyze_existing_pdfs(self):
        """Analyze already downloaded PDFs"""
        pdf_dir = os.path.join(self.output_dir.get(), "pdfs")
        if not os.path.exists(pdf_dir):
            messagebox.showwarning("Warning", f"No PDF directory found at {pdf_dir}")
            return
            
        def analyze():
            self.log_message("🔍 Analyzing existing PDFs...")
            pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            
            if not pdf_files:
                self.log_message("❌ No PDF files found")
                return
                
            encrypted_count = 0
            total_pages = 0
            
            for pdf_file in pdf_files:
                pdf_path = os.path.join(pdf_dir, pdf_file)
                self.log_message(f"   📄 Analyzing {pdf_file}")
                
                if PDF_PROCESSING_AVAILABLE:
                    try:
                        with open(pdf_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            is_encrypted = pdf_reader.is_encrypted
                            pages = len(pdf_reader.pages)
                            
                            if is_encrypted:
                                encrypted_count += 1
                                self.log_message(f"     🔒 Encrypted, {pages} pages")
                            else:
                                total_pages += pages
                                self.log_message(f"     ✅ Not encrypted, {pages} pages")
                                
                    except Exception as e:
                        self.log_message(f"     ❌ Error: {str(e)[:50]}")
                else:
                    file_size = os.path.getsize(pdf_path) / (1024*1024)
                    self.log_message(f"     📊 Size: {file_size:.2f} MB")
            
            self.log_message(f"📊 Analysis complete: {len(pdf_files)} files, {encrypted_count} encrypted")
            if PDF_PROCESSING_AVAILABLE:
                self.log_message(f"📖 Total pages analyzed: {total_pages}")
        
        threading.Thread(target=analyze, daemon=True).start()
        
    def open_output_folder(self):
        """Open the output folder in file manager"""
        output_dir = self.output_dir.get()
        if os.path.exists(output_dir):
            if platform.system() == 'Windows':
                os.startfile(output_dir)
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'open "{output_dir}"')
            else:  # Linux and others
                os.system(f'xdg-open "{output_dir}"')
        else:
            messagebox.showwarning("Warning", f"Directory {output_dir} does not exist yet.")
    
    def open_research_dashboard(self):
        """Open the research analytics dashboard"""
        try:
            # Import here to avoid dependency issues if not installed
            from research_dashboard import open_research_dashboard
            
            # Get current papers data (you can enhance this to read from metadata.csv)
            papers_data = []
            if os.path.exists("papers/metadata.csv"):
                try:
                    import pandas as pd
                    df = pd.read_csv("papers/metadata.csv")
                    papers_data = df.to_dict('records')
                except:
                    pass
            
            dashboard = open_research_dashboard(self.root, papers_data)
            if dashboard:
                self.log_message("📊 Research dashboard opened successfully")
        except ImportError:
            messagebox.showinfo("Research Dashboard", 
                               "📊 Research Dashboard requires additional packages:\n\n"
                               "pip install matplotlib seaborn pandas\n\n"
                               "Install these packages to unlock advanced analytics!")
        except Exception as e:
            self.log_message(f"❌ Could not open research dashboard: {e}")
    
    def process_with_ai(self, paper_title, paper_text, paper_id):
        """Process paper with AI assistant"""
        if not self.ai_enabled.get() or not self.openai_api_key.get().strip():
            return
        
        try:
            import openai
            from openai import OpenAI
            
            # Set up OpenAI client with newer API
            client = OpenAI(api_key=self.openai_api_key.get().strip())
            
            task = self.ai_task.get()
            
            if task == "summarize":
                prompt = f"""Please provide a concise academic summary of this research paper:

Title: {paper_title}

Text: {paper_text[:4000]}...

Provide a summary covering:
1. Main contribution
2. Methodology 
3. Key findings
4. Significance

Keep it under 200 words and academic in tone."""
            
            elif task == "extract_keywords":
                prompt = f"""Extract the most important keywords and research concepts from this paper:

Title: {paper_title}
Text: {paper_text[:4000]}...

List 10-15 key technical terms, methods, and concepts."""
            
            elif task == "find_methodology":
                prompt = f"""Identify and summarize the research methodology used in this paper:

Title: {paper_title}
Text: {paper_text[:4000]}...

Focus on:
1. Research approach
2. Experimental setup
3. Data collection methods
4. Analysis techniques"""
            
            elif task == "identify_gaps":
                prompt = f"""Identify research gaps and future work opportunities mentioned in this paper:

Title: {paper_title}
Text: {paper_text[:4000]}...

Highlight:
1. Limitations mentioned by authors
2. Suggested future work
3. Potential research directions"""
            
            # Make API call with newer client
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert research assistant specializing in robotics and AI."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            ai_analysis = response.choices[0].message.content
            
            # Save AI analysis
            ai_dir = os.path.join(self.output_dir.get(), "ai_analysis")
            os.makedirs(ai_dir, exist_ok=True)
            
            ai_file = os.path.join(ai_dir, f"{paper_id}_ai_{task}.md")
            with open(ai_file, 'w', encoding='utf-8') as f:
                f.write(f"# AI Analysis: {task.replace('_', ' ').title()}\n\n")
                f.write(f"**Paper:** {paper_title}\n\n")
                f.write(f"**Analysis Type:** {task}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## AI Analysis\n\n")
                f.write(ai_analysis)
            
            self.log_message(f"   🤖 AI analysis saved: {os.path.basename(ai_file)}")
            
        except ImportError:
            self.log_message("   ⚠️ Install openai package for AI features: pip install openai")
        except Exception as e:
            self.log_message(f"   ❌ AI processing error: {str(e)[:100]}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """🤖 Robotics Research Paper Fetcher

An intelligent academic research assistant for discovering and managing robotics research papers.

✨ Advanced Research Capabilities:
• Intelligent search across 7 specialized research domains
• Seamless PDF acquisition and comprehensive text extraction
• Research analytics dashboard with advanced visualizations
• Export to BibTeX, EndNote, RIS formats
• Cross-platform compatibility with elegant 1280×720 UI

🔧 Technical Architecture:
• Modern Python application with tkinter
• arXiv API integration for real-time paper discovery
• PyPDF2 for comprehensive document processing
• Optional analytics with matplotlib & seaborn
• Responsive design with Material Design principles

📊 Research Intelligence:
• Real-time activity monitoring
• Trend analysis and keyword extraction
• Citation network visualization
• Collaborative sharing and export tools
• Comprehensive metadata analysis

🎯 Perfect for:
• Academic researchers and students
• Research institutions and labs
• Literature review automation
• Academic paper collection management

© 2024 - Open Source Academic Research Tool
Transform your research workflow today!"""
        
        messagebox.showinfo("About", about_text)

def ensure_emoji_display(root):
    """Ensure proper emoji display on all platforms"""
    try:
        # Set UTF-8 encoding for proper emoji support
        root.tk.call('encoding', 'system', 'utf-8')
    except:
        pass

def configure_modern_style(root):
    """Configure modern, appealing visual style"""
    style = ttk.Style()
    
    # Use a modern theme as base
    available_themes = style.theme_names()
    if "vista" in available_themes:  # Windows
        style.theme_use("vista")
    elif "aqua" in available_themes:  # macOS
        style.theme_use("aqua")
    elif "clam" in available_themes:  # Cross-platform
        style.theme_use("clam")
    else:
        style.theme_use("default")
    
    # Define elegant modern color palette
    colors = {
        'primary': '#1E88E5',      # Elegant Blue
        'primary_dark': '#1565C0',
        'secondary': '#26A69A',    # Sophisticated Teal
        'accent': '#FF7043',       # Warm Orange
        'surface': '#FAFAFA',      # Pure White Surface
        'background': '#F8F9FA',   # Subtle Gray Background
        'text': '#263238',         # Rich Dark Text
        'text_secondary': '#546E7A', # Muted Secondary Text
        'error': '#E53935',
        'success': '#43A047',
        'highlight': '#E3F2FD'     # Light Blue Highlight
    }
    
    # Configure styles with research-preferred fonts
    style.configure('Title.TLabel', 
                   font=('Calibri', 22, 'bold'),
                   foreground=colors['primary'],
                   background=colors['background'])
    
    style.configure('Subtitle.TLabel',
                   font=('Calibri', 11),
                   foreground=colors['text_secondary'],
                   background=colors['background'])
    
    style.configure('Section.TLabelframe.Label',
                   font=('Calibri', 12, 'bold'),
                   foreground=colors['primary'])
    
    style.configure('Section.TLabelframe',
                   borderwidth=1,
                   relief='solid',
                   background=colors['surface'])
    
    # Modern button styles with research-preferred fonts
    style.configure('Primary.TButton',
                   font=('Calibri', 11, 'bold'),
                   foreground='white',
                   background=colors['primary'],
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8))
    
    style.map('Primary.TButton',
             background=[('active', colors['primary_dark']),
                        ('pressed', colors['primary_dark'])])
    
    style.configure('Success.TButton',
                   font=('Calibri', 11),
                   foreground='white',
                   background=colors['secondary'],
                   borderwidth=0,
                   focuscolor='none',
                   padding=(8, 6))
    
    style.configure('Warning.TButton',
                   font=('Calibri', 11),
                   foreground='white',
                   background=colors['accent'],
                   borderwidth=0,
                   focuscolor='none',
                   padding=(8, 6))
    
    # Enhanced entry styles
    style.configure('Modern.TEntry',
                   fieldbackground=colors['surface'],
                   borderwidth=1,
                   relief='solid',
                   padding=(8, 6))
    
    # Progress bar styling
    style.configure('Modern.Horizontal.TProgressbar',
                   troughcolor=colors['background'],
                   background=colors['primary'],
                   lightcolor=colors['primary'],
                   darkcolor=colors['primary_dark'])
    
    # Modern frame styling
    style.configure('Modern.TFrame',
                   background=colors['background'],
                   relief='flat')
    
    # Modern label styling with research-preferred fonts
    style.configure('Modern.TLabel',
                   font=('Calibri', 11),
                   foreground=colors['text'],
                   background=colors['surface'])
    
    # Modern checkbutton styling with research-preferred fonts
    style.configure('Modern.TCheckbutton',
                   font=('Calibri', 10),
                   foreground=colors['text'],
                   background=colors['surface'],
                   focuscolor='none')
    
    # Set window background
    root.configure(bg=colors['background'])
    
    return style, colors

def main():
    root = tk.Tk()
    
    # Ensure proper emoji display
    ensure_emoji_display(root)
    
    # Configure modern styling
    style, colors = configure_modern_style(root)
    
    # Create app (window positioning handled in setup_adaptive_ui)
    app = EnhancedArxivFetcherGUI(root, colors)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main() 