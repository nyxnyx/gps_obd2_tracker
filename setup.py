import fnmatch
from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as build_py_orig

with open("README.md", "r") as fh:
    long_description = fh.read()

excluded = ['obdtracker/__main__.py']

class build_py(build_py_orig):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [
            (pkg, mod, file)
            for (pkg, mod, file) in modules
            if not any(fnmatch.fnmatchcase(file, pat=pattern) for pattern in excluded)
        ]


setup(
    name="obdtracker", # Replace with your own username
    version="0.2.6",
    author="Grzegorz Szostak",
    author_email="szostak.grzegorz@gmail.com",
    description="Library to read data from http://www.aika168.com and other cloud services to track cars with GPS trackers installed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nyxnyx/gps_obd2_tracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={'build_py': build_py},
)
