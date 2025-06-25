#!/usr/bin/env python3
"""
Setup script for Enhanced arXiv Robotics Paper Fetcher
Creates a proper Python package that can be installed via pip
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements_gui.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="arxiv-robotics-fetcher",
    version="2.1.0",
    author="arXiv Robotics Fetcher",
    author_email="",
    description="🤖 Enhanced arXiv Robotics Paper Fetcher with GUI and PDF Processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/arxiv-robotics-fetcher",
    packages=find_packages(),
    py_modules=["enhanced_arxiv_gui", "arxiv_robotics_fetcher", "pdf_analyzer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
        "build": ["pyinstaller>=5.0", "cx_Freeze"],
    },
    entry_points={
        "console_scripts": [
            "arxiv-fetcher-cli=arxiv_robotics_fetcher:main",
            "arxiv-fetcher-gui=enhanced_arxiv_gui:main",
            "arxiv-fetcher=enhanced_arxiv_gui:main",  # Default to GUI
        ],
        "gui_scripts": [
            "ArxivFetcher=enhanced_arxiv_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.cfg"],
    },
    keywords="arxiv, robotics, papers, research, pdf, gui, automation, academic",
    project_urls={
        "Bug Reports": "https://github.com/your-username/arxiv-robotics-fetcher/issues",
        "Source": "https://github.com/your-username/arxiv-robotics-fetcher",
        "Documentation": "https://github.com/your-username/arxiv-robotics-fetcher/blob/main/README.md",
    },
) 