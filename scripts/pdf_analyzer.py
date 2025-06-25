#!/usr/bin/env python3
"""
PDF Analyzer - Check PDF properties including encryption status
"""

import os
import sys
from pathlib import Path

def check_pdf_properties(pdf_path):
    """Check PDF properties including encryption status"""
    try:
        import PyPDF2
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if encrypted
            is_encrypted = pdf_reader.is_encrypted
            
            # Get basic info
            info = {
                'file': os.path.basename(pdf_path),
                'size_mb': round(os.path.getsize(pdf_path) / (1024*1024), 2),
                'encrypted': is_encrypted,
                'num_pages': len(pdf_reader.pages) if not is_encrypted else 'N/A (encrypted)',
                'can_extract_text': False
            }
            
            # Try to extract text from first page (if not encrypted)
            if not is_encrypted:
                try:
                    first_page = pdf_reader.pages[0]
                    text = first_page.extract_text()
                    info['can_extract_text'] = len(text.strip()) > 0
                    info['sample_text'] = text[:100] + "..." if len(text) > 100 else text
                except:
                    info['can_extract_text'] = False
                    info['sample_text'] = "Text extraction failed"
            else:
                info['sample_text'] = "PDF is encrypted"
                
            return info
            
    except ImportError:
        return {
            'file': os.path.basename(pdf_path),
            'size_mb': round(os.path.getsize(pdf_path) / (1024*1024), 2),
            'encrypted': 'Unknown (PyPDF2 not installed)',
            'num_pages': 'Unknown',
            'can_extract_text': False,
            'sample_text': 'Install PyPDF2 to analyze PDFs'
        }
    except Exception as e:
        return {
            'file': os.path.basename(pdf_path),
            'size_mb': round(os.path.getsize(pdf_path) / (1024*1024), 2),
            'encrypted': f'Error: {str(e)}',
            'num_pages': 'Error',
            'can_extract_text': False,
            'sample_text': f'Analysis failed: {str(e)}'
        }

def analyze_pdfs_in_directory(directory):
    """Analyze all PDFs in a directory"""
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return []
    
    results = []
    print(f"📁 Analyzing {len(pdf_files)} PDF files in {directory}")
    print("=" * 80)
    
    for pdf_file in pdf_files:
        print(f"🔍 Analyzing: {pdf_file.name}")
        info = check_pdf_properties(pdf_file)
        results.append(info)
        
        # Print results
        print(f"   📄 Size: {info['size_mb']} MB")
        print(f"   🔒 Encrypted: {info['encrypted']}")
        print(f"   📖 Pages: {info['num_pages']}")
        print(f"   📝 Text extractable: {info['can_extract_text']}")
        print(f"   💬 Sample text: {info['sample_text'][:50]}...")
        print()
    
    return results

def main():
    # Check if PyPDF2 is installed
    try:
        import PyPDF2
        print("✅ PyPDF2 is available for PDF analysis")
    except ImportError:
        print("❌ PyPDF2 not installed. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"])
        print("✅ PyPDF2 installed successfully")
    
    # Analyze PDFs in papers/pdfs directory
    pdf_dir = "papers/pdfs"
    if os.path.exists(pdf_dir):
        results = analyze_pdfs_in_directory(pdf_dir)
        
        # Summary
        encrypted_count = sum(1 for r in results if r['encrypted'] is True)
        text_extractable_count = sum(1 for r in results if r['can_extract_text'] is True)
        
        print("📊 Summary:")
        print(f"   Total PDFs: {len(results)}")
        print(f"   Encrypted: {encrypted_count}")
        print(f"   Text extractable: {text_extractable_count}")
        
        if encrypted_count > 0:
            print("⚠️  Some PDFs are encrypted and may need special handling")
        else:
            print("✅ All PDFs are readable and not encrypted")
            
    else:
        print(f"❌ Directory {pdf_dir} not found")

if __name__ == "__main__":
    main() 