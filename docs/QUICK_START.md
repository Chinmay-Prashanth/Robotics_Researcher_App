# 🚀 Quick Start Guide

Get your robotics research automation up and running in 5 minutes!

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Internet connection** for downloading papers
- **Optional**: OpenAI API key for AI analysis features

## ⚡ Installation Options

### Option 1: Automatic Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/robotics_paper_fetcher.git
cd robotics_paper_fetcher

# One-click installation
python scripts/install.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the application
python reliable_arxiv_gui.py
```

## 🎯 First Research Session

### 1. Launch the Application
```bash
python reliable_arxiv_gui.py
```

### 2. Configure Your Search
- **Search Terms**: Enter keywords like "robotic manipulation", "SLAM", "deep learning"
- **Categories**: Select relevant areas (Robotics, AI, Machine Learning, etc.)
- **Date Range**: Optional - filter by publication date
- **Max Results**: Start with 10-20 papers for your first session

### 3. Start Fetching
- Click **"[GO] Fetch & Process Papers"**
- Watch the progress in the activity log
- Papers will be downloaded to the `papers/` folder

### 4. Explore Your Results
- Click **"[VIEW] View Downloaded Papers"** to see your collection
- Check `papers/summaries/` for AI-generated summaries
- Open `papers/pdfs/` to read the full papers

## 🧠 AI Analysis Setup (Optional)

### Get OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-...`)

### Enable AI Features
1. In the GUI, check **"🧠 Enable AI"**
2. Paste your API key in the **"🔑 API Key"** field
3. Select analysis type: **"summarize"** for beginners
4. AI will automatically analyze downloaded papers

## 📊 Understanding Your Results

### File Structure After First Run
```
papers/
├── pdfs/                     # Downloaded research papers
├── summaries/                # Markdown summary templates  
├── extracted_text/           # Full text for searching
├── ai_analysis/              # AI-generated insights (if enabled)
└── metadata.csv              # Complete paper database
```

### Key Files to Check
- **`papers/metadata.csv`**: Spreadsheet with all paper information
- **`papers/summaries/001_*_summary.md`**: Summary of first paper
- **Activity Log**: Real-time progress in the GUI

## 🔧 Troubleshooting

### Common Issues

**GUI doesn't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**No papers downloaded**
```bash
# Check internet connection
ping arxiv.org

# Try broader search terms
# Use fewer categories
# Increase date range
```

**AI analysis fails**
- Check API key is valid
- Verify you have OpenAI credits
- Try disabling AI temporarily

**PDF processing errors**
```bash
# Install PDF dependencies
pip install PyPDF2
```

## 🎯 Next Steps

1. **Daily Routine**: Run 5-minute searches for latest papers in your area
2. **Deep Dive**: Use AI summaries to quickly identify relevant papers
3. **Organization**: Export citations to your reference manager
4. **Insights**: Use the Research Dashboard for trend analysis

## 🤝 Getting Help

- **Documentation**: Check `docs/` folder for detailed guides
- **Issues**: Report problems on GitHub Issues
- **Features**: Request new features via GitHub
- **Community**: Connect with other researchers using the tool

## 📚 Sample Research Queries

Try these searches to get started:

| Research Area | Search Terms | Expected Papers |
|---------------|--------------|-----------------|
| **Manipulation** | "robotic manipulation", "grasping" | 50+ recent papers |
| **Navigation** | "SLAM", "path planning", "autonomous navigation" | 100+ papers |
| **Learning** | "reinforcement learning", "meta learning" | 200+ papers |
| **Vision** | "computer vision", "object detection", "segmentation" | 150+ papers |
| **HRI** | "human robot interaction", "collaborative robotics" | 30+ papers |

---

**Ready to transform your research workflow? Start with a simple search and discover the power of intelligent paper management!** 🚀 