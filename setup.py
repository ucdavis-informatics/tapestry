from setuptools import setup

setup(
    name='tapestry',
    version='5.0.2',
    description='TDAP Temporal Data Alignment Platform',
    author='Bill Riedl',
    author_email='awriedl@ucdavis.edu',
    url='https://gitlab.ri.ucdavis.edu/ri/pytdap',
    packages=['tdap'],
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=['pandas', 'numpy', 'scipy', 'sqlalchemy', 'pytz', 'cx-oracle', 'ucd-ri-pydbutils>=3.0.0', 'ruptures', 'piesafe>=2','python-dotenv'],
    python_requires='>=3.8',
    license='GPLv3'
)
