"""
Setup script for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="video-classification-dataset",
    version="1.0.0",
    description="Video classification dataset with labeled video clips across multiple categories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Molla Samser",
    author_email="help@rskworld.in",
    url="https://rskworld.in",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.8.0",
        "opencv-contrib-python>=4.8.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "tqdm>=4.66.0",
        "pyyaml>=6.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="video classification dataset machine learning deep learning",
    project_urls={
        "Homepage": "https://rskworld.in",
        "Documentation": "https://rskworld.in",
        "Source": "https://rskworld.in",
    },
)

