from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="oscn",
    version="0.0.0.85",
    description="Oklahoma State Courts Network case parsing utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codefortulsa/oscn",
    author="John Dungan",
    author_email="john@docket2me.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=["requests", "beautifulsoup4", "boto3","python-decouple"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
