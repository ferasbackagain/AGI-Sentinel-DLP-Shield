"""
AGI Sentinel DLP Shield - Setup Configuration
Professional packaging for PyPI or local installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="agi-sentinel-dlp-shield",
    version="2.1.0",
    author="Feras Khatib",
    author_email="feras.khatib@example.com",  # Replace with actual email
    description="Enterprise-grade Data Loss Prevention for AI/AGI Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ferasbackagain/AGI-Sentinel-DLP-Shield",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Framework :: AsyncIO",
    ],
    
    keywords="security, dlp, ai, agi, data-loss-prevention, cybersecurity",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    python_requires=">=3.8",
    
    install_requires=[
        "pandas>=2.0.0,<3.0.0",
        "regex>=2023.1.1,<2024.0.0",
        "cryptography>=41.0.0,<43.0.0",
        "ujson>=5.0.0,<6.0.0",
        "tqdm>=4.65.0,<5.0.0",
    ],
    
    extras_require={
        "cloud": [
            "boto3>=1.28.0,<2.0.0",
            "azure-storage-blob>=12.0.0,<13.0.0",
            "google-cloud-storage>=2.0.0,<3.0.0",
        ],
        "performance": [
            "pyarrow>=12.0.0,<13.0.0",
            "numpy>=1.24.0,<2.0.0",
        ],
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pytest-cov>=4.0.0,<5.0.0",
            "black>=23.0.0,<24.0.0",
            "mypy>=1.0.0,<2.0.0",
            "flake8>=6.0.0,<7.0.0",
            "sphinx>=7.0.0,<8.0.0",
            "sphinx-rtd-theme>=1.0.0,<2.0.0",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "agi-sentinel=agi_sentinel.cli:main",
            "sentinel-scan=scripts.scan_csv:main",
        ],
    },
    
    package_data={
        "agi_sentinel": [
            "config/*.json",
            "config/*.yaml",
        ],
    },
    
    include_package_data=True,
    
    project_urls={
        "Bug Reports": "https://github.com/ferasbackagain/AGI-Sentinel-DLP-Shield/issues",
        "Source": "https://github.com/ferasbackagain/AGI-Sentinel-DLP-Shield",
        "Documentation": "https://github.com/ferasbackagain/AGI-Sentinel-DLP-Shield/wiki",
    },
)
