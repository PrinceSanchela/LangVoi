"""
Setup configuration for LangVoi Voice Studio Pro.
"""

from setuptools import setup, find_packages

setup(
    name="langvoi",
    version="2.2.0",
    author="Prince Sanchela",
    description="Universal Native Audio Engineering Workstation & Neural Whisper Language Identification",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PrinceSanchela/LangVoi",
    packages=find_packages(include=["app*", "core*"]),
    include_package_data=True,
    install_requires=[
        "numpy>=1.24.0",
        "sounddevice>=0.4.6",
        "SpeechRecognition>=3.10.0",
        "soundfile>=0.12.0",
        "av>=11.0.0",
        "miniaudio>=1.50.0",
        "httpx>=0.25.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "langvoi = run:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.10",
)
