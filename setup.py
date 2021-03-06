from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["tabulate"]

setup(
    name="drawio-layer",
    version="0.0.1",
    author="Stanislav Zhelnio",
    author_email="zhelniosl@yandex.ru",
    description="Layer management script for draw.io",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/zhelnio/drawio-layer",
    packages=find_packages(),
    py_modules = ['drawio_layer'],
    entry_points={
        "console_scripts": [
            "drawio-layer = drawio_layer:main",
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
)
