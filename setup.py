from setuptools import setup, find_packages
# import importlib.util
import io
import os
# from packaging.version import Version, parse


ROOT_DIR = os.path.dirname(__file__)

def get_path(*filepath) -> str:
    return os.path.join(ROOT_DIR, *filepath)

def read_readme() -> str:
    """Read the README file if present."""
    p = get_path("README.md")
    if os.path.isfile(p):
        return io.open(get_path("README.md"), "r", encoding="utf-8").read()
    else:
        return ""
    
setup(
    name="hub",
    version='0.1',
    author="SANI Team",
    license="BSD 3-Clause License",
    description=("A hub for nonprofits to access latest technologies"),
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/IbrahimAlrayes/NM-Hub",
    project_urls={
        "Homepage": "https://github.com/IbrahimAlrayes/NM-Hub",
        "Documentation": "https://github.com/IbrahimAlrayes/NM-Hub",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: BSD 3-Clause License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    # install_requires=get_requirements(),
    # ext_modules=ext_modules,
    # extras_require={
    #     "tensorizer": ["tensorizer>=2.9.0"],
    # },
    # cmdclass={"build_ext": cmake_build_ext} if not _is_neuron() else {},
    # package_data=package_data,
)