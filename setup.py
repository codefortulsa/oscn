from setuptools import setup, find_packages

setup(  name='oscn',
        version='0.1',
        description='Oklahoma Supreme Court Network page parsing utilities',
        url='https://github.com/codefortulsa/oscn',
        author='Code for Tulsa',
        author_email='code-for-tulsa@googlegroups.com',
        license='MIT',
        packages=find_packages(),
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            ],
        )
