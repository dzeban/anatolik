"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('anatolik/anatolik.py').read(),
    re.M
    ).group(1)
 
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "anatolik",
    packages = ["anatolik"],
    entry_points = {
        "console_scripts": ['anatolik = anatolik.anatolik:main']
        },
    version = version,
    description = "Funny static blog engine.",
    long_description = long_descr,
    author = "avd",
    author_email = "avd@reduct.ru",
    url = "http://github.com/dzeban/anatolik",
    )
