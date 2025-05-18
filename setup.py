from setuptools import setup, find_packages

setup(
    name="maguniverse",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "pandas", "jinja2"],
    author="X. Li",
    description="A Python-based data manager for working with tabulated data from publications of observational surveys of cosmic magnetic fields.",
    url="https://github.com/xli2522/maguniverse",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)