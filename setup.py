from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="categories-of-the-commons",
    version="0.1.0",
    author="Ibrahim Cesar",
    author_email="ibrahim@ibrahimcesar.com",
    description="Categorical-cybernetic framework for analyzing OSS governance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibrahimcesar/categories-of-the-commons",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
        "PyGithub>=2.1.0",
        "aiohttp>=3.9.0",
        "statsmodels>=0.14.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "networkx>=3.2.0",
        "tqdm>=4.66.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "jupyterlab>=4.0.0",
            "ipywidgets>=8.1.0",
            "plotly>=5.18.0",
        ],
    },
)
