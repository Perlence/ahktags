from setuptools import setup

with open('README.md') as fp:
    README = fp.read()

setup(
    name='ahktags',
    version='0.1',
    author='Sviatoslav Abakumov',
    author_email='dust.harvesting@gmail.com',
    description='Ctags-compatible tag generator for AutoHotkey',
    long_description=README,
    url='https://github.com/Perlence/ahktags',
    download_url='https://github.com/Perlence/ahktags/archive/master.zip',
    py_modules=['ahktags'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ahktags = ahktags:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
