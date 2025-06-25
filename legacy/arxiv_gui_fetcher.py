#!/usr/bin/env python3
"""
arXiv Robotics Paper Fetcher - GUI Version
A user-friendly interface for researchers to fetch papers from arXiv
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import arxiv
import os
import csv
import threading
from datetime import datetime, timedelta
import webbrowser

class ArxivFetcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("arXiv Robotics Paper Fetcher")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.output_dir = tk.StringVar(value="papers")
        self.summary_dir = tk.StringVar(value="summaries")
        self.max_results = tk.IntVar(value=50)
        self.search_query = tk.StringVar(value="")
        self.date_filter_enabled = tk.BooleanVar(value=False)
        self.start_date = tk.StringVar(value="")
        self.end_date = tk.StringVar(value="")
        
        # Categories
        self.categories = {
            "Robotics (cs.RO)": "cs.RO",
            "AI (cs.AI)": "cs.AI", 
            "Machine Learning (cs.LG)": "cs.LG",
            "Computer Vision (cs.CV)": "cs.CV",
            "Systems & Control (eess.SY)": "eess.SY",
            "Human-Computer Interaction (cs.HC)": "cs.HC"
        }
        self.selected_categories = {cat: tk.BooleanVar(value=True if cat in ["Robotics (cs.RO)", "AI (cs.AI)", "Systems & Control (eess.SY)"] else False) for cat in self.categories}
        
        self.create_widgets()
        self.is_fetching = False
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="arXiv Robotics Paper Fetcher", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Search section
        search_frame = ttk.LabelFrame(main_frame, text="Search Configuration", padding="10")
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Custom search query
        ttk.Label(search_frame, text="Custom Search:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_query, width=50)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        
        ttk.Label(search_frame, text="(e.g., 'robot manipulation', 'deep learning', etc.)", 
                 font=("Arial", 8)).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Categories selection
        cat_frame = ttk.LabelFrame(search_frame, text="Categories", padding="5")
        cat_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        row = 0
        col = 0
        for cat_name, var in self.selected_categories.items():
            cb = ttk.Checkbutton(cat_frame, text=cat_name, variable=var)
            cb.grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Date filtering
        date_frame = ttk.LabelFrame(main_frame, text="Date Filtering (Optional)", padding="10")
        date_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        date_frame.columnconfigure(1, weight=1)
        date_frame.columnconfigure(3, weight=1)
        
        ttk.Checkbutton(date_frame, text="Enable date filtering", 
                       variable=self.date_filter_enabled).grid(row=0, column=0, columnspan=4, sticky=tk.W)
        
        ttk.Label(date_frame, text="Start Date:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        start_entry = ttk.Entry(date_frame, textvariable=self.start_date, width=12)
        start_entry.grid(row=1, column=1, sticky=tk.W, pady=(5, 0), padx=(10, 20))
        
        ttk.Label(date_frame, text="End Date:").grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
        end_entry = ttk.Entry(date_frame, textvariable=self.end_date, width=12)
        end_entry.grid(row=1, column=3, sticky=tk.W, pady=(5, 0), padx=(10, 0))
        
        ttk.Label(date_frame, text="Format: YYYY-MM-DD", 
                 font=("Arial", 8)).grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(2, 0))
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="Max Results:").grid(row=0, column=0, sticky=tk.W)
        results_spinbox = ttk.Spinbox(settings_frame, from_=1, to=500, textvariable=self.max_results, width=10)
        results_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(settings_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        output_frame = ttk.Frame(settings_frame)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 0), padx=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir, width=8).grid(row=0, column=1, padx=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.fetch_button = ttk.Button(button_frame, text="🚀 Fetch Papers", command=self.start_fetch, style="Accent.TButton")
        self.fetch_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Stop", command=self.stop_fetch, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📁 Open Output Folder", command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="ℹ About", command=self.show_about).pack(side=tk.LEFT)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log area
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=15, width=80)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main_frame grid weights
        main_frame.rowconfigure(5, weight=1)
        
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
            # Simple keyword search in title and abstract
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
        """Main fetching logic"""
        try:
            # Create directories
            output_dir = self.output_dir.get()
            summary_dir = os.path.join(output_dir, "summaries")
            pdf_dir = os.path.join(output_dir, "pdfs")
            
            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(summary_dir, exist_ok=True)
            
            self.log_message(f"📁 Created directories: {pdf_dir}, {summary_dir}")
            
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
            
            with open(metadata_file, mode="w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["ID", "Title", "Authors", "Published", "PDF_URL", "arXiv_URL", "Abstract"])
                
                # Use newer client method instead of deprecated search.results()
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
                    
                    pdf_filename = f"{papers_processed:03d}_{result.entry_id.split('/')[-1]}.pdf"
                    summary_filename = f"{papers_processed:03d}_{result.entry_id.split('/')[-1]}_summary.md"
                    
                    # Download PDF
                    pdf_path = os.path.join(pdf_dir, pdf_filename)
                    try:
                        result.download_pdf(filename=pdf_path)
                        papers_downloaded += 1
                        self.log_message(f"   ✅ Downloaded PDF ({papers_downloaded} total)")
                    except Exception as e:
                        self.log_message(f"   ❌ Failed to download PDF: {str(e)[:100]}")
                        continue
                    
                    # Create summary template
                    summary_path = os.path.join(summary_dir, summary_filename)
                    with open(summary_path, "w", encoding="utf-8") as f:
                        f.write(f"# {result.title}\n\n")
                        f.write(f"**Authors:** {', '.join([a.name for a in result.authors])}\n\n")
                        f.write(f"**Published:** {result.published.strftime('%Y-%m-%d')}\n\n")
                        f.write(f"**arXiv URL:** {result.entry_id}\n\n")
                        f.write(f"**Categories:** {', '.join(result.categories)}\n\n")
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
                        result.summary[:500] + "..." if len(result.summary) > 500 else result.summary
                    ])
                    
                    self.log_message(f"   ✅ Created summary template")
                    
            self.log_message(f"🎉 Completed! Downloaded {papers_downloaded} papers, processed {papers_processed} total")
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
        
    def open_output_folder(self):
        """Open the output folder in file manager"""
        output_dir = self.output_dir.get()
        if os.path.exists(output_dir):
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'xdg-open "{output_dir}"')
        else:
            messagebox.showwarning("Warning", f"Directory {output_dir} does not exist yet.")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """arXiv Robotics Paper Fetcher v2.0

A user-friendly tool for researchers to fetch and organize papers from arXiv.

Features:
• Search by categories and custom terms
• Date range filtering
• Automatic PDF download
• Summary template generation
• Metadata export to CSV

Created for researchers to streamline their literature review process.

GitHub: github.com/your-username/arxiv-robotics-fetcher"""
        
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    app = ArxivFetcherGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 