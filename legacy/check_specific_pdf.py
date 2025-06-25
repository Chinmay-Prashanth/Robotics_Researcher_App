#!/usr/bin/env python3
"""
Check specific PDF file for detailed analysis
"""

import PyPDF2
import os

def analyze_specific_pdf(pdf_path):
    """Analyze a specific PDF file in detail"""
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return
    
    print(f"🔍 Analyzing: {pdf_path}")
    print("=" * 60)
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Basic info
            print(f"📄 File size: {os.path.getsize(pdf_path) / (1024*1024):.2f} MB")
            print(f"📖 Number of pages: {len(pdf_reader.pages)}")
            print(f"🔒 Encrypted: {pdf_reader.is_encrypted}")
            
            # Metadata
            if pdf_reader.metadata:
                print(f"📝 Title: {pdf_reader.metadata.get('/Title', 'N/A')}")
                print(f"👤 Author: {pdf_reader.metadata.get('/Author', 'N/A')}")
                print(f"📅 Creation Date: {pdf_reader.metadata.get('/CreationDate', 'N/A')}")
                print(f"🛠️ Producer: {pdf_reader.metadata.get('/Producer', 'N/A')}")
            
            print("\n📋 Text Content (First 2 pages):")
            print("-" * 40)
            
            # Extract text from first few pages
            for i, page in enumerate(pdf_reader.pages[:2]):
                print(f"\n📄 Page {i+1}:")
                text = page.extract_text()
                if text.strip():
                    # Clean up the text
                    lines = text.split('\n')
                    cleaned_lines = [line.strip() for line in lines if line.strip()]
                    
                    # Print first 20 lines or all if less
                    for j, line in enumerate(cleaned_lines[:20]):
                        print(f"   {line}")
                    
                    if len(cleaned_lines) > 20:
                        print(f"   ... ({len(cleaned_lines) - 20} more lines)")
                else:
                    print("   No extractable text found")
                    
                print("-" * 40)
            
            # Check for potential issues
            print("\n🔍 Analysis:")
            
            # Check if text extraction worked well
            first_page_text = pdf_reader.pages[0].extract_text()
            if len(first_page_text.strip()) < 100:
                print("⚠️  Warning: Very little text extracted. PDF might be image-based.")
            
            # Check for common issues
            if "arXiv:" in first_page_text:
                print("✅ Appears to be an arXiv paper")
            
            if any(word in first_page_text.lower() for word in ['robot', 'manipulation', 'ai', 'learning']):
                print("✅ Contains robotics/AI content")
            
            # Check for potential OCR needs
            total_chars = sum(len(page.extract_text()) for page in pdf_reader.pages)
            avg_chars_per_page = total_chars / len(pdf_reader.pages)
            
            if avg_chars_per_page < 500:
                print("⚠️  Low character count per page - might need OCR")
            else:
                print(f"✅ Good text density ({avg_chars_per_page:.0f} chars/page avg)")
                
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")

def main():
    # Check the specific PDF file the user mentioned
    pdf_path = "papers/pdfs/005_2506.19269v1.pdf"
    analyze_specific_pdf(pdf_path)

if __name__ == "__main__":
    main() 