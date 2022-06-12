from setuptools import find_packages, setup
from setuptools.extension import Extension


with open('README.rst') as readme:
    long_description = readme.read()


setup(
    name='weighted_levenshtein_list',
    version='0.1.0',
    description=(
        'Library providing functions to calculate Levenshtein distance, Optimal String Alignment distance, '
        'and Damerau-Levenshtein distance, where the cost of each operation can be weighted by letter.'
    ),
    long_description=long_description,
    url='https://github.com/YassineZiyad/weighted-levenshtein-list',
    author_email='yassineziyad.yz@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='Levenshtein Damerau weight weighted distance',
    test_suite='test.test',
    packages=find_packages(exclude=('test', 'docs',)),
    package_data={
        'weighted_levenshtein_list': ['clev.pxd', 'clev.pyx'],
    },
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        'setuptools >= 18.0',
        'cython',
    ],
    ext_modules=[Extension("weighted_levenshtein_list.clev", ['weighted_levenshtein_list/clev.pyx'])],
)
