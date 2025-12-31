from setuptools import setup, find_packages

setup(
    name="pyping-tool",
    version="1.0.0",
    author="Ismail Tasdelen",
    author_email="pentestdatabase@gmail.com",
    description="A modernized cross-platform ping test tool written in Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ismailtasdelen/PyPing",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "rich",
        "matplotlib",
        "Flask",
        "flask-socketio",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "pyping=source.ping_test_tool:ping_test",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
