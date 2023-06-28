import setuptools
import os


PROJECT_NAME = 'pyrclone'
if os.name == 'nt':  # Windows
    rclone_binary = (f'lib\site-packages\{PROJECT_NAME}', ['win/rclone.exe'])
elif os.name == 'posix':  # Unix-like
    if os.uname().sysname == 'Linux':
        rclone_binary = (f'lib\site-packages\{PROJECT_NAME}', ['linux/rclone'])
    elif os.uname().sysname == 'Darwin':
        rclone_binary = (f'lib\site-packages\{PROJECT_NAME}', ['mac/rclone'])
else:
    raise NotImplementedError('Unsupported OS')

setuptools.setup(
    name="PyRCloneTest",
    version="0.0.1-v1.62.2",
    author="Yuangang Li",
    author_email="yuangangli@outlook.com",
    description="A package that provides a wrapper for RClone",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MrLYG/python-rclone.git",
    packages=setuptools.find_packages(),
    data_files=[(rclone_binary)],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
