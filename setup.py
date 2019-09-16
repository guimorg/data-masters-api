import os

from setuptools import (
    setup,
    find_packages
)


from api import __version__



def get_long_description():
    readme = ""

    with open('README.md', encoding='utf-8') as readme_file:
        readme = readme_file.read()

    return readme

requirements = [line.strip() for line in open("requirements.txt", 'r')]
test_requirements = [line.strip() for line in open("dev-requirements.txt", 'r')]

setup(
    name='api',
    version='{version}'.format(version=__version__),
    description="Simple API to serve a Machine Learning Model",
    long_description=get_long_description(),
    author="Guilherme Gimenez Jr",
    author_email='ggimenezjr@gmail.com',
    url='https://github.com/guimorg/machine-learning-api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="api, machine-learning",
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'run_api=api.app:run_app'
        ]
    }
)
