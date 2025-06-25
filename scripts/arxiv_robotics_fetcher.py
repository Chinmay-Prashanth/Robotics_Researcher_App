# arxiv_robotics_fetcher.py
import arxiv
import os
import csv

# Settings
MAX_RESULTS = 100
OUTPUT_DIR = "papers"
SUMMARY_DIR = "summaries"
METADATA_FILE = "metadata.csv"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)

# Fetch latest robotics papers
search = arxiv.Search(
    query="cat:cs.RO OR cat:cs.AI OR cat:eess.SY",
    sort_by=arxiv.SortCriterion.SubmittedDate,
    max_results=MAX_RESULTS,
)

# Write metadata
with open(METADATA_FILE, mode="w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Title", "Authors", "Published", "PDF_URL", "arXiv_URL"])

    for i, result in enumerate(search.results(), start=1):
        pdf_filename = f"{i:03d}.pdf"
        summary_filename = f"{i:03d}_summary.md"

        # Download PDF
        pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
        try:
            result.download_pdf(filename=pdf_path)
        except Exception as e:
            print(f"Failed to download PDF for {result.title}: {e}")
            continue

        # Save markdown summary template
        summary_path = os.path.join(SUMMARY_DIR, summary_filename)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(f"# {result.title}\n")
            f.write(f"**Authors:** {', '.join([a.name for a in result.authors])}\n\n")
            f.write(f"**Published:** {result.published.strftime('%Y-%m-%d')}\n\n")
            f.write(f"**arXiv URL:** {result.entry_id}\n\n")
            f.write("## 🔍 Summary\n\n...\n\n")
            f.write("## 🧠 What I Learned\n\n...\n\n")
            f.write("## 🔬 How It Can Be Improved\n\n...\n\n")
            f.write("## 🧪 Ideas for Extension\n\n...\n")

        # Append to CSV
        writer.writerow([
            i,
            result.title,
            ", ".join([a.name for a in result.authors]),
            result.published.strftime('%Y-%m-%d'),
            result.pdf_url,
            result.entry_id,
        ])

print("✅ Done fetching and saving!") 