from setuptools import setup, find_packages


setup(
    name="assistant-cli",
    version="1.0.0",
    description="A command-line application for managing contacts and notes.",
    author="Nineteen_PyP",
    url="https://github.com/qEmrys/project-Nineteen_PyP.git",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "rich==14.3.3"
    ],
    entry_points={
        "console_scripts": [
            "assistant=assistant_bot.main:main"
        ]
    },
    include_package_data=True,
    package_data={"": ["*.txt"]}
)