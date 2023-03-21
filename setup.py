from setuptools import setup, find_packages
import io

with io.open("requirements.txt", "r", encoding="utf-8") as req:
    requirements = req.read().splitlines()

setup(
    name="azizdoc",
    version="0.1.0",
    author="Maroun",
    author_email="marounjassaf@gmail.com",
    description="A package to extract comments from Python code",
    url="https://github.com/marounassaf14/extract_comments",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
)
