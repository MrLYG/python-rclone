import setuptools
import os


if os.name == 'nt':  # Windows
    rclone_binary = ['rclone.exe']
elif os.name == 'posix':  # Unix-like
    if os.uname().sysname == 'Linux':
        rclone_binary = ['rclone']
    elif os.uname().sysname == 'Darwin':
        rclone_binary = ['rclone']
else:
    raise NotImplementedError('Unsupported OS')

setuptools.setup(
    name="pyrclonetest",
    version="0.0.7",
    author="Yuangang Li",
    author_email="yuangangli@outlook.com",
    description="A package that provides a wrapper for RClone",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MrLYG/python-rclone.git",
    packages=setuptools.find_packages(exclude=('mac', 'win', 'linux')),
    include_package_data=True,
    package_data={
        'pyrclone': rclone_binary,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
