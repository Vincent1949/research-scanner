"""
Research Scanner - Universal research paper discovery system
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="research-scanner",
    version="1.0.0",
    author="Vincent Micó",
    author_email="vincent.mico@proton.me",
    description="Universal research paper discovery system - works for ANY research domain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vincent1949/research-scanner",
    project_urls={
        "Bug Tracker": "https://github.com/Vincent1949/research-scanner/issues",
        "Documentation": "https://github.com/Vincent1949/research-scanner#readme",
        "Source Code": "https://github.com/Vincent1949/research-scanner",
    },
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Indexing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "research-scanner=research_scanner.cli:main",
            "research-setup=setup_wizard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "research_scanner": [
            "templates/*.yaml",
        ],
    },
    keywords=[
        "research",
        "papers",
        "arxiv",
        "pubmed",
        "academic",
        "literature review",
        "knowledge management",
        "ai",
        "machine learning",
        "vector database",
        "semantic search",
    ],
    zip_safe=False,
)
