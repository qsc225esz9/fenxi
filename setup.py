from setuptools import setup, find_packages

setup(
    name="fenxi",
    version="0.1.0",
    description="数据分析工具 / Data Analysis Tool",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "scipy>=1.10.0",
    ],
    entry_points={
        "console_scripts": [
            "fenxi=fenxi.__main__:main",
        ],
    },
)
