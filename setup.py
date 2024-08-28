from setuptools import setup, find_packages

setup(
    name="pyavc",
    version="1.0.10",
    author="Lawson Tanner",
    author_email="pyavc@lawsonia.cc",
    description="A command line utility and library for converting DOCX and TXT files to Avid Script Files (.avc)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lawson-tanner/pyavc",
    packages=find_packages(where="src"),  # Automatically find and include packages
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pyavc=avc.cli:main',  
        ],
    },
    
    python_requires='>=3.6',
    install_requires=[
        'python-docx>=0.8.10',
    
    ],
    include_package_data=True,
)
