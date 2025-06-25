#!/usr/bin/env python3
"""
🚀 Research Dashboard for Robotics Paper Fetcher
Advanced analytics and visualization for research management
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from datetime import datetime, timedelta
import os
import json
from collections import Counter, defaultdict
import re

# Set style for better plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class ResearchDashboard:
    def __init__(self, parent, papers_data=None):
        self.parent = parent
        self.papers_data = papers_data or []
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Create the research dashboard interface"""
        # Create main dashboard window
        self.dashboard_window = tk.Toplevel(self.parent)
        self.dashboard_window.title("📊 Research Analytics Dashboard")
        self.dashboard_window.geometry("1200x800")
        
        # Create notebook for different views
        notebook = ttk.Notebook(self.dashboard_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Overview tab
        self.create_overview_tab(notebook)
        
        # Analytics tab
        self.create_analytics_tab(notebook)
        
        # Trends tab
        self.create_trends_tab(notebook)
        
        # Export tab
        self.create_export_tab(notebook)
    
    def create_overview_tab(self, notebook):
        """Create overview statistics tab"""
        overview_frame = ttk.Frame(notebook)
        notebook.add(overview_frame, text="📈 Overview")
        
        # Stats cards
        stats_frame = ttk.Frame(overview_frame)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.create_stat_card(stats_frame, "Total Papers", len(self.papers_data), "📄", 0, 0)
        self.create_stat_card(stats_frame, "Recent (30 days)", self.count_recent_papers(), "🆕", 0, 1)
        self.create_stat_card(stats_frame, "Categories", self.count_categories(), "📚", 0, 2)
        self.create_stat_card(stats_frame, "Avg Pages", self.avg_pages(), "📖", 1, 0)
        
        # Recent activity
        activity_frame = ttk.LabelFrame(overview_frame, text="🕒 Recent Activity", padding="15")
        activity_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Activity listbox
        activity_listbox = tk.Listbox(activity_frame, height=10, font=('Segoe UI', 10))
        activity_scrollbar = ttk.Scrollbar(activity_frame, orient="vertical", command=activity_listbox.yview)
        activity_listbox.configure(yscrollcommand=activity_scrollbar.set)
        
        activity_listbox.pack(side="left", fill="both", expand=True)
        activity_scrollbar.pack(side="right", fill="y")
        
        # Populate recent activity
        self.populate_recent_activity(activity_listbox)
    
    def create_analytics_tab(self, notebook):
        """Create detailed analytics tab"""
        analytics_frame = ttk.Frame(notebook)
        notebook.add(analytics_frame, text="📊 Analytics")
        
        # Create matplotlib figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # Papers by category
        self.plot_papers_by_category(ax1)
        
        # Papers over time
        self.plot_papers_timeline(ax2)
        
        # Page distribution
        self.plot_page_distribution(ax3)
        
        # Keyword frequency
        self.plot_keyword_frequency(ax4)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, analytics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_trends_tab(self, notebook):
        """Create research trends analysis tab"""
        trends_frame = ttk.Frame(notebook)
        notebook.add(trends_frame, text="📈 Trends")
        
        # Trend analysis controls
        controls_frame = ttk.Frame(trends_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(controls_frame, text="🔍 Trend Analysis:", font=('Segoe UI', 12, 'bold')).pack(anchor="w")
        
        # Trending keywords
        keywords_frame = ttk.LabelFrame(trends_frame, text="🔥 Trending Keywords", padding="15")
        keywords_frame.pack(fill="x", padx=20, pady=10)
        
        trending_keywords = self.get_trending_keywords()
        for i, (keyword, count) in enumerate(trending_keywords[:10]):
            keyword_row = ttk.Frame(keywords_frame)
            keyword_row.pack(fill="x", pady=2)
            
            ttk.Label(keyword_row, text=f"{i+1}.", width=3).pack(side="left")
            ttk.Label(keyword_row, text=keyword, font=('Segoe UI', 10, 'bold')).pack(side="left", padx=(5, 0))
            ttk.Label(keyword_row, text=f"({count} papers)", foreground="gray").pack(side="left", padx=(10, 0))
        
        # Research evolution
        evolution_frame = ttk.LabelFrame(trends_frame, text="📊 Research Evolution", padding="15")
        evolution_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Timeline visualization
        self.create_evolution_chart(evolution_frame)
    
    def create_export_tab(self, notebook):
        """Create export and sharing tab"""
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="📤 Export")
        
        # Export options
        export_options_frame = ttk.LabelFrame(export_frame, text="📋 Export Options", padding="20")
        export_options_frame.pack(fill="x", padx=20, pady=20)
        
        # Bibliography export
        bib_frame = ttk.Frame(export_options_frame)
        bib_frame.pack(fill="x", pady=10)
        
        ttk.Label(bib_frame, text="📚 Bibliography Export:", font=('Segoe UI', 11, 'bold')).pack(anchor="w")
        
        bib_buttons_frame = ttk.Frame(bib_frame)
        bib_buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(bib_buttons_frame, text="📄 BibTeX", command=self.export_bibtex).pack(side="left", padx=(0, 10))
        ttk.Button(bib_buttons_frame, text="📋 EndNote", command=self.export_endnote).pack(side="left", padx=(0, 10))
        ttk.Button(bib_buttons_frame, text="🔗 RIS Format", command=self.export_ris).pack(side="left", padx=(0, 10))
        
        # Data export
        data_frame = ttk.Frame(export_options_frame)
        data_frame.pack(fill="x", pady=10)
        
        ttk.Label(data_frame, text="📊 Data Export:", font=('Segoe UI', 11, 'bold')).pack(anchor="w")
        
        data_buttons_frame = ttk.Frame(data_frame)
        data_buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(data_buttons_frame, text="📈 Excel Report", command=self.export_excel).pack(side="left", padx=(0, 10))
        ttk.Button(data_buttons_frame, text="📊 CSV Data", command=self.export_csv).pack(side="left", padx=(0, 10))
        ttk.Button(data_buttons_frame, text="📑 Research Summary", command=self.export_summary).pack(side="left", padx=(0, 10))
        
        # Sharing options
        sharing_frame = ttk.LabelFrame(export_frame, text="🤝 Sharing & Collaboration", padding="20")
        sharing_frame.pack(fill="x", padx=20, pady=10)
        
        sharing_buttons_frame = ttk.Frame(sharing_frame)
        sharing_buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(sharing_buttons_frame, text="📤 Generate Reading List", command=self.generate_reading_list).pack(side="left", padx=(0, 10))
        ttk.Button(sharing_buttons_frame, text="🔗 Create Citation Network", command=self.create_citation_network).pack(side="left", padx=(0, 10))
        ttk.Button(sharing_buttons_frame, text="📋 Research Portfolio", command=self.create_portfolio).pack(side="left", padx=(0, 10))
    
    def create_stat_card(self, parent, title, value, icon, row, col):
        """Create a statistics card"""
        card_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
        
        icon_label = ttk.Label(card_frame, text=icon, font=('Segoe UI', 24))
        icon_label.pack(pady=(10, 5))
        
        value_label = ttk.Label(card_frame, text=str(value), font=('Segoe UI', 18, 'bold'))
        value_label.pack()
        
        title_label = ttk.Label(card_frame, text=title, font=('Segoe UI', 10))
        title_label.pack(pady=(0, 10))
    
    def count_recent_papers(self):
        """Count papers from the last 30 days"""
        if not self.papers_data:
            return 0
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_count = 0
        
        for paper in self.papers_data:
            # This would need to be adapted based on your data structure
            # Assuming papers have a 'date' or 'published' field
            recent_count += 1  # Placeholder
        
        return min(recent_count, len(self.papers_data))
    
    def count_categories(self):
        """Count unique categories in papers"""
        if not self.papers_data:
            return 0
        
        categories = set()
        for paper in self.papers_data:
            # Extract categories from paper metadata
            categories.add("Robotics")  # Placeholder
        
        return max(1, len(categories))
    
    def avg_pages(self):
        """Calculate average pages per paper"""
        if not self.papers_data:
            return 0
        
        # This would calculate based on actual PDF page counts
        return 12  # Placeholder average
    
    def populate_recent_activity(self, listbox):
        """Populate recent activity list"""
        activities = [
            "📄 Downloaded 'Deep Reinforcement Learning for Robotic Manipulation'",
            "📊 Analyzed PDF text extraction for 5 papers",
            "🔍 Searched for 'computer vision' papers",
            "📈 Generated research summary report",
            "📚 Added 3 papers to 'Machine Learning' category",
            "🎯 Filtered papers by date range 2024-01-01 to 2024-12-31",
            "📝 Extracted metadata from recent downloads",
            "🤖 Processed robotics category papers"
        ]
        
        for activity in activities:
            listbox.insert(tk.END, activity)
    
    def plot_papers_by_category(self, ax):
        """Plot papers distribution by category"""
        categories = ['Robotics', 'AI', 'CV', 'ML', 'NLP', 'HCI', 'Control']
        counts = [25, 18, 15, 22, 8, 12, 10]  # Placeholder data
        
        ax.bar(categories, counts, color=sns.color_palette("husl", len(categories)))
        ax.set_title('📚 Papers by Research Domain', fontsize=14, fontweight='bold')
        ax.set_xlabel('Research Domain')
        ax.set_ylabel('Number of Papers')
        ax.tick_params(axis='x', rotation=45)
    
    def plot_papers_timeline(self, ax):
        """Plot papers acquired over time"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        counts = [3, 5, 8, 12, 15, 18, 22, 25, 20, 16, 12, 8]  # Placeholder
        
        ax.plot(dates, counts, marker='o', linewidth=2, markersize=6)
        ax.set_title('📈 Research Acquisition Timeline', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month')
        ax.set_ylabel('Papers Acquired')
        ax.grid(True, alpha=0.3)
    
    def plot_page_distribution(self, ax):
        """Plot distribution of paper lengths"""
        page_ranges = ['1-5', '6-10', '11-15', '16-20', '21+']
        counts = [12, 28, 35, 15, 10]  # Placeholder
        
        ax.pie(counts, labels=page_ranges, autopct='%1.1f%%', startangle=90)
        ax.set_title('📖 Paper Length Distribution', fontsize=14, fontweight='bold')
    
    def plot_keyword_frequency(self, ax):
        """Plot most frequent keywords"""
        keywords = ['deep learning', 'robotics', 'manipulation', 'vision', 'control', 'neural', 'learning', 'AI']
        frequencies = [45, 38, 32, 28, 25, 22, 20, 18]  # Placeholder
        
        ax.barh(keywords, frequencies, color=sns.color_palette("viridis", len(keywords)))
        ax.set_title('🔥 Most Frequent Keywords', fontsize=14, fontweight='bold')
        ax.set_xlabel('Frequency')
    
    def get_trending_keywords(self):
        """Get trending keywords from papers"""
        # Placeholder trending keywords
        return [
            ('deep reinforcement learning', 15),
            ('robotic manipulation', 12),
            ('computer vision', 11),
            ('neural networks', 10),
            ('machine learning', 9),
            ('autonomous systems', 8),
            ('human-robot interaction', 7),
            ('motion planning', 6),
            ('perception', 5),
            ('control systems', 4)
        ]
    
    def create_evolution_chart(self, parent):
        """Create research evolution visualization"""
        evolution_text = """
📊 Research Evolution Analysis

🔹 Emerging Trends (2024):
  • Transformer architectures in robotics
  • Multi-modal learning approaches
  • Sim-to-real transfer methods

🔹 Growing Areas:
  • Embodied AI and robotics
  • Few-shot learning applications
  • Sustainable robotics research

🔹 Established Fields:
  • Classical computer vision
  • Traditional control theory
  • Statistical machine learning
        """
        
        text_widget = tk.Text(parent, wrap=tk.WORD, height=12, font=('Segoe UI', 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, evolution_text)
        text_widget.config(state=tk.DISABLED)
    
    # Export methods
    def export_bibtex(self):
        """Export papers as BibTeX format"""
        messagebox.showinfo("Export", "📄 BibTeX export feature coming soon!\nWill generate properly formatted citations.")
    
    def export_endnote(self):
        """Export papers for EndNote"""
        messagebox.showinfo("Export", "📋 EndNote export feature coming soon!\nWill create .enw files for import.")
    
    def export_ris(self):
        """Export papers in RIS format"""
        messagebox.showinfo("Export", "🔗 RIS export feature coming soon!\nCompatible with most reference managers.")
    
    def export_excel(self):
        """Export comprehensive Excel report"""
        messagebox.showinfo("Export", "📈 Excel report feature coming soon!\nWill include analytics and paper details.")
    
    def export_csv(self):
        """Export raw data as CSV"""
        messagebox.showinfo("Export", "📊 CSV export feature coming soon!\nMachine-readable research data.")
    
    def export_summary(self):
        """Export research summary report"""
        messagebox.showinfo("Export", "📑 Research summary feature coming soon!\nComprehensive analysis report.")
    
    def generate_reading_list(self):
        """Generate prioritized reading list"""
        messagebox.showinfo("Sharing", "📤 Reading list generation coming soon!\nPrioritized by relevance and impact.")
    
    def create_citation_network(self):
        """Create citation network visualization"""
        messagebox.showinfo("Sharing", "🔗 Citation network feature coming soon!\nVisualize paper relationships.")
    
    def create_portfolio(self):
        """Create research portfolio"""
        messagebox.showinfo("Sharing", "📋 Research portfolio feature coming soon!\nProfessional research summary.")

def open_research_dashboard(parent, papers_data=None):
    """Open the research dashboard window"""
    try:
        dashboard = ResearchDashboard(parent, papers_data)
        return dashboard
    except ImportError as e:
        messagebox.showerror("Missing Dependencies", 
                           f"Research Dashboard requires additional packages:\n\n"
                           f"pip install matplotlib seaborn pandas\n\n"
                           f"Error: {e}")
        return None
    except Exception as e:
        messagebox.showerror("Dashboard Error", f"Could not open research dashboard:\n{e}")
        return None 