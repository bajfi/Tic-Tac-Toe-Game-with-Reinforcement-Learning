from setuptools import find_packages, setup

setup(
    name="tic_tac_toe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "flask",
        "flask-cors",
    ],
)
