import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="obdtracker", # Replace with your own username
    version="0.2.2",
    author="Grzegorz Szostak",
    author_email="szostak.grzegorz@gmail.com",
    description="Library to read data from http://www.aika168.com and other cloud services to track cars with GPS trackers installed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nyxnyx/gps_obd2_tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)