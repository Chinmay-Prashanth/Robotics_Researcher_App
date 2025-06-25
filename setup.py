#!/usr/bin/env python3
"""
Setup script for AI-Powered Robotics Research Paper Fetcher
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="robotics-paper-fetcher",
    version="2.0.0",
    author="Chinmay",
    author_email="your.email@example.com",  # Update with your email
    description="🤖 AI-Powered tool for discovering, analyzing, and managing robotics research papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/robotics_paper_fetcher",  # Update with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "ai": ["openai>=0.27.0"],
        "analytics": ["matplotlib>=3.5.0", "seaborn>=0.11.0", "pandas>=1.3.0"],
        "pdf": ["PyPDF2>=2.0.0"],
        "dev": ["pytest>=6.0", "black>=22.0", "flake8>=4.0"],
    },
    entry_points={
        "console_scripts": [
            "robotics-fetcher=main:main",
            "rfetch=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "robotics", "research", "arxiv", "papers", "ai", "machine-learning",
        "automation", "bibliography", "citations", "literature-review"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/robotics_paper_fetcher/issues",
        "Source": "https://github.com/yourusername/robotics_paper_fetcher",
        "Documentation": "https://github.com/yourusername/robotics_paper_fetcher/blob/main/docs/",
    },
) 