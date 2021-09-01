from setuptools import setup, find_packages

with open('README.md', mode='r', encoding='utf8') as f:
    README = f.read()

with open('requirements.txt', mode='r', encoding='utf8') as f:
    DEPENDENCIES = f.read().splitlines()

with open('tests/requirements.txt', mode='r', encoding='utf8') as f:
    TEST_DEPENDENCIES = f.read().splitlines()

setup(
    name="nanomake",
    version='0.1.0',
    description='A new way to build, test and distribute your C/C++ projects and libraries 🚀',
    python_requires='>=3.9,<4',

    long_description=README,
    long_description_content_type='text/markdown',

    author='Alon Krymgand Osovsky',
    author_email='downtown2u@gmail.com',

    packages=find_packages(),
    install_requires=DEPENDENCIES,

    extras_require={
        'dev': TEST_DEPENDENCIES,
    },

    entry_points={
        'console_scripts': [
            'nanomake=nanomake.__main__:main'
        ]
    }
)
