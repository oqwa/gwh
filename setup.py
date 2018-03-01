from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="gwh",
    version=__import__('gwh').__version__,
    keywords="git webhook flask bitbucket",
    description="Tool for handling Git webhooks based on Flask",
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    platforms="any",
    author="oqwa",
    author_email="oqwa@inbox.lv",
    license="MIT",
    url="https://github.com/oqwa/gwh",
    install_requires=['Flask>=0.12.2'],
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    setup_requires=['pytest', 'pytest-runner', 'pytest-flask'],
    tests_require=['pytest'],
    zip_safe=False
)
