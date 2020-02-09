from setuptools import setup

setup(
    name="optset",
    version="0.0.1",
    description="Command options and configuration settings file handling module",
    author="James Martin",
    license="MIT",
    author_email="jimpub@gmail.com",
    url="https://github.com/J-A-M-E-5/optset",
    packages=["optset"],
    install_requires=[
          'argparsex',
          'python-box>=4.0.4',  # TODO Remove this requirement (code custom frozen class)
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="optset options settings configuration defaults",
)
