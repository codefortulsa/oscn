from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(  name='oscn',
        version='0.0.0.28',
        description='Oklahoma State Courts Network case parsing utilities',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/codefortulsa/oscn',
        author='Code for Tulsa',
        author_email='code-for-tulsa@googlegroups.com',
        license='MIT',
        packages=find_packages(),
        zip_safe=False,
        install_requires=[
            'requests',
            'beautifulsoup4',
            ],
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            ],
        )
