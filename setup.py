from setuptools import setup, find_packages

setup(
    name="pyavc",
    version="0.1.0",
    author="Lawson Tanner",
    author_email="pyavc@lawsonia.cc",
    description="A command line utility and library for converting DOCX and TXT files to Avid Script Files (.avc)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lawson-tanner/pyavc",
    packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[
        # List of dependencies
    ],
)
