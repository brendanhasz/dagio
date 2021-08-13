from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dagio",
    version="0.0.1",
    author="Brendan Hasz",
    author_email="winsto99@gmail.com",
    description="A python package for running directed acyclic graphs of asynchronous I/O operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brendanhasz/dagio",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    zip_safe=False,
    extras_require={
        "dev": [
            "autoflake >= 1.4",
            "black >= 19.10b0",
            "bumpversion",
            "flake8 >= 3.8.3",
            "isort >= 5.1.2",
            "pytest >= 6.0.0rc1",
            "pytest-asyncio >= 0.15.1",
            "pytest-cov >= 2.7.1",
            "setuptools >= 49.1.0",
            "twine >= 3.2.0",
            "wheel >= 0.34.2",
        ],
    },
)