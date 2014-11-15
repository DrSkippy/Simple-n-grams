from distutils.core import setup

setup(
    name='sngrams',
    version='0.1.5',
    author='Scott Hendrickson',
    author_email='scott@drskippy.net',
    packages=['simple_n_grams'],
    scripts=['term_frequency.py'],
    url='https://github.com/DrSkippy27/SimpleNGrams',
    download_url='https://github.com/DrSkippy27/SimpleNGrams/tags/',
    license='LICENSE.txt',
    description='Term and paragraph frequency counts for non-stopwords in input document.',
    install_requires=[]
    )
