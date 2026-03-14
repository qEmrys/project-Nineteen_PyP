from setuptools import setup, find_namespace_packages


setup(
    name="CLIAppl",
    version="1",
    description="A command-line application for managing contacts and notes.",
    author="Nineteen_PyP",
    url="https://github.com/qEmrys/project-Nineteen_PyP.git",
    license="MIT",
    packages=find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "rich==14.3.3"
    ],
    include_package_data=True,
    package_data={"": ["*.txt"]}
)