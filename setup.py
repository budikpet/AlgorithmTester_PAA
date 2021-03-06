from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

setup(
    name='algorithm_tester_paa',
    version='0.1',
    description='Algorithms for MI-PAA, uses AlgorithmTester.',
    #long_description=long_description,
    keywords="algorithms,budikpet,cli",
    ext_modules = cythonize(
        [
            Extension('csa', ['package_algorithms/knapsack/csa.pyx'], include_dirs=[numpy.get_include()]),
            Extension('csa_sat', ['package_algorithms/sat/csa_sat.pyx'], include_dirs=[numpy.get_include()])
        ],
        language_level=3),
    setup_requires=['pytest-runner'],
    install_requires=['algorithm_tester'],
    tests_require=['pytest==5.0.1', 'flexmock'],
    
    # All these 'dev' packages can then be installed by 'pip install .[dev]'
    extras_require={
        'dev':  ["sphinx"],
        'analysis': ['notebook', 'pandas', 'openpyxl', 'matplotlib'],
        'tests': ['pytest==5.0.1', 'flexmock']
    },
    python_requires='>=3.7',
    author='Petr Budík',
    author_email='budikpet@fit.cvut.cz',
    license='Public Domain',
    url='https://github.com/budikpet/AlgorithmTester_PAA',
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'algorithm_tester.plugins': [
            'algorithms = package_algorithms',
            'parsers = package_parsers'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
        ],
)