#!/usr/bin/env python3
"""
Setup script for RAG Assistant for Academic Research.

This setup.py file provides compatibility with older Python packaging tools
and demonstrates traditional Python package configuration alongside the
modern pyproject.toml approach.

Note: While this file is included for educational purposes and compatibility,
the primary configuration is now in pyproject.toml following modern Python
packaging standards (PEP 517/518).
"""

from setuptools import setup, find_packages
import os
import sys
from pathlib import Path

# Ensure we're using Python 3.11+
if sys.version_info < (3, 11):
    sys.exit("Python 3.11 or higher is required. You are using Python {}.{}.".format(
        sys.version_info.major, sys.version_info.minor))

# Get the long description from the README file
here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Read requirements from requirements.txt
def read_requirements(filename):
    """Read requirements from a requirements file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f 
                   if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

# Main requirements
install_requires = read_requirements('requirements.txt')

# Development requirements
dev_requires = read_requirements('requirements-dev.txt')

# Define package data
package_data = {
    'src': [
        'templates/*.html',
        'templates/*.css',
        'templates/*.js',
        'static/*',
    ]
}

# Define entry points for command-line scripts
entry_points = {
    'console_scripts': [
        'rag-web=magic_research.web_app:main',
        'rag-cli=magic_research.app:main',
        'rag-assistant=magic_research.app:main',
    ],
}

# Setup configuration
setup(
    # Basic package information
    name="rag-assistant",
    version="1.0.0",
    
    # Package description
    description="A Retrieval-Augmented Generation (RAG) system for academic research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Author information
    author="RAG Assistant Contributors",
    author_email="contributors@example.com",
    maintainer="Main Maintainer",
    maintainer_email="maintainer@example.com",
    
    # URLs
    url="https://github.com/your-username/rag-assistant",
    project_urls={
        "Bug Reports": "https://github.com/your-username/rag-assistant/issues",
        "Source": "https://github.com/your-username/rag-assistant",
        "Documentation": "https://rag-assistant.readthedocs.io/",
        "Changelog": "https://github.com/your-username/rag-assistant/blob/main/CHANGELOG.md",
    },
    
    # Package discovery and content
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        'magic_research': [
            'templates/*.html',
            'templates/*.css', 
            'templates/*.js',
            'static/*',
        ]
    },
    include_package_data=True,
    
    # Dependencies
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "test": [
            "pytest>=7.4.4",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pytest-asyncio>=0.21.1",
            "factory-boy>=3.3.0",
            "faker>=20.1.0",
            "responses>=0.24.1",
            "httpx>=0.28.1",
        ],
        "docs": [
            "sphinx>=7.2.6",
            "sphinx-rtd-theme>=2.0.0",
            "myst-parser>=2.0.0",
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.2",
        ],
        "performance": [
            "py-spy>=0.3.14",
            "memory-profiler>=0.61.0",
            "line-profiler>=4.1.1",
            "locust>=2.17.0",
        ],
        "all": dev_requires + [
            "sphinx>=7.2.6", "mkdocs>=1.5.3", "py-spy>=0.3.14"
        ],
    },
    
    # Python version requirement
    python_requires=">=3.11",
    
    # PyPI classifiers
    classifiers=[
        # Development status
        "Development Status :: 5 - Production/Stable",
        
        # Intended audience
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        
        # Topic classification
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        
        # License
        "License :: Free for non-commercial use",
        
        # Programming language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        
        # Operating system
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        
        # Framework
        "Framework :: FastAPI",
        
        # Environment
        "Environment :: Web Environment",
        "Environment :: Console",
        
        # Natural language
        "Natural Language :: English",
    ],
    
    # Keywords for searching
    keywords=[
        "rag", "retrieval-augmented-generation", "academic-research", 
        "nlp", "semantic-search", "vector-database", "medieval-history",
        "digital-humanities", "fastapi", "chromadb", "langchain",
        "openai", "embeddings", "pdf-processing", "academic-papers"
    ],
    
    # Entry points for command-line scripts
    entry_points=entry_points,
    
    # Additional metadata
    zip_safe=False,  # Don't create zipped eggs
    
    # Platform specification
    platforms=["any"],
    
    # License
    license="CC-BY-NC-SA-4.0",
    
    # Additional options for setuptools
    options={
        "build_py": {
            "compile": True,
            "optimize": 2,
        },
        "install": {
            "optimize": 1,
        },
    },
)

# Print installation success message
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  RAG Assistant Setup                        ║
    ║                                                              ║
    ║  A Retrieval-Augmented Generation system for academic       ║
    ║  research on historical texts and manuscripts.              ║
    ║                                                              ║
    ║  Next steps:                                                 ║
    ║  1. Configure your .env file with API keys                  ║
    ║  2. Add your documents to the data/ directory               ║
    ║  3. Run: python src/web_app.py                              ║
    ║  4. Open: http://127.0.0.1:8000                             ║
    ║                                                              ║
    ║  For help: python -m src.app --help                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)